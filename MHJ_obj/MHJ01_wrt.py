""" Класс для вывода информации о работе алгоритма MHJ_obj.MHJ00_cls
    дополнительно к информации о базовом классе MHJ_obj.MHJ0_cls
"""

from MHJ_obj.MHJ00_wrt import MHJ00_wrt


class MHJ01_wrt (MHJ00_wrt) :
  """ Класс для вывода в файлы информации о работе алгоритма MHJ_obj.MHJ00_cls
      ***дополнительно*** к информации о базовом классе MHJ_obj.MHJ0_cls
  """

  obj_num = 0
  fn_postfix = "01"
  

  def __init__ (self, pMHJ_obj) :
    super().__init__(pMHJ_obj)  
  # = = = = = __init__/MHJ01_wrt  

  
  def writeInitInfo ( self, pFile  ) :
    """Вывод начальой информации"""

    super().writeInitInfo(pFile)
    self.writeParam( pFile, "useBlock",pSep="/")
  # = = = = = writeInitInfo/MHJ01_wrt


  def writeFinitInfo ( self, pFile  ) :
    """Вывод итоговой информации"""

    super().writeFinitInfo(pFile)
    self.writeParam( pFile, "Nblk",pSep="/")
  # = = = = = writeFinitInfo/MHJ01_wrt


  def writeGridInfoTitle ( self, pFile, pPref="" ) :
    super().writeGridInfoTitle(pFile,pPref)
    pFile.write(f"|{'dNblk':4}")
  # = = = = = writeGridInfoTitle/MHJ01_wrt


  def writeGridInfo ( self, pFile, pPref="" ) :
    """Вывод информации о поиске на сетке"""
    super().writeGridInfo(pFile,pPref)
    pFile.write(f"|{self.mhj.Nblk-self.mhj.prevNblk:4}")
  # = = = = = writeGridInfo/MHJ01_wrt

  
# = = = = = MHJ01_wrt



def trash () :
  """Отходы производства"""


  """ 
    Перенесено из / 2024-  
  """

  pass

# = = = = = trash/MHJ01_wrt



if __name__=="__main__" :
  #python -m MHJ_obj.MHJ01_wrt
  import sys

  print("\n+ + + + + Модуль "+__file__+" - Проверка работы + + + + +",end="")

  MHJ01_wrt = MHJ01_wrt(None)

  sys.exit("\n- - - - - Проверка работы модуля "+__file__+" завешилась штатно - - - - -\n")

# = = = = = if __main__/MHJ01_wrt
