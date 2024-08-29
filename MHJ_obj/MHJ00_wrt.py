""" Класс для вывода информации о работе базового алгоритма MHJ_obj.MHJ0_cls
"""

import datetime
#from io import FileIO # Зачем это? 2024-08-26
from MHJ_proc.MHJ_proc2 import lstToStr
from MHJ_proc.MHJ_proc2 import lstToStr2


class MHJ00_wrt :
  """ Класс для вывода в файлы информации о работе базового алгоритма MHJ_obj.MHJ0_cls
  """

  obj_num = 0
  fn_postfix = "00"


  def initFiles(self) :
    """Открывает файлы для записи информации о ходе процесса и результатах"""

    #if len(pFNInfoGrid)==0 : 
    #  locFNInfoGrid=self.fnInfoGrid, 

    self.fInfoMeth = open(self.fnInfoMeth, "w")
    self.fInfoMeth.write(datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n")

    self.fInfoGrid = open(self.fnInfoGrid, "w")
    self.fInfoGrid.write(datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n")

    self.fInfoPool = open(self.fnInfoPool, "w")
    self.fInfoPool.write(datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n")

    self.fInfoDir = open(self.fnInfoDir, "w")
    self.fInfoDir.write(datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n")

  # = = = = = initFiles


  def initFileNames (self) :
    """Задаёт имена файлов для записи информации о ходе процесса и результатах"""
    self.dirInfo = "./Output/"
    postfix = self.__class__.fn_postfix
    self.fnInfoMeth = self.dirInfo+"infoMeth"+postfix+".txt"
    self.fnInfoGrid = self.dirInfo+"infoGrid"+postfix+".txt"
    self.fnInfoPool = self.dirInfo+"infoPool"+postfix+".txt"
    self.fnInfoDir  = self.dirInfo+"infoDir"+postfix+".txt"

  # = = = = = initFileNames

  
  def __init__ ( self, pMHJ_obj ) :
    self.mhj = pMHJ_obj
    self.initFileNames()
    self.initFiles()

    self.__class__.obj_num += 1
    print(f"\nСоздан объект {self.__class__.__name__}№{self.__class__.obj_num}", end="")

  # = = = = = __init__


  def writeParam ( self, pFile, pParamName, pFormat="", pSep="; ") :
    """Вывод в файл значения атрибута именем pParamName
        для объекта self.mhj
        по формату pFormat
        с разделителем pSep (может использоваться и как pEnd)
        """

    if not hasattr(self.mhj, pParamName) :
      pFile.write(f"no {pParamName} in {self.mhj.name}"+pSep)

    gvName = "self.mhj." + pParamName
    temp_str = pParamName+"={0"
    if len(pFormat)>0 :
      temp_str +=":"+pFormat
    temp_str += "}"+pSep

    pFile.write(temp_str.format(eval(gvName)))
      
    return
  # = = = = = writeParam

  
  def writeInitInfo ( self, pFile ) :  
    """Вывод параметров метода в файл"""
    format1 = ".2e"
    pFile.write("\n")
    pFile.write(f"+ + + {self.mhj.__class__.__name__}№{self.mhj.__class__.obj_num}: ")

    self.writeParam( pFile,"dim")

    self.writeParam( pFile,"Fval",format1,pSep="/")
    #, "Функция: ", self.Func.__name__)
    pFile.write( "Func="+self.mhj.Func.__name__+"; ")
    self.writeParam( pFile,"ss_init",format1)
    self.writeParam( pFile,"ss_min",format1)  
    self.writeParam( pFile,"ss_coef")  
    self.writeParam( pFile,"minFval",format1)
    self.writeParam( pFile,"maxNEv")
    self.writeParam( pFile,"X")

  # = = = = = writeInitInfo

  
  def writeFinitInfo ( self, pFile  ) :
    """Вывод итоговой информации"""

    format1 = ".2e"
    pFile.write("\n")
    pFile.write(f"- - - {self.mhj.__class__.__name__}: ")

    self.writeParam( pFile, "Fval",format1)

    self.writeParam( pFile, "ss_cur",format1)
    self.writeParam( pFile, "pathLen",format1)
    self.writeParam( pFile, "NEv",pSep="/")
    self.writeParam( pFile, "NSc",pSep="/")

    pFile.write("X="+lstToStr(self.mhj.X,"+.1e")+"; ")
  # = = = = = writeFinitInfo/MHJ00_wrt

  
  def writeGridInfoTitle ( self, pFile, pPref="" ) :
    pFile.write("\n")
    if len(pPref)>0 : pFile.write(pPref)
    pFile.write(f"{'ss_cur':7}|{'dFval':8}|")
    pFile.write(f"{'dNEv':4}/{'dNSc':4}")
    pFile.write(f"|{'dPLen':8}|")
    pFile.write(f"|{'Fval':8}|")

  # = = = = = writeGridInfoTitle/MHJ00_wrt


  def writeGridInfo ( self, pFile, pPref="" ) :
    """Вывод информации о поиске на сетке"""
    pFile.write("\n")
    if len(pPref)>0 : pFile.write(pPref)
    pFile.write(f"{self.mhj.ss_cur:.1e}|{self.mhj.Fval-self.mhj.prevFval:+.1e}")
    pFile.write(f"|{self.mhj.NEv-self.mhj.prevNEv:4}/{self.mhj.NSc-self.mhj.prevNSc:4}")
    pFile.write(f"|{self.mhj.pathLen-self.mhj.prevPathLen:.2e}|")
    pFile.write(f"|{self.mhj.Fval:.2e}|")

  # = = = = = writeGridInfo/MHJ00_wrt


  def writePoolInfoTitle ( self ) :
    self.mhj.fInfoPool.write("\ng_p_:")

  # = = = = = writePoolInfoTitle/MHJ00_wrt


  def writePoolInfo ( self, pFile ) :
    """ Вывод информации о переборе координат и направлений"""

    pFile.write(f"\ng{self.mhj.numGrid}p{self.mhj.numPool}: ")
    pFile.write(f"{self.mhj.Fval-self.mhj.prevFval_pool:+.0e}[")
    pFile.write(lstToStr2(self.mhj.dX_pool," .0e")+"]")
  
  # = = = = = writePoolInfo/MHJ00_wrt


  def writeDirInfoDir ( self, pFile ) :
    """ Вывод направления"""

    pFile.write(f"\np{self.mhj.numPool}d{self.mhj.curCoord}{'+'if self.mhj.curDir==1 else '-'}!")
  # = = = = = writeDirInfo/MHJ00_wrt
  
  def writeDirInfo ( self, pFile ) :
    """ Вывод информации об исследовании направления"""
    self.writeDirInfoDir( pFile )
    pFile.write(f"{self.mhj.dFval_dir:+.0e}[")
    pFile.write(lstToStr2(self.mhj.dX_dir," .0e")+"];")
    if self.mhj.dFval_dir<0 : pFile.write("Success")
  # = = = = = writeDirInfo/MHJ00_wrt
    
# = = = = = MHJ00_wrt


def trash () :
  """Отходы производства"""


  """ Перенесено из writePoolInfoTitle / 2024-08-26  
  # Перенести в класс, использующий множители для шагов поиска
  #self.mhj.fInfoPool.write(f"{'ss_mult':self.mhj.dim}|")
  #self.mhj.fInfoPool.write(f"{'mult'}")
  for i in range (self.mhj.dim-4) : self.mhj.fInfoPool.write(" ")
  self.mhj.fInfoPool.write(f"{'|'}")

  # Перенести в класс, использующий расстояниие приемлемости
  self.mhj.fInfoPool.write(f"{'dist[dir][coord]'}")
  for i in range(8*2*self.mhj.dim-14) : self.mhj.fInfoPool.write(" ")
  """

  pass

# = = = = = trash


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ00_wrt
  import sys

  print("\n+ + + + + Модуль "+__file__+" - Проверка работы + + + + +",end="")

  mhj00_wrt = MHJ00_wrt(None)

  sys.exit("\n- - - - - Проверка работы модуля "+__file__+" завешилась штатно - - - - -\n")

# = = = = = if __main__/MHJ00_wrt

