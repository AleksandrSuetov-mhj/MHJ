"""Метод Хука-Дживса c обобщённым условием стационарности, только с этапом исследования направлений
(Обобщённое=распределённое, не локальное)
  Без эвристик
"""


import globVars as gv
import MHJ_print1 as print1
import MHJ_proc1 as proc1


def MHJ_GS_1 (pFun, pX, nev_max=0, ss_init=1.0, ss_min=0.0001, ss_сoef=0.5, pCoefTolDist=0.0, pCTD_min=1):
  '''   Метод Хука-Дживса с обобщённым условием стационарности, только с этапом опроса направлений '''
  '''
    pFun - функция, которую нужно минимизировать
    pN   - размерность задачи
    pX   - приближение к точке минимума; на входе - начальное приближение
    nev_max - максимальное количество вычислений функции
    ss_init - начальная длина шага (Step Size)
    ss_min  - минимальная (финальная) длина шага
    ss_koef - коэффициент уменьшения длины шага
    pCoefTolDist - для вычисления "приемлемого расстояния"
            на основе шага сетки и размерности задачи
  '''

  procName = "MHJ_GS_1"
  # Инициализация глобальных переменных
  proc1.initGlobVars (pX, pFun, nev_max, ss_init, ss_min, ss_сoef, pCoefTolDist)
  proc1.initFiles()

  if self.infoLevMeth>0 :
    print1.printInitInfo(procName)
  
  ss_cur = ss_init

  print1.printGridInfoTitle(self.fInfoGrid)
  print1.printGridInfoTitle(self.fInfoCoord,"grid:")
  

  # Цикл по сеткам с убывающими размерами шагов
  while True :   # + + + Цикл уменьшения шага сетки
    self.GCSdist = ss_cur*pCoefTolDist*self.dim
    #self.GCSdist_min = self.GCSdist*1.1
    #self.GCSdist_min = ss_cur*self.dim/2
    self.GCSdist_min = ss_cur/2
# Начальные расстояния до точек с возрастанием по направлениям
    self.incDirDist = [[-1-self.GCSdist]*self.dim,
                     [-1-self.GCSdist]*self.dim] 
    self.ss_mult = [min(self.ss_mult_max,self.ss_mult_init)]*self.dim # На новых сетках начинаем с увеличенным шагом
    # Но приемлемое расстояние вычисляется на основе шага сетки
    while True : # + + + Цикл уменьшения расстояния приемлемости
      self.ss_cur = ss_cur
      searchGridGCS(pX, ss_cur, pollCoordsGCS1)
      #searchGridGCS(pX, ss_cur, pollCoordsGCS1)
      if self.NEv >= nev_max  or self.GCSdist< self.ss_cur :
        break
      elif self.ss_cur <= self.ss_min :
        self.GCSdist /= 2
      elif self.GCSdist <= self.GCSdist_min  :
        break
      else :
        self.GCSdist /= 2
      # - - - Цикл уменьшения расстояние приемлемости  
    
    if ss_cur <= ss_min  or self.NEv >= nev_max: 
      break  # Достигнут мин. шаг сетки или макс. количество вычислений
    else:    # Уменьшаем шаг сетки
      ss_cur = ss_cur * ss_сoef
    # - - - Цикл уменьшения шага сетки
    
  # Вывод итоговой информации
  if self.infoLevMeth>0 :
    print1.printFinishInfo(procName)

  proc1.finitFiles()
  
  return 0
# = = = = =  HJM_GS_1

# # # # # # #

def pollCoordsGCS1 (pX, ss_cur) :
  """ Цикл по координатам и напрвлениям для текущего узла сетки"""
  """ Замечание: возможен вариант с выходом из цикла при первом успехе"""
  isStac= True
  prevX = pX.copy() # Для поиска в направлении суммарного смещения
  # prevPathLen = self.gridPathLen # Для использования в searchBadDirs

  #if self.infoLevCoord>0 :     print("pollCoords: ",end="")

  # Перебор координат
  for i in range (1,self.dim+1) :
    # Замечание: можно обойтись одним "if" с ленивым "or"
    if isGoodDirGCS(pX, i, ss_cur)  or isGoodDirGCS(pX, -i, ss_cur): # Если положительное направление неубывающее, то успех
      isStac = False 
   # - - - for

  # Поиск в направлении суммарного смещения
  if not isStac and self.searchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)
    #proc1.searchBadDirs(pX, prevX, prevPathLen, ss_cur)


  # Вывод информации о результатах проверки всех направлений
  if self.infoLevCoord>0 : print("//", end="")
  print1.printCoordInfo()

  return isStac
# = = = = = pollCoordsGCS1


def pollCoordsGCS2 (pX, ss_cur) :
  """ Проверка направлений в порядке удалённости от точек стационарности """
  
  isStac= True
  prevX = pX.copy() # Для поиска в направлении суммарного смещения
  # prevPathLen = self.gridPathLen # Для использования в searchBadDirs

  while self.NEv < self.maxNEv :
    # находим индексы направления с макс.удалением от точки с условием стационарности
    (iDirMax,iCoorMax,maxDist) = proc1.findDirMaxDist()  
    # Сравнить maxDist с расстояниием приемлемости?
    if maxDist <= self.GCSdist :
      isStac = True
      break
      
    iCoorMax +=1
    if iDirMax==0 : iCoorMax= -iCoorMax
    
    isGoodDirGCS(pX, iCoorMax, ss_cur)  # Возвращаемое значение не используется
  
      
  # Поиск в направлении суммарного смещения: здесь надо разобраться как вести
  """if not isStac and self.useSearchGoodDirs:
    proc1.searchGoodDirs(pX, prevX)
    #proc1.searchBadDirs(pX, prevX, prevPathLen, ss_cur)
  """

  # Вывод информации о результатах проверки направлени{я/й}

  return isStac
# = = = = = pollCoordsGCS2


def searchGridGCS (pX, ss_cur, pPollCoords=pollCoordsGCS1) :
  """ Поиск обобщённо-стационарного узла текущей сетки
      pPoolCoords = параметр-функция опроса направлений (2024-08-13)"""
  
  print1.printGridInfo(self.fInfoCoord,"gGCS:")
  proc1.initSearchGrid()
  
  isStacPoint = False # Признак обобщённо-стационарного узла
  while True :
    if pPollCoords(pX, ss_cur) :
      isStacPoint = True
      break
    elif self.NEv >= self.maxNEv :
      isStacPoint = False
      break
    else :
      continue
  # - - - Цикл поиска обобщённо-стационарного узла на сетке

  proc1.finitSearchGrid ( )
  return isStacPoint
  # = = = = = searchGridGCS

# # # # # # # 

def isGoodDirGCS (pX, pI, ss_cur) :
  """ Проверка заданного направления (положит. или отрицат.) для координаты"""
  """ abs(pI) - номер координаты, sign(pI) - направление по этой координате"""

  i = abs(pI) - 1 # Индекс координаты
  iDir = 1 if pI>0 else 0 # Индекс направления
  
  if self.infoLevCoord>0 : print(f"{pI:+}[{self.gridPathLen-self.incDirDist[iDir][i]:.2e}]", end="/")
  
  if self.gridPathLen-self.incDirDist[iDir][i] <= self.GCSdist  : # 
    self.NBlk += 1
    return False
  
  oldX = pX[i]
  if pI >0 : pX[i] += ss_cur*self.ss_mult[i]
  else     : pX[i] -= ss_cur*self.ss_mult[i]

  newFval = self.func(pX)
  if self.infoLevCoord>0 : print(f"{self.Fval-newFval:+.1e}({self.ss_mult[i]})", end="; ")
    
  if newFval<self.Fval : # Принимаем новое приближение
    self.Fval = newFval
    self.NSc += 1
    self.gridPathLen += ss_cur*self.ss_mult[i]    # После увеличения длины пути
                                              # Регистрируем неуспешность противоположного направления
    self.incDirDist[1-iDir][i] = self.gridPathLen #Даже если шаг большой

    proc1.incSSmult(i)
    return True
  else :               
    pX[i] = oldX
    if self.ss_mult[i] == 1 : # Регистрируем неуспешную попытку
      self.incDirDist[iDir][i] = self.gridPathLen
      return False
    else :
      proc1.decSSmult(i)
      return True  # Нужна новая попытка
# = = = = = isGoodDirGCS1


def trash () :
  """ Свалка

  2024-08-03,сб; Заменено на функцию MHJ_GS_1.printInitInfo
  print(f'Значение: {self.Fval}; Начальное приближение: {pX}')
  #, "Функция: ", self.Func.__name__)
  print(f'Длина шага начальная={ss_cur}, конечная={ss_min:.5e}',  
        f'; Макс.колич.вычислений={nev_max}, Коэф.расстояния GSC={pCoefTolDist}')


  2024-08-03,сб; Заменено на функцию MHJ_GS_1.printFinishInfo(procName)
        print (f'HJM_GS_1: Значение: {self.Fval:.5g}',end="; ")
        print(f"NEv/NSc/NBlk={self.NEv}/{self.NSc}/{self.NBlk}", end="; ")
        print(f"NSrch/NSrch2/NSrch2UnSc={self.NSearch}/{self.NSearch2}/{self.NSearch2UnSc}", end="; ") 
        print(f"ss_cur={ss_cur:.5g}",end="; ")
        print(f"totalPthLen={self.totalPathLen:.5g}")
        print (f'Конечное приближение: {pX}')

  """
# = = = = = trash /  Свалка  