""" Класс для вывода информации о работе алгоритма MHJ_obj.MHJ00_cls
    дополнительно к информации о базовом классе MHJ_obj.MHJ0_cls
"""

from MHJ_obj.MHJ0_wrt import MHJ0_wrt


class MHJ00_wrt (MHJ0_wrt) :
  """ Класс для вывода в файлы информации о работе алгоритма MHJ_obj.MHJ00_cls
      ***дополнительно*** к информации о базовом классе MHJ_obj.MHJ0_cls
  """

  obj_num = 0
  fn_postfix = "00"

  def __init__ (self, pMHJ_obj) :
    super().__init__(pMHJ_obj)

    
  # = = = = = __init__/MHJ00_wrt  

  
  def writeFinitInfo ( self, pFile, pProcName  ) :
    """Вывод итоговой информации"""

    super().writeFinitInfo(pFile, pProcName)
    self.writeParam( pFile, "NBlk",pSep="/")

  # = = = = = writeFinitInfo/MHJ00_wrt

  
  def writeGridInfoTitle ( self, pFile, pPref="" ) :
    super().writeGridInfoTitle(pFile,pPref)
    pFile.write(f"|{'dNblk':4}")

  # = = = = = writeGridInfoTitle/MHJ00_wrt


  def writeGridInfo ( self, pFile, pPref="" ) :
    """Вывод информации о поиске на сетке"""
    super().writeGridInfo(pFile,pPref)
    pFile.write(f"|{self.mhj.NBlk-self.mhj.prevNBlk:4}")

  # = = = = = writeGridInfo/MHJ00_wrt


  def writeDirInfo ( self, pFile ) :
    """ Вывод информации об исследовании направления"""
    if not self.mhj.directionIsBlocked :
      super().writeDirInfo(pFile)
    else :
      pFile.write(f"\ng{self.mhj.numGrid}p{self.mhj.numPool}: Direction is Blocked for pooling")

  # = = = = = writeDirInfo/MHJ00_wrt

# = = = = = MHJ00_wrt



def trash () :
  """Отходы производства"""


  """ 
    Перенесено из / 2024-  
  """

  pass

# = = = = = trash/MHJ00_wrt



if __name__=="__main__" :
  #python -m MHJ_obj.MHJ00_wrt
  import sys

  print("\n+ + + + + Модуль "+__file__+" - Проверка работы + + + + +",end="")

  mhj00_wrt = MHJ00_wrt(None)

  sys.exit("\n- - - - - Проверка работы модуля "+__file__+" завешилась штатно - - - - -\n")

# = = = = = if __main__/MHJ00_wrt
