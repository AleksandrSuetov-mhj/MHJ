"""Метод Хука-Дживса "классический", c эвристикой "поиска по образцу"
   Без изменения шага поиска на сетке.
"""

import globVars as gv
import MHJ_proc1 as proc1
import MHJ_print1 as print1
import MHJ_kl_0  as mk0


def HJM_1 (pFun, pX, nev_max=0, ss_init=1.0, ss_min=0.0001, ss_koef=0.5):
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

  procName = "MHJ_KL_2"
  # Инициализация глобальных переменных
  proc1.initGlobVars (pX, pFun, nev_max, ss_init, ss_min, ss_koef)
  proc1.initFiles("infGridKL1.txt","infCoorKL1.txt")
  if self.infoLevMeth>0 :
    print1.printInitInfo(procName)
  
  ss_cur = ss_init

  print1.printGridInfoTitle(self.fInfoGrid)
  print1.printGridInfoTitle(self.fInfoCoord,"grid:")

  # Цикл по сеткам с убывающими размерами шагов
  while True : # + + + Цикл уменьшения шага сетки
    searchCurGrid(pX, ss_cur)
    if ss_cur < ss_min or self.NEv >= nev_max : 
      break  # Достигнут мин. шаг сетки или макс. количество вычислений
    else:    # Уменьшаем шаг сетки
      ss_cur = ss_cur * ss_koef
    # - - - Цикл уменьшения шага сетки


  # Вывод итоговой информации
  if self.infoLevMeth>0 :
    print1.printFinishInfo(procName)

  proc1.finitFiles()

  return 0
  
# = = = = =  HJM_1


def searchCurGrid (pX, ss_cur) :
  """ Поиск стационарного узла текущей сетки"""

  # Сохранение данных до поиска
  prevNEv = self.NEv
  prevNSc = self.NSc
  prevFval = self.Fval
  #self.grid PathLen = 0
  self.ss_mult = [1]*self.dim
  if self.infoLevGrid >0 :
    print("\nStart searchCurGrid:",'prevFval=',prevFval,'ss_cur=',ss_cur,end="")

  print1.printGridInfo(self.fInfoCoord,"2:")
  print1.printCoordInfoTitle()
  
  while True :
    if pollCoords(pX, ss_cur)  or self.NEv >= self.maxNEv :
      break
      
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if self.infoLevGrid >0 :
    print("\nFinsh searchCurGrid: ",end="")
    print(f"dNEv/dNSc={self.NEv-prevNEv}/{self.NSc-prevNSc}; dFval={self.Fval-prevFval}; ", end="")
    print(f"PthLen={self.gridPathLen}",end="")

  print1.printGridInfo(self.fInfoGrid)

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
    if mk0.isGoodDirection(pX, i, ss_cur) : 
      isStac = False     # Если положительное направление неубывающее, то успех
    elif mk0.isGoodDirection(pX, -i, ss_cur) :  # Иначе проверяем отрицательное направление
      isStac = False
    """if isGoodDirection(pX, i, ss_cur) : 
      isStac = False     # Если положительное направление неубывающее, то успех
    elif isGoodDirection(pX, -i, ss_cur) :  # Иначе проверяем отрицательное направление
      isStac = False"""
  # - - - for

  # Поиск в направлении суммарного смещения
  if not isStac and self.useSearchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)

  # Вывод информации о результатах проверки всех направлений
  if self.infoLevCoord>0 :     
    print("//", end="")
    
  print1.printCoordInfo()
  
  return isStac
# = = = = = pollCoords



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
