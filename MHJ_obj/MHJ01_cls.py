"""Класс для Метода Хука-Дживса с блокированием направления, противоположного к последнему успешном 
"""

import math
import typing

from MHJ_obj.MHJ00_cls import MHJ00_cls
from MHJ_obj.MHJ01_prn import MHJ01_prn
from MHJ_obj.MHJ01_wrt import MHJ01_wrt


class MHJ01_cls ( MHJ00_cls ) :
  
  obj_num = 0

  
  def __initWrt ( self ) :
    # Объекты для записи информации о ходе и результе процесса
    if hasattr(self,"wrt") : return 
    self.wrt = MHJ01_wrt(self)
    self.prn = MHJ01_prn(self)
  # = = = = = __initWrt/MHJ01_cls
  
  
  def __init__(self, pFun:typing.Callable[[list[float]], float],
               pX:list[float], pMinFval=-math.inf,
               pNev_max=-1, pSs_init=0.1, pSs_min=0.0001, pSs_coef=2) -> None:
    """ Инициализация полей объекта 2024-08-28"""
    # Имена и Файлы для записи информации о результатах

    # Вызов конструктора родителя
    self.__initWrt() 
    super().__init__(pFun, pX, pMinFval, pNev_max, pSs_init, pSs_min, pSs_coef)

    self.Nblk = 0
    self.useBlock = True
  # = = = = = __init__/MHJ01_cls


  def searchGridInit (self) :
    # Сохранение данных до поиска
    super().searchGridInit()
    self.prevNblk = self.Nblk
    self.iCoord_succ = -1
    self.iDir_succ   = -1
    return
  # = = = = = searchGridInit/MHJ01_cls


  def pollCoordsInit (self) :
    super().pollCoordsInit()
    self.prevNblk_poll = self.Nblk
  # = = = = = pollCoordsInit/MHJ00_cls
  

  def isGoodDirection (self, pI, pD) :
    """ Проверка заданного направления (pI,pD)
        Плюс дополнительные действия"""
    """Метод предполагается переопределять в производных классах"""

    if self.useBlock and self.iCoord_succ==pI and self.Dir_succ==pD :
      self.Nblk += 1
      self.curCoord = pI+1
      self.curDir   = pD
      self.wrt.writeDirInfoDir( self.wrt.fInfoDir )
      self.wrt.fInfoDir.write("Direction is Blocked")
      return False
    elif self.isGoodDir0( pI, pD ) : # Проверяем направление
      self.iCoord_succ = pI           # При успехе -
      self.Dir_succ = 0 if pD==1 else 1 # Запоминаем противоположное направление
      return True           

  # = = = = = isGoodDirection/MHJ01_cls

  
# = = = = = MHJ_cls_01


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

# = = = = = trash/MHJ01_cls


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ01_cls
 
  from tsFuncs.tsFnRosen import tsFnRosen
  from tsFuncs.tsFnBVP1d import tsFnBVP1d

  print("\n+ + + + + Проверка работы модуля "+__file__,end="")

  X : list[float]

  def set_X ( pDim ) :
    global X
    X = [1] * pDim
    X[0] = -1

  
  for i in range(2,3) :
    set_X(i)
    mhj = MHJ01_cls(tsFnRosen, X, pSs_init=0.01, pSs_min=1e-3, pNev_max=1e5, pMinFval=1e-1)
    #mhj01.useBlock = False
    mhj.searchAllGrids()
  
  print("\n- - - - - Проверка работы модуля завешилась штатно/"+__file__)
