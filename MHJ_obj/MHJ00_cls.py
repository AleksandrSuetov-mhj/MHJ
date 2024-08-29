"""Класс для Метода Хука-Дживса с блокированием направления, противоположного к последнему успешном 
"""


import typing
import math
from io import FileIO
from typing import Any

from MHJ_obj.MHJ0_wrt import MHJ0_wrt
from MHJ_obj.MHJ0_prn import MHJ0_prn

from MHJ_obj.MHJ0_cls import MHJ0_cls



class MHJ00_cls ( MHJ0_cls ) :
  
  obj_num = 0
  

  def __init__(self, pFun:typing.Callable[[list[float]], float],
               pX:list[float], pMinFval=-math.inf,
               pNev_max=-1, pSs_init=0.1, pSs_min=0.0001, pSs_coef=2) -> None:
    """ Инициализация полей объекта 2024-08-28"""
    # Имена и Файлы для записи информации о результатах

    # Вызов конструктора родителя
    super().__init__(pFun, pX, pMinFval, pNev_max, pSs_init, pSs_min, pSs_coef)

    self.Nblk = 0
  
  # = = = = = __init__

    
  '''
  def searchAllGrids (self, pSs_init=-1):
    """   Метод Хука-Дживса без поиска по образцу (без эвристик) """
    """
      ss_init - начальная длина шага (Step Size)
    """
  
    procName = __name__
    #self.ss _mult_max = 0
  
    if self.infoLevMeth>0 :
      self.printInitInfo(procName)

    if pSs_init < 0 :   self.ss_cur = self.ss_init
    else            :   self.ss_cur = pSs_init
    
    # Цикл по сеткам с убывающими размерами шагов
    while True : # + + + Цикл уменьшения шага сетки
      self.searchCurGrid()
      if (self.ss_cur < self.ss_min 
          or self.NEv >= self.maxNEv 
          or self.Fval<=self.minFval) : 
        break  # Достигнут мин. шаг сетки или макс. количество вычислений
      else:    # Уменьшаем шаг сетки
        self.ss_cur = self.ss_cur/self.ss_coef
      # - - - Цикл уменьшения шага сетки
  
    # Вывод итоговой информации
    if self.infoLevMeth>0 :
      self.printFinishInfo(procName)
      
    return 0
    
  # = = = = =  searchAllGrid
  '''

  '''
  def searchCurGrid (self) :
    """ Поиск стационарного узла текущей сетки"""
  
    # Сохранение данных до поиска
    self.prevNEv = self.NEv
    self.prevNSc = self.NSc
    self.prevFval = self.Fval
  
    if self.infoLevGrid >0 :
      print("Start searchCurGrid:",'prevFval=',self.prevFval,'ss_cur=',self.ss_cur)
    
    while True :
      if self.pollCoords()  or self.NEv >= self.maxNEv :
        break
      elif self.pathLen-self.prevPathLen < self.ss_cur/2 :
        print("Нет ни стационарности, ни смещения")
        
    # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
    if self.infoLevGrid >0 :
      print("Finsh searchCurGrid: ",end="")
      print(f"dNEv/dNSc={self.NEv-self.prevNEv}/{self.NSc-prevNSc}; dFval={self.Fval-prevFval}; ", end="")
      print(f"PthLen={self.pathLen}")
      
    return 0
  
  # = = = = = searchCurGrid  
  '''

  '''
  def pollCoords (self) :
    """ Цикл по координатам для текущего узла сетки"""
    """ Замечание: возможен вариант с выходом из цикла при первом успехе,
          Но зачем?"""
    isStac= True
    prevX = self.X.copy() # Для поиска в направлении суммарного смещения
  
    #print("pollCoords: ",end="")
    for i in range (1,self.dim+1) :
      # Замечание: можно обойтись одним "if" с ленивым "or"
      if   self.isGoodDirection( i ) :# Проверяем положительное направление вдоль оси
        isStac = False           
      elif self.isGoodDirection(-i ) :# При неуспеха проверяем отрицательное направление
        isStac = False
     # - - - for
  
    return isStac
    
  # = = = = = pollCoords
  '''
  
  '''
  def isGoodDirection (self, pI) :
    """ Проверка заданного направления (положительного или отрицательного) для заданной координаты
        Не используются множители для размера шага"""
    """ abs(pI) - номер координаты, sign(pI) - направление по этой координате
    """

    # Распаковываем номер координаты и индекс направления
    locCoord = abs(pI)
    locDir =  1 if pI>0 else 0
    if locDir==self.prevDir and locCoord==self.prevCoord :
      print(self.NEv, f"Блокировано {locCoord}, {locDir}")
      self.NBlk +=1
      return False

    i = abs(pI) - 1 # Индекс варьируемой компоненты
    oldX = self.X[i]
    if pI >0 : self.X[i] += self.stepSize(locCoord)
    else     : self.X[i] -= self.stepSize(locCoord)

    newFval = self.func(self.X)
    if self.infoLevCoord :
      print(f"{pI:+}/{self.Fval-newFval:+.1e}", end="; ")
      
    if newFval<self.Fval :
      self.Fval = newFval
      self.NSc += 1
      self.pathLen += self.stepSize(locCoord)
      if self.useBlockPrevDir :
        self.prevDir = 1-locDir
        self.prevCoord= locCoord
      return True
    else :
      self.X[i] = oldX
      return False
      
  # = = = = = idGoogDirection
  '''

  



  def test (self) : pass


# = = = = = MHJ_cls_0

def trash (self) :
  
  #   TODO: перенести в дочерний класс 2024-08-20,вт
  def searchGoodDirs ( self, prevX ) :
    """Поиск в направлении суммарного смещения 2024-08-01"""
    if not self.useSearchGoodDirs : return
    searchX = [0] * self.dim
    l1disp = 0
    for i in range(0, self.dim):
      dx = self.X[i] - self.prevX[i]
      l1disp += abs(dx)
      searchX[i] = 2 * self.X[i] - prevX[i]

    searchFval = self.func(searchX)
    if self.infoLevCoord > 0:
      print(f"!{self.Fval-searchFval:+.1e}", end="; ")

    if searchFval < self.Fval:
      self.Fval = searchFval
      self.NSearch += 1
      self.pathLen += l1disp
      for i in range(0, self.dim):
        self.X[i] = searchX[i]
    else:
      self.NSearchUnSc += 1

    return

  # = = = = = searchGoodDirs


  #TODO: перенести в дочерний класс 2024-08-20,вт
  def searchBadDirs(self, prevX, prevPathLen, ss_cur):
    """Поиск в направлении суммы неуспешных направлений 2024-08-16"""
    NotImplementedError("Метод пока не реализован как надо")

    """Надо использовать направления, которые были исследованы в последнем цикле, 
       но оказались неуспешными
       Без использования расстояния приемлемости """
    searchX = [0] * self.dim
    l1disp = 0
    numBadDirs = 0
    for iCoord in range(0, self.dim):
      for iDir in range(0, 2):
        # Проверка пригодности направления возрастания для поиска:
        # Данное направление проверялось и оказалось возрастающим
          numBadDirs += 1
          dx = -ss_cur if iDir == 1 else ss_cur  # сдвиг в направлении, противоположном возрастанию
          l1disp += abs(dx)
          searchX[iCoord] = self.X[iCoord] + dx
          # - - - if
        # - - - for iDir
      # - - - for iCoord

    if numBadDirs == 0:
      return

    searchFval = self.func(searchX)
    if searchFval < self.Fval:
      self.Fval = searchFval
      self.NSearch2 += 1
      self.gridPathLen += l1disp
      for i in range(0, self.dim):
        pX[i] = searchX[i]
    else:
      self.NSearch2UnSc += 1
    return
  # = = = = = searchBadDirs

  """ Свалка отходов

    TODO: перенести в дочерний класс 2024-08-20,вт
    def printFinishInfo 
    if hasattr(self,"searchGoodDirs") :
      self.printParam ("NSearch",pSep="/")
    if hasattr(self,"searchBadDirs")  :
      self.printParam ("NSearch2",pSep="/")
      self.printParam ("NSearch2UnSc",pSep="/")


        TODO: перенести в дочерний класс 2024-08-20,вт
        def poolCoords
          # Поиск в направлении суммарного смещения
          if not isStac and self.useSearchGoodDirs:
            self.searchGoodDirs(prevX)

          # Вывод информации о результатах проверки всех направлений
          if self.infoLevCoord>0 :     
            print("//", end="")

      

        def initCounts
        # Счётчики поисков по суммарным направлениям 
        if self.useSearchGoodDirs :
          self.NSearch = 0     # количество поисков по суммам успешных направлений
          self.NSearchUnSc = 0 # количество Успешных поисков по суммам успешных направлений
        if self.useSearchBadDirs :
          self.NSearch2= 0      # количество поисков по минус суммам неуспешных направлений
          self.NSearch2UnSc = 0 # количество Успешных поисков по минус суммам неуспешных направлений

        # TODO: перенести в дочерний класс 2024-08-20,вт
        def __init__
        # self.useSearchGoodDirs = False
        # self.useSearchBadDirs = False
          

  """
  pass

# = = = = = trash


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ_cls_0
  import sys
  from tsFuncs.tsFnRosen import tsFnRosen
  from tsFuncs.tsFnBVP1d import tsFnBVP1d


  X : list[float]

  def set_X ( pDim ) :
    global X
    X = [1] * pDim
    X[0] = -1

  
  for i in range(1,5) :
    set_X(i)
    mhj0 = MHJ_cls_0(tsFnRosen, X, 0.1)
    mhj0.searchAllGrids()
    set_X(i)
    mhj0 = MHJ_cls_0(tsFnRosen, X, 0.1)
    mhj0.useBlockPrevDir = True
    mhj0.searchAllGrids()
  
  sys.exit("Работа модуля MHJ_cls_0 завешилась штатно")
