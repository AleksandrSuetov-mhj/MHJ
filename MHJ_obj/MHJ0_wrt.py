""" Класс для вывода информации о работе базового алгоритма MHJ_obj.MHJ0_cls
"""

import datetime
#from io import FileIO # Зачем это? 2024-08-26
from MHJ_proc.MHJ_proc2 import lstToStr


class MHJ0_wrt :
  """ Класс для вывода в файлы информации о работе базового алгоритма MHJ_obj.MHJ0_cls
  """

  obj_num = 0


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
    self.fnInfoMeth = self.dirInfo+"infoMeth0.txt"
    self.fnInfoGrid = self.dirInfo+"infoGrid0.txt"
    self.fnInfoPool = self.dirInfo+"infoPool0.txt"
    self.fnInfoDir  = self.dirInfo+"infoDir0.txt"

  # = = = = = initFileNames

  
  def __init__ ( self, pMHJ_obj ) :
    self.mhj = pMHJ_obj
    self.initFileNames()
    self.initFiles()


    MHJ0_wrt.obj_num += 1
    print(f"\nСоздан объект MHJ0_wrt №{MHJ0_wrt.obj_num}", end="")

  # = = = = = __init__


  def writeParam ( self, pFile, pParamName, pFormat="", pSep="; ", pEnd="") :
    """Вывод в файл атрибута с именем pParamName по формату pFormat
        для объекта self.mhj"""

    if not hasattr(self.mhj, pParamName) :
      pFile.write(f"no {pParamName} in {self.mhj.name}"+pEnd)

    gvName = "self.mhj." + pParamName
    temp_str = pParamName+"={0"
    if len(pFormat)>0 :
      temp_str +=":"+pFormat
    temp_str += "}"+pSep

    pFile.write(temp_str.format(eval(gvName))+pEnd)
      
    return
  # = = = = = printParam


  
  def writeInitInfo ( self, pFile ) :  
    """Вывод параметров метода в файл"""
    format1 = ".2e"
    pFile.write("\n")
    pFile.write(f"+ + + MHJ_obj/объект №{self.mhj.__class__.obj_num}: ",end="")

    self.writeParam( pFile,"dim")

    self.writeParam( pFile,"Fval",format1)
    #, "Функция: ", self.Func.__name__)
    self.writeParam( pFile,"ss_init",format1)
    self.writeParam( pFile,"ss_min",format1)  
    self.writeParam( pFile,"ss_coef")  
    self.writeParam( pFile,"minFval",format1)
    self.writeParam( pFile,"maxNEv")
    self.writeParam( pFile,"X")

  # = = = = = writeInitInfo

  
  def writeFinitInfo ( self, pFile, pProcName  ) :
    """Вывод итоговой информации"""

    format1 = ".2e"
    pFile.write("\n")
    pFile.write(f"- - - {pProcName}: ",end="")

    self.writeParam( pFile, ("Fval",format1)

    self.writeParam( pFile, ("ss_cur",format1)
    self.writeParam( pFile, ("pathLen",format1)
    self.writeParam( pFile, ("NEv",pSep="/")
    self.writeParam( pFile, ("NSc",pSep="/")

  
    print ("X="+proc2.lstToStr(self.mhj.X,"+.1e"),end=" ")

    pFile.write()

  # = = = = = writeFinishInfo


  
  def writeGridInfoTitle ( self, pFile, pPref="" ) :
    pFile.write("\n")
    if len(pPref)>0 : pFile.write(pPref)
    pFile.write(f"{'ss_cur':7}|{'dFval':8}|")
    pFile.write(f"{'dNEv':4}/{'dNSc':4}")
    pFile.write(f"|{'dPLen':8}||")
    #pFile.write(f"\n")

  # = = = = = writeGridInfoTitle


  def writeGridInfo ( self, pFile, pPref="" ) :
    """Вывод информации о поиске на сетке"""
    pFile.write("\n")
    if len(pPref)>0 : pFile.write(pPref)
    pFile.write(f"{self.mhj.ss_cur:.1e}|{self.mhj.Fval-self.mhj.prevFval:+.1e}")
    pFile.write(f"|{self.mhj.NEv-self.mhj.prevNEv:4}/{self.mhj.NSc-self.mhj.prevNSc:4}")
    pFile.write(f"|{self.mhj.pathLen-self.mhj.prevPathLen:.2e}||")

  # = = = = = writeGridInfo


  def writePoolInfoTitle ( self ) :
    self.mhj.fInfoPool.write("\ng_p_:")

  # = = = = = writePoolInfoTitle


  def writePoolInfo ( self, pFile ) :
    """ Вывод информации о переборе координат и направлений"""

    pFile.write(f"\ng{self.mhj.numGrid}p{self.mhj.numPool}: ")
    pFile.write(f"{self.mhj.dFval_pool:+.0e}[")
    pFile.write(lstToStr(self.mhj.dX_pool," .0e")+"]")
  
  # = = = = = writePoolInfo


  def writeDirInfo ( self, pFile ) :
    """ Вывод информации об исследовании направления"""

    pFile.write(f"\np{self.mhj.numPool}d{self.mhj.curCoord}{'+'if self.mhj.curDir==1 else '-'}!")
    pFile.write(f"{self.mhj.dFval_dir:+.0e}[")
    pFile.write(lstToStr(self.mhj.dX_dir,"+.0e")+"]")

  # = = = = = writePoolInfo

# = = = = = MHJ0_wrt



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


