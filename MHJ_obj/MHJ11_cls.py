""" Класс для Метода Хука-Дживса с использованием суммы успешных направлений
    после опроса всех координат
"""


import math
import typing

from MHJ_obj.MHJ00_cls import MHJ00_cls
from MHJ_obj.MHJ11_prn import MHJ11_prn
from MHJ_obj.MHJ11_wrt import MHJ11_wrt


class MHJ11_cls ( MHJ00_cls ) :

  obj_num = 0


  def __initWrt ( self ) :
    # Объекты для записи информации о ходе и результе процесса
    if hasattr(self,"wrt") : return 
    self.wrt = MHJ11_wrt(self)
    self.prn = MHJ11_prn(self)
  # = = = = = __initWrt/MHJ11_cls

  
   
  def initVars ( self ) :
    #TODO: Почему это не работает ??? 2024-08-30,пт
    super().initVars()
    self.NSrchGd = 0   # Кол-во поисков в направленииях смещения за цикл опроса
    self.NSrchGdSc = 0 # Кол-во Успешных поисков в направленииях смещения за цикл опроса
    print("\n__initVars/MHJ11_cls")
  # = = = = = __initVars/MHJ11_cls
  

  def __init__(self, pFun:typing.Callable[[list[float]], float],
               pX:list[float], pMinFval=-math.inf,
               pNev_max=-1, pSs_init=0.1, pSs_min=0.0001, pSs_coef=2, pName="") -> None:
    """ Инициализация полей объекта 2024-08-30"""
    # Имена и Файлы для записи информации о результатах
    self.__initWrt() 
    
    #self.initVars()
    self.useSearchGoodDirs = True
    
    super().__init__(pFun, pX, pMinFval, pNev_max, pSs_init, pSs_min, pSs_coef,pName)

    return
  # = = = = = __init__/MHJ11_cls


  def searchGridInit (self) :
    super().searchGridInit()
    # Сохранение данных до поиска
    self.prevNSrchGd = self.NSrchGd
    self.prevNSrchGdSc = self.NSrchGdSc
  
    if self.infoLevGrid >0 :
      print("")
  
    return
  # = = = = = initSearchGrid/MHJ11_cls


  def searchGoodDirs ( self ) :
    """Поиск в направлении суммарного смещения 2024-08-11"""
    # Вызывается после цикла опроса всех координат (и некоторых направлений)
    #DONE: перенесено в этот дочерний класс 2024-08-30,пт (2024-08-20,вт)
    
    if not self.useSearchGoodDirs : 
      return False
      
    self.NSrchGd += 1

    l1disp = 0
    self.NGdDirs = 0
    searchX = [0.0] * self.dim
    for i in range(0, self.dim):
      searchX[i] = self.X[i] + self.dX_pool[i]
      l1disp += abs(self.dX_pool[i])
      if self.dX_pool[i]>0.0 :
        self.NGdDirs += 1

    if l1disp < self.ss_cur/2 :
      return False # Небыло смещения 
  
    searchFval = self.func(searchX)
    if self.infoLevCoord > 0:
      print(f"!{self.Fval-searchFval:+.1e}", end="; ")
  
    if searchFval < self.Fval:
      self.NSrchGdSc += 1
      self.Fval = searchFval
      self.pathLen += l1disp
      for i in range(0, self.dim):
        self.X[i] = searchX[i]
      return True
    else :
      return False
  # = = = = = searchGoodDirs


  def pollCoordsFinit (self) :
    super().pollCoordsFinit()
    if self.searchGoodDirs() :
      mess = " Successful GD-seach/"+str(self.NGdDirs)
    else :
      mess = " Unsuccessful GD-seach/"+str(self.NGdDirs)

    self.wrt.fInfoPool.write(mess)
    self.wrt.fInfoDir.write(mess)
  # = = = = = pollCoordsFinit/MHJ11_cls


# = = = = = MHJ_cls_11


def trash (self) :
  '''
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
      self.NSrchBd += 1
      self.gridPathLen += l1disp
      for i in range(0, self.dim):
        pX[i] = searchX[i]
    else:
      self.NSrchBdSc += 1
    return
  # = = = = = searchBadDirs
  '''
  """ Свалка отходов

    TODO: перенести в дочерний класс 2024-08-20,вт
    def printFinishInfo 
    if hasattr(self,"searchGoodDirs") :
      self.printParam ("NSrch",pSep="/")
    if hasattr(self,"searchBadDirs")  :
      self.printParam ("NSrchBd",pSep="/")
      self.printParam ("NSrchBdSc",pSep="/")


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
          self.NSrch = 0     # количество поисков по суммам успешных направлений
          self.NSrchSc = 0 # количество Успешных поисков по суммам успешных направлений
        if self.useSearchBadDirs :
          self.NSrchBd= 0      # количество поисков по минус суммам неуспешных направлений
          self.NSrchBdSc = 0 # количество Успешных поисков по минус суммам неуспешных направлений

        # TODO: перенести в дочерний класс 2024-08-20,вт
        def __init__
        # self.useSearchGoodDirs = False
        # self.useSearchBadDirs = False


  """
  pass

# = = = = = trash/MHJ11_cls


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ11_cls

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
    mhj = MHJ11_cls(tsFnRosen, X, pSs_init=0.01, pSs_min=1e-3, pNev_max=1e5, pMinFval=1e-1)
    #mhj11.useBlock = False
    mhj.searchAllGrids()

  print("\n- - - - - Проверка работы модуля завешилась штатно/"+__file__)
