"""Базовый класс для Метода Хука-Дживса, Минимальный жизнеспособный продукт:
     Измельчение сетки; Перебор всех направлений в стандартном порядке;
"""

def comments () :
  """Конструкция для фолдинга комментариев"""
  """
     В производных классах должны быть реализованы методы:

     1. В следующих классах, со стандартным условием измельчения сетки
     1а. Не используем регулирование (увеличение/уменьшение) шага поиска для текущей сетки 
     * Исключая направление, с которого пришли в текущую точку
     * Перебор "перспективных" направлений-по одному (из двух) для каждой координаты (эвристика)
     * Поиск в направлениях суммы успешных направлений и суммы неуспешных направлений 

     1б. Используем регулирование (увеличение/уменьшение) шага поиска для текущей сетки
     * Использование мелкой сетки для регулирования размера шага поиска
     * Коэффициент для шага в условии приемлемости

     2. В классе с обобщённым условием Дискретной Стационарности (ОУДС)
     * 
  """
  pass
  return

# = = = = = comments - Для фолдинга большого блока комментариев

import typing
import math

from MHJ_obj.MHJ0_wrt import MHJ0_wrt
from MHJ_obj.MHJ0_prn import MHJ0_prn


class MHJ0_cls :
  obj_num = 0


  def __initParams(self, pFun:typing.Callable[[list[float]], float], 
                     pX:list[float], pMinFval, pNev_max, 
                     pSs_init, pSs_min, pSs_coef):
    """ Инициализация полей объекта 2024-08-16
        Переделано из MHJ_proc.MHJ_proc 1.initGlobVar()
        pFun = Целевая функция; 
        pX   = Начальное приближение к минимуму
        pNev_max = Максимальное число вычислений функции
        ## Параметры шага сетки
        pSs_init = Начальное значение размера шага сетки
        pSs_min  = Минимальное значение размера шага сетки
        pSs_coef = Коэффициент уменьшения размера шага сетки
        pCoefTolDist = Коэффициент для определения начального  расстояния приемлемости
    """
    #print(pFun,pX,pNev_max)
    self.Func : typing.Callable[[list[float]], float] = pFun # Целевая функция
  
    self.X: list[float] = pX  
    self.dim  = len(pX)  # Размерность задачи
    self.minFval = pMinFval  # Значение, при котором завершается поиск
  
    if pNev_max<0 : 
      self.maxNEv = self.dim*500 # Макс.кол-во вычислений по умолчанию
    else :
      self.maxNEv = pNev_max

    ## Параметры шага сетки
    self.ss_init = pSs_init # Начальное значение размера шага сетки
    self.ss_min  = pSs_min # Минимальное значение размера шага сетки
    self.ss_coef = pSs_coef # Коэффициент уменьшения размера шага сетки
    
  # = = = = = = initParams


  def __initVars (self) :
    """Инициализация переменных метода:
       счётчики: вычислений, попыток, успехов
       и прочее
    """

    self.NEv = 0 # Количество вычислений функции
    self.Fval = self.func(self.X) # Текущее значение целевой функции
    self.prevFval= math.inf   # Предыдущее значение целевой функции

    self.ss_cur  = self.ss_init # Текущее значение размера шага сетки
    self.pathLen = 0 # Длина пути от начальной точки до текущей

    # Счётчики количества вычислений, успехов, "блокировок попыток"
    self.NSc = 0    # количество успехов поиска
    # Приращения счётчиков 
    self.prevNEv = 0    # приращение количества вычислений целевой функции
    self.prevNSc = 0    # приращение количества успехов поиска

    self.numGrid = 0    # номер текущей сетки
    self.numPool = 0    # номер опроса направлений на текущей сетке
  # = = = = = = initVars


  def __init__(self, pFun:typing.Callable[[list[float]], float],
               pX:list[float], pMinFval=-math.inf,
               pNev_max=-1, pSs_init=0.1, pSs_min=0.0001, pSs_coef=2) -> None:
    """ Инициализация полей объекта 2024-08-16"""
    self.__class__.obj_num += 1
    self.name = self.__class__.__name__+"№"+str(MHJ0_cls.obj_num)
    self.__initParams(pFun, pX, pMinFval, pNev_max, pSs_init, pSs_min, pSs_coef)
  
    # Объект для записи информации о ходе и результе процесса
    self.wrt = MHJ0_wrt(self)
    self.prn = MHJ0_prn(self)

    self.__initVars ()
  
    self.pathLen = 0 # длина пути в сетке; 2024-08-03,сб; Используется как полная длина пути
    self.prevPathLen = 0 
  
    self.infoLevMeth = 1 # уровень информирования о результате метода
    self.infoLevGrid = 0 # уровень информирования о результате на сетке
    self.infoLevCoord = 0 # уровень информирования о результате опроса координат
    if self.infoLevCoord > 0:
      self.infoLevGrid = max(1, self.infoLevGrid)

    if self.infoLevGrid > 0:
      self.infoLevMeth = max(1, self.infoLevMeth)

    print(f"\nСоздан объект MHJ0_cls №{MHJ0_cls.obj_num}",end="")
    
  # = = = = = __init__


  def func (self,pX) :
    """Целевая функция для подсчёта числа обращений в методах"""
    self.NEv += 1
    res = (self.Func)(pX)
    return res

  # = = = = = func


  def func2 (self,pX) :
    """Вспомогательная Целевая функция для проверок правильности работы методов""" 
    res = (self.Func)(pX)
    return res
  
  # = = = = = func2
    

  def searchAllGrids (self, pSs_init=-1):
    '''   Метод Хука-Дживса без поиска по образцу (без эвристик) '''
    '''
      ss_init - начальная длина шага (Step Size)
    '''
  
    procName = "MHJ0_cls"
    #self.ss _mult_max = 0
  
    if self.infoLevMeth>0 :
      self.prn.printInitInfo(procName)

    self.wrt.writeInitInfo(self.wrt.fInfoMeth)
    self.wrt.writeInitInfo(self.wrt.fInfoGrid)
    self.wrt.writeInitInfo(self.wrt.fInfoPool)
    self.wrt.writeInitInfo(self.wrt.fInfoDir)

    if pSs_init < 0 :   self.ss_cur = self.ss_init
    else            :   self.ss_cur = pSs_init

    """ см. searchCurGrid
    self.wrt.writeGridInfoTitle(self.wrt.fInfoPool,"g"+str(self.numGrid))
    self.wrt.writeGridInfoTitle(self.wrt.fInfoDir,"g"+str(self.numGrid))
    """
    self.wrt.writeGridInfoTitle(self.wrt.fInfoGrid,"Gs:")

    # Цикл по сеткам с убывающими размерами шагов
    while True : # + + + Цикл уменьшения шага сетки
      self.searchCurGrid()
      if (self.ss_cur <= self.ss_min 
          or self.NEv >= self.maxNEv 
          or self.Fval<=self.minFval) : 
        break  # Достигнут мин. шаг сетки или макс. количество вычислений
      else:    # Уменьшаем шаг сетки
        self.ss_cur = self.ss_cur/self.ss_coef
      # - - - Цикл уменьшения шага сетки
  
    # Вывод итоговой информации
    if self.infoLevMeth>0 :
      self.prn.printFinishInfo(procName)
      
    return 0
    
  # = = = = =  searchAllGrid


  def initSearchGrid (self) :
    self.numGrid += 1
    self.numPool  = 0
    
    # Сохранение данных до поиска
    self.prevNEv = self.NEv
    self.prevNSc = self.NSc
    self.prevFval = self.Fval

    if self.infoLevGrid >0 :
      print("Start searchCurGrid:",'prevFval=',self.prevFval,'ss_cur=',self.ss_cur)

    #self.wrt.write GridInfoTitle(self.wrt.fInfoGrid,"g"+str(self.numGrid)+":")
    #self.wrt.write GridInfoTitle(self.wrt.fInfoPool,"g"+str(self.numGrid)+":")
    #self.wrt.write GridInfoTitle(self.wrt.fInfoDir,"g"+str(self.numGrid)+":")

    return
    
  # = = = = = initSearchGrif

  def isStacPoint (self) :
    """Проверка условия стационарности для текущей точки на текущей сетки"""

    #print("pollCoords: ",end="")
    for iCoord in range (1,self.dim+1) :
      for iDir in [-1,1] :
        if self.isGoodDir00(iCoord*iDir,self.func2) :
          print(f"\nОшибка:Убывание в направлении {iCoord}, {iDir}")

    return

  # = = = = = checkGridSC

  
  def searchCurGrid (self) :
    """ Поиск стационарного узла текущей сетки"""
  
    self.initSearchGrid()
    """ См. конец функции
    self.wrt.writeGridInfo(self.wrt.fInfoPool,"gL1:")
    self.wrt.writePoolInfoTitle()
    """
    
    while True :
      if self.pollCoords() :
        break
      elif self.NEv >= self.maxNEv:
        print("\nДостигнуто ограничение по количеству вычислений",end="")
        break
      elif self.Fval<=self.minFval:
        print("\nДостигнуто ограничение по значению функции",end="")
        break
      elif self.pathLen-self.prevPathLen < self.ss_cur/2 :
        print("\nПроблема:Нет ни стационарности, ни смещения",end="")


    if not (self.NEv >= self.maxNEv or self.Fval<=self.minFval) :
      self.isStacPoint()

    # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
    if self.infoLevGrid >0 :
      print("Finsh searchCurGrid: ",end="")
      print(f"dNEv/dNSc={self.NEv-self.prevNEv}/{self.NSc-self.prevNSc}; ", end="");
      print(f"dFval={self.Fval-self.prevFval}; ", end="")
      print(f"PthLen={self.pathLen}")

    #TODO: finitSearchGrid ???
    infoGridStr = f"g{self.numGrid}:"
    self.wrt.writeGridInfo(self.wrt.fInfoGrid,infoGridStr)
    self.wrt.writeGridInfoTitle(self.wrt.fInfoPool,"Gs:")
    self.wrt.writeGridInfo(self.wrt.fInfoPool,infoGridStr)
    self.wrt.writeGridInfoTitle(self.wrt.fInfoDir,"Gs:")
    self.wrt.writeGridInfo(self.wrt.fInfoDir,infoGridStr)
    return 0
  
  # = = = = = searchCurGrid  
    
  
  def pollCoords (self) :
    """ Цикл по координатам для текущего узла сетки"""
    """ Замечание: возможен вариант с выходом из цикла при первом успехе,
          Но зачем?"""
    isStac= True

    self.numPool += 1

    # Для результатов опроса направлений
    self.prevFval_pool = self.Fval
    self.dX_pool    = [0]*self.dim # Заполняется по результатам исследования направлений

    #print("pollCoords: ",end="")
    for coord in range (1,self.dim+1) :
      # Замечание: можно обойтись одним "if" с ленивым "or"
      if   self.isGoodDirection( coord ) :# Проверяем положительное направление оси
        isStac = False           
      else :
        if self.isGoodDirection(-coord ) :# При неуспеха проверяем отрицательное направление
          isStac = False
     # - - - for

    self.dFval_pool = self.Fval - self.prevFval_pool
    self.wrt.writePoolInfo(self.wrt.fInfoPool)
    self.wrt.writePoolInfo(self.wrt.fInfoDir)
    self.wrt.fInfoDir.write("\n")

    return isStac
    
  # = = = = = pollCoords

    
  def stepSize ( self, pI ) :
    """Текущий размер шага по координате pI;
        В базовом классе не меняется для текущей сетки """
    """В производных класса предполагается изменять"""
    return self.ss_cur

  # = = = = = stepSize


  def isGoodDir00 (self, pI, pFunc ) :
    """ Проверка данного направления (положительного или отрицательного) для данной координаты
        Метод выделен для использования в двух местах: 
          * исследованиия направлений и 
          * проверки стационарности
        Не используются множители для размера шага"""
    """ Метод предполагается неизменным для производных классо"""
    """ abs(pI) - номер координаты, sign(pI) - направление по этой координате
    """

    # Распаковываем номер координаты и индекс направления
    self.curCoord = abs(pI)
    self.curDir =  1 if pI>0 else 0
    self.curInd = abs(pI) - 1 # Индекс варьируемой компоненты

    # Исследуем направление
    oldX = self.X[self.curInd]
    if pI >0 : 
      self.dx = self.stepSize(self.curCoord)
    else     : 
      self.dx = -self.stepSize(self.curCoord)

    self.X[self.curInd] += self.dx
    
    self.newFval = pFunc(self.X)

    # Запоминаем результаты исследования Направления
    self.dFval_dir = self.newFval-self.Fval
    self.dX_dir    = [0]*self.dim
    self.dX_dir[self.curInd] = self.dx

    # Восстанавливаем значение координаты
    self.X[self.curInd] = oldX

    # Результат исследования направления
    return self.newFval < self.Fval 

  # = = = = = isGoogDir00
 
  
  def isGoodDir0 (self, pI ) :
    """ Проверка заданного направления (положительного или отрицательного) для заданной координаты
        Не используются множители для размера шага"""
    """ Метод предполагается неизменным для производных классо"""
    """ abs(pI) - номер координаты, sign(pI) - направление по этой координате
    """

    self.isGoodDir00(pI, self.func)
  
    if self.infoLevCoord :
      print(f"{pI:+}/{self.Fval-self.newFval:+.1e}", end="; ")

    if self.newFval<self.Fval :
      self.X[self.curInd] += self.dx # dx Вычисляется в isGoodDir00
      self.dX_pool[self.curInd] += self.dx
      self.Fval = self.newFval
      self.NSc += 1
      self.pathLen += self.stepSize(self.curCoord)
      res = True
    else :
      res = False

    self.wrt.writeDirInfo(self.wrt.fInfoDir)
    return res  
  # = = = = = isGoogDir0


  def isGoodDirection (self, pI) :
    """ Проверка заданного направления (положительного или отрицательного) для заданной координаты
        Плюс дополнительные действия"""
    """Метод предполагается переопределять в производных классах"""
    """ abs(pI) - номер координаты, sign(pI) - направление по этой координате
    """
    return self.isGoodDir0 ( pI)

  # = = = = = isGoodDirection


# = = = = = MHJ0_cls

def trash () :  
  pass

# = = = = = trash


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ0_cls
  import sys
  from tsFuncs.tsFnRosen import tsFnRosen
  from tsFuncs.tsFnBVP1d import tsFnBVP1d


  print("\n+ + + + + Класс MHJ0_cls - Проверка работы + + + + +")
  X : list[float] = [0]

  def set_X ( pDim ) :
    global X
    X = [1] * pDim
    X[0] = -1

  #curFunc = tsFnBVP1d
  curFunc = tsFnRosen

  locDim = 2
  for i in range(locDim,1+locDim) :
    set_X(i)
    mhj0 = MHJ0_cls(curFunc, X, pSs_init=0.01, pSs_min=1e-11, pNev_max=1e5, pMinFval=1e-11)
    mhj0.searchAllGrids()
  
  sys.exit("Работа модуля MHJ0_cls завешилась штатно")

# = = = = = if __main__
