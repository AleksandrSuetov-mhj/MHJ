""" Класс для вывода информации о работе алгоритма MHJ_obj.MHJ00_cls
    дополнительно к информации о базовом классе MHJ_obj.MHJ0_cls
"""

from MHJ_obj.MHJ00_wrt import MHJ00_wrt


class MHJ11_wrt (MHJ00_wrt) :
  """ Класс для вывода в файлы информации о работе алгоритма MHJ_obj.MHJ00_cls
      ***дополнительно*** к информации о базовом классе MHJ_obj.MHJ0_cls
  """

  obj_num = 0
  fn_postfix = "11"
  

  def __init__ (self, pMHJ_obj) :
    super().__init__(pMHJ_obj)  
  # = = = = = __init__/MHJ11_wrt  

  
  def writeInitInfo ( self, pFile  ) :
    """Вывод начальой информации"""

    super().writeInitInfo(pFile)
    self.writeParam( pFile, "useSearchGoodDirs",pSep="/")
  # = = = = = writeInitInfo/MHJ11_wrt


  def writeFinitInfo ( self, pFile  ) :
    """Вывод итоговой информации"""

    super().writeFinitInfo(pFile)
    pFile.write(f"|NSrchGd/Sc={self.mhj.NSrchGd:4}/{self.mhj.NSrchGdSc:4}")
  # = = = = = writeFinitInfo/MHJ11_wrt


  def writeGridInfoTitle ( self, pFile, pPref="" ) :
    super().writeGridInfoTitle(pFile,pPref)
    pFile.write(f"|{'dNSrchGd/Sc':9}")
  # = = = = = writeGridInfoTitle/MHJ11_wrt


  def writeGridInfo ( self, pFile, pPref="" ) :
    """Вывод информации о поиске на сетке"""
    super().writeGridInfo(pFile,pPref)
    pFile.write(f"|dNSrchGd/Sc={self.mhj.NSrchGd-self.mhj.prevNSrchGd:4}")
    pFile.write(f"/{self.mhj.NSrchGdSc-self.mhj.prevNSrchGdSc:4}")
  # = = = = = writeGridInfo/MHJ11_wrt

  
# = = = = = MHJ11_wrt



def trash () :
  """Отходы производства"""


  """ 
    Перенесено из / 2024-  
  """

  pass

# = = = = = trash/MHJ11_wrt



if __name__=="__main__" :
  #python -m MHJ_obj.MHJ11_wrt

  print("\n+ + + + + Модуль "+__file__+" - Проверка работы + + + + +",end="")

  MHJ11_wrt = MHJ11_wrt(None)

  print("\n- - - - - Проверка работы модуля "+__file__+" завешилась штатно - - - - -\n")

# = = = = = if __main__/MHJ11_wrt
