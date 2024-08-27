"""Метод Хука-Дживса "классический", c эвристикой "поиска по образцу"
  С изменением шага поиска на сетке.
"""

import MHJ_proc.MHJ_globVars as gv
import MHJ_proc.MHJ_proc1 as proc1
import MHJ_proc.MHJ_print1 as print1
import MHJ_proc.MHJ_kl_0  as mk0


def HJM_2 (pFun, pX, nev_max=0, ss_init=1.0, ss_min=0.0001, ss_koef=0.5):
  '''   Метод Хука-Дживса без поиска по образцу (без эвристик) '''
  '''
    pFun - функция, которую нужно минимизировать
    pN   - размерность задачи
    pX   - приближение к точке минимума; на входе - начальное приближение
    nev_max - максимальное количество вычислений функции
    ss_init - начальная длина шага (Step Size)
    ss_min  - минимальная (финальная) длина шага
    ss_coef - коэффициент уменьшения длины шага
  '''

  procName = __name__
  # Инициализация глобальных переменных
  proc1.initGlobVars (pX, pFun, nev_max, ss_init, ss_min, ss_koef)
  proc1.initFiles(gv.dirInfo+"infGridKL2.txt",gv.dirInfo+"infCoorKL2.txt")

  if gv.infoLevMeth>0 :
    print1.printInitInfo(procName)
  
  ss_cur = ss_init
  print1.printGridInfoTitle(gv.fInfoGrid)
  print1.printGridInfoTitle(gv.fInfoCoord,"grid:")

  # Цикл по сеткам с убывающими размерами шагов
  while True : # + + + Цикл уменьшения шага сетки
    gv.ss_cur = ss_cur
    gv.ss_mult = [2]*gv.dim
    gv.ss_mult = [min(gv.ss_mult_max,gv.ss_mult_init)]*gv.dim 
    searchCurGrid(pX, ss_cur)
    if ss_cur < ss_min or gv.NEv >= nev_max : 
      break  # Достигнут мин. шаг сетки или макс. количество вычислений
    else:    # Уменьшаем шаг сетки
      ss_cur = ss_cur * ss_koef
    # - - - Цикл уменьшения шага сетки


  # Вывод итоговой информации
  if gv.infoLevMeth>0 :
    print1.printFinishInfo(procName)
  return 0
  
# = = = = =  HJM_1


def searchCurGrid (pX, ss_cur) :
  """ Поиск стационарного узла текущей сетки"""
  print1.printGridInfo(gv.fInfoCoord,"gKL1:")
  print1.printCoordInfoTitle()

  # Сохранение данных до поиска
  gv.prevNEv = gv.NEv
  gv.prevNSc = gv.NSc
  gv.prevNBlk = gv.NBlk
  gv.prevFval = gv.Fval
  gv.prevPathLen = gv.gridPathLen
  '''
  prevNEv = gv.NEv
  prevNSc = gv.NSc
  prevFval = gv.Fval
  '''
  #gv.grid PathLen = 0
                       

  if gv.infoLevGrid >0 :
    print("\nStart searchCurGrid:",'prevFval=',gv.prevFval,'ss_cur=',gv.ss_cur,end="")
  
 
  while True :
    if gv.infoLevCoord>0 : print("||", end="")
    if pollCoords(pX, ss_cur)  or gv.NEv >= gv.maxNEv :
      break
      
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if gv.infoLevGrid >0 :
    print("\nFinsh searchCurGrid: ",end="")
    print(f"dNEv/dNSc={gv.NEv-gv.prevNEv}/{gv.NSc-gv.prevNSc}; dFval={gv.Fval-gv.prevFval}; ", end="")
    print(f"PthLen={gv.gridPathLen}",end="")

  print1.printGridInfo(gv.fInfoGrid)

  return 0
# = = = = = searchCurGrid  
  

def pollCoords (pX, ss_cur) :
  """ Цикл по координатам для текущего узла сетки"""
  """ Замечание: возможен вариант с выходом из цикла при первом успехе"""
  isStac= True
  prevX = pX.copy() # Для поиска в направлении суммарного смещения

  #print("pollCoords: ",end="")
  for i in range (1,gv.dim+1) :
    # Замечание: можно обойтись одним "if" с ленивым "or"
    if   isGoodDirVarSS(pX, i, ss_cur) : 
      isStac = False     # Если положительное направление неубывающее, то успех
    elif isGoodDirVarSS(pX, -i, ss_cur) :  # Иначе проверяем отрицательное направление
      isStac = False
  # - - - for

  # Поиск в направлении суммарного смещения
  if not isStac and gv.searchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)

  # Вывод информации о результатах проверки всех направлений
  if gv.infoLevCoord>0 :     
    print("//", end="")

  print1.printCoordInfo()
  
  return isStac
# = = = = = pollCoords



def isGoodDirVarSS ( pX, pI, ss_cur ) :
  """ Проверка заданного направления переменными шагами поиска"""
  """ abs(pI) - номер координаты, sign(pI) - направление по этой координате"""

  i = abs(pI) - 1 # Индекс координаты
  iDir = 1 if pI>0 else 0 # Индекс направления

  if gv.infoLevCoord>0 :
    print(f"{pI:+}", end="/")

  oldX = pX[i]
  if pI >0 : pX[i] += ss_cur*gv.ss_mult[i]
  else     : pX[i] -= ss_cur*gv.ss_mult[i]

  newFval = gv.func(pX)
  if gv.infoLevCoord>0 :
    print(f"{gv.Fval-newFval:+.1e}({gv.ss_mult[i]})", end="; ")

  if newFval<gv.Fval : # Принимаем новое приближение
    gv.Fval = newFval
    gv.NSc += 1
    gv.gridPathLen += ss_cur*gv.ss_mult[i]
    proc1.incSSmult(i)
    return True
  else :               
    pX[i] = oldX
    if gv.ss_mult[i] == 1 : # Регистрируем неуспешную попытку
      return False
    else :                  # Уменьшаем множитель для шага поиска
      proc1.decSSmult(i)
      return False

  # = = = = = isGoodDirGCS


""" Свалка отходов

  2024-08-05,пн Заменено на MHJ_kl_0.isGoodDirection
  Похоже на MHJ_GS_1.MHJ_GS_1
  def isGoodDirection (pX, pI, ss_cur) :
    # Проверка заданного направления (положительного или отрицательного) для заданной координаты
    # abs(pI) - номер координаты, 
    # sign(pI) - направление по этой координате
  
    i = abs(pI) - 1 # Индекс варьируемой компоненты
    oldX = pX[i]
    if pI >0 : pX[i] += ss_cur*gv.ss_mult[i]
    else     : pX[i] -= ss_cur*gv.ss_mult[i]
  
    newFval = func(pX)
    if gv.infoLevCoord :
      print(f"{pI:+}/{gv.Fval-newFval:+.1e}", end="; ")
  
    if newFval<gv.Fval :
      gv.Fval = newFval
      gv.NSc += 1
      gv.gridPathLen += ss_cur*gv.ss_mult[i]
      return True
    else :
      pX[i] = oldX
      return False
  # = = = = = isGoodDirection
  
  2024-08-01 Заменено на функцию MHJ_proc1.initGlobVars
  gv.Func = pFun
  gv.Fval = gv.Func(pX)
  gv.maxNEv = nev_max
  gv.NEv = 0
  gv.NSc = 0


  2024-08-03 Заменено на функцию MHJ_print.printInitInfo
  print(f'Значение: {gv.Fval}; Начальное приближение: {pX}')
  #, "Функция: ", gv.Func.__name__)
  print(f'Длина шага начальная={ss_cur}', f', конечная={ss_min:.5e}',  f'; Макс.колич.вычислений={nev_max}')
  

  2024-08-03 Заменено на функцию MHJ_print.printFinishInfo
  print (f'HJM_1: Значение: {gv.Fval:.5g}',end="; ")
  print(f"NEv/NSc={gv.NEv}/{gv.NSc}; ss_cur={ss_cur:.5g}")
  
"""
