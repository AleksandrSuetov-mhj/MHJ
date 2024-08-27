"""Метод Хука-Дживса "классический"/"базовый", только с этапом исследования направлений

  Без эвристик
"""
#from _typeshed import Self
import math

import MHJ_proc.MHJ_globVars as gv
import MHJ_proc.MHJ_proc1 as proc1
import MHJ_proc.MHJ_print1 as print1


def HJM_0 (pFun, pX, nev_max=0, ss_init=1.0, ss_min=0.0001, ss_koef=0.5):
  '''   Метод Хука-Дживса без поиска по образцу (без эвристик) '''
  '''
    pFun - функция, которую нужно минимизировать
    pN   - размерность задачи
    pX   - приближение к точке минимума; на входе - начальное приближение
    nev_max - максимальное количество вычислений функции
    ss_init - начальная длина шага (Step Size)
    ss_min  - минимальная (финальная) длина шага
    ss_koef - коэффициент уменьшения длины шага
  '''

  procName = __name__
  # Инициализация глобальных переменных
  proc1.initGlobVars (pX, pFun, nev_max, ss_init, ss_min, ss_koef)
  #gv.ss _mult_max = 0

  if gv.infoLevMeth>0 :
    print1.printInitInfo(procName)

  ss_cur = ss_init
  
  # Цикл по сеткам с убывающими размерами шагов
  while True : # + + + Цикл уменьшения шага сетки
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

  # Сохранение данных до поиска
  prevNEv = gv.NEv
  prevNSc = gv.NSc
  prevFval = gv.Fval

  gv.ss_mult = [0]*gv.dim #Исключаем увеличение шага сетки
  if gv.infoLevGrid >0 :
    print("Start searchCurGrid:",'prevFval=',prevFval,'ss_cur=',ss_cur)
  
  while True :
    if pollCoords(pX, ss_cur)  or gv.NEv >= gv.maxNEv :
      break
      
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if gv.infoLevGrid >0 :
    print("Finsh searchCurGrid: ",end="")
    print(f"dNEv/dNSc={gv.NEv-prevNEv}/{gv.NSc-prevNSc}; dFval={gv.Fval-prevFval}; ", end="")
    print(f"PthLen={gv.gridPathLen}")
    
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
    if isGoodDirection(pX, i, ss_cur) : 
      isStac = False     # Если положительное направление неубывающее, то успех
    elif isGoodDirection(pX, -i, ss_cur) :  # Иначе проверяем отрицательное направление
      isStac = False
   # - - - for

  # Поиск в направлении суммарного смещения
  if not isStac and gv.useSearchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)

  # Вывод информации о результатах проверки всех направлений
  if gv.infoLevCoord>0 :     
    print("//", end="")

  return isStac
# = = = = = pollCoords


def isGoodDirection (pX, pI, ss_cur) :
  """ Проверка заданного направления (положительного или отрицательного) для заданной координаты"""
  """ abs(pI) - номер координаты, sign(pI) - направление по этой координате"""

  i = abs(pI) - 1 # Индекс варьируемой компоненты
  oldX = pX[i]
  if pI >0 : pX[i] += ss_cur
  else     : pX[i] -= ss_cur

  newFval = gv.func(pX)
  if gv.infoLevCoord :
    print(f"{pI:+}/{gv.Fval-newFval:+.1e}", end="; ")
    
  if newFval<gv.Fval :
    gv.Fval = newFval
    gv.NSc += 1
    gv.gridPathLen += ss_cur
    return True
  else :
    pX[i] = oldX
    return False
# = = = = = checkDirection




""" Свалка отходов

  #2024-08-05,пн Перенесено в globVars
  def func (pX) :
    gv.NEv += 1
    return gv.Func (pX)
  

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
