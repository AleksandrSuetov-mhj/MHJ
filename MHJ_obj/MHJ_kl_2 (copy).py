"""Метод Хука-Дживса "классический", c эвристикой "поиска по образцу"
  С изменением шага поиска на сетке.
"""

import globVars as gv
import MHJ_proc1 as proc1
import MHJ_print1 as print1
import MHJ_kl_0  as mk0


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
  proc1.initFiles(self.dirInfo+"infGridKL2.txt",self.dirInfo+"infCoorKL2.txt")

  if self.infoLevMeth>0 :
    self.writeInitInfo(procName)
  
  ss_cur = ss_init
  self.write GridInfoTitle(self.fInfoGrid)
  self.write GridInfoTitle(self.fInfoCoord,"grid:")

  # Цикл по сеткам с убывающими размерами шагов
  while True : # + + + Цикл уменьшения шага сетки
    self.ss_cur = ss_cur
    self.ss_mult = [2]*self.dim
    self.ss_mult = [min(self.ss_mult_max,self.ss_mult_init)]*self.dim 
    searchCurGrid(pX, ss_cur)
    if ss_cur < ss_min or self.NEv >= nev_max : 
      break  # Достигнут мин. шаг сетки или макс. количество вычислений
    else:    # Уменьшаем шаг сетки
      ss_cur = ss_cur * ss_koef
    # - - - Цикл уменьшения шага сетки


  # Вывод итоговой информации
  if self.infoLevMeth>0 :
    self.writeFinishInfo(procName)
  return 0
  
# = = = = =  HJM_1


def searchCurGrid (pX, ss_cur) :
  """ Поиск стационарного узла текущей сетки"""
  self.write GridInfo(self.fInfoCoord,"gKL1:")
  self.write CoordInfoTitle()

  # Сохранение данных до поиска
  self.prevNEv = self.NEv
  self.prevNSc = self.NSc
  self.prevNBlk = self.NBlk
  self.prevFval = self.Fval
  self.prevPathLen = self.gridPathLen
  '''
  prevNEv = self.NEv
  prevNSc = self.NSc
  prevFval = self.Fval
  '''
  #self.grid PathLen = 0
                       

  if self.infoLevGrid >0 :
    print("\nStart searchCurGrid:",'prevFval=',self.prevFval,'ss_cur=',self.ss_cur,end="")
  
 
  while True :
    if self.infoLevCoord>0 : print("||", end="")
    if pollCoords(pX, ss_cur)  or self.NEv >= self.maxNEv :
      break
      
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if self.infoLevGrid >0 :
    print("\nFinsh searchCurGrid: ",end="")
    print(f"dNEv/dNSc={self.NEv-self.prevNEv}/{self.NSc-self.prevNSc}; dFval={self.Fval-self.prevFval}; ", end="")
    print(f"PthLen={self.gridPathLen}",end="")

  self.writeGridInfo(self.fInfoGrid)

  return 0
# = = = = = searchCurGrid  
  

def pollCoords (pX, ss_cur) :
  """ Цикл по координатам для текущего узла сетки"""
  """ Замечание: возможен вариант с выходом из цикла при первом успехе"""
  isStac= True
  prevX = pX.copy() # Для поиска в направлении суммарного смещения

  #print("pollCoords: ",end="")
  for i in range (1,self.dim+1) :
    # Замечание: можно обойтись одним "if" с ленивым "or"
    if   isGoodDirVarSS(pX, i, ss_cur) : 
      isStac = False     # Если положительное направление неубывающее, то успех
    elif isGoodDirVarSS(pX, -i, ss_cur) :  # Иначе проверяем отрицательное направление
      isStac = False
  # - - - for

  # Поиск в направлении суммарного смещения
  if not isStac and self.searchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)

  # Вывод информации о результатах проверки всех направлений
  if self.infoLevCoord>0 :     
    print("//", end="")

  self.writeCoordInfo()
  
  return isStac
# = = = = = pollCoords



def isGoodDirVarSS ( pX, pI, ss_cur ) :
  """ Проверка заданного направления переменными шагами поиска"""
  """ abs(pI) - номер координаты, sign(pI) - направление по этой координате"""

  i = abs(pI) - 1 # Индекс координаты
  iDir = 1 if pI>0 else 0 # Индекс направления

  if self.infoLevCoord>0 :
    print(f"{pI:+}", end="/")

  oldX = pX[i]
  if pI >0 : pX[i] += ss_cur*self.ss_mult[i]
  else     : pX[i] -= ss_cur*self.ss_mult[i]

  newFval = self.func(pX)
  if self.infoLevCoord>0 :
    print(f"{self.Fval-newFval:+.1e}({self.ss_mult[i]})", end="; ")

  if newFval<self.Fval : # Принимаем новое приближение
    self.Fval = newFval
    self.NSc += 1
    self.gridPathLen += ss_cur*self.ss_mult[i]
    proc1.incSSmult(i)
    return True
  else :               
    pX[i] = oldX
    if self.ss_mult[i] == 1 : # Регистрируем неуспешную попытку
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
    if pI >0 : pX[i] += ss_cur*self.ss_mult[i]
    else     : pX[i] -= ss_cur*self.ss_mult[i]
  
    newFval = func(pX)
    if self.infoLevCoord :
      print(f"{pI:+}/{self.Fval-newFval:+.1e}", end="; ")
  
    if newFval<self.Fval :
      self.Fval = newFval
      self.NSc += 1
      self.gridPathLen += ss_cur*self.ss_mult[i]
      return True
    else :
      pX[i] = oldX
      return False
  # = = = = = isGoodDirection
  
  2024-08-01 Заменено на функцию MHJ_proc1.initGlobVars
  self.Func = pFun
  self.Fval = self.Func(pX)
  self.maxNEv = nev_max
  self.NEv = 0
  self.NSc = 0


  2024-08-03 Заменено на функцию MHJ_print.printInitInfo
  print(f'Значение: {self.Fval}; Начальное приближение: {pX}')
  #, "Функция: ", self.Func.__name__)
  print(f'Длина шага начальная={ss_cur}', f', конечная={ss_min:.5e}',  f'; Макс.колич.вычислений={nev_max}')
  

  2024-08-03 Заменено на функцию MHJ_print.printFinishInfo
  print (f'HJM_1: Значение: {self.Fval:.5g}',end="; ")
  print(f"NEv/NSc={self.NEv}/{self.NSc}; ss_cur={ss_cur:.5g}")
  
"""
