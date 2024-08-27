"""Функции вывода параметров и результатов поиска"""
import MHJ_proc.MHJ_globVars as gv


def printParam ( pParamName, pFormat="", pSep="; ", pEnd="") :

  gvName = "gv." + pParamName
  temp_str = pParamName+"={0"
  if len(pFormat)>0 :
    temp_str +=":"+pFormat
  temp_str += "}"+pSep

  print(temp_str.format(eval(gvName)), end=pEnd)
  return
# = = = = = printParam


def printInitInfo ( pProcName  ) :  
  """Вывод параметров метода"""
  format1 = ".2e"
  print()
  print(f"+ + + {pProcName}: ",end="")
  printParam ("dim")

  printParam ("Fval",format1)
  #, "Функция: ", gv.Func.__name__)
  printParam ("ss_init",format1)
  printParam ("ss_min",format1)  
  printParam ("ss_сoef",format1)  
  printParam ("ss_mult_max")  
  printParam ("maxNEv")
  printParam ("coefTolDist",format1)
  printParam ("searchGoodDirs")
  printParam ("X")
# = = = = = printInitInfo


def printFinishInfo ( pProcName  ) :
  """Вывод итоговой информации"""

  format1 = ".2e"
  print()
  print(f"- - - {pProcName}: ",end="")

  printParam ("Fval",format1)
  
  #printParam ("ss_cur",format1)
  printParam ("gridPathLen",format1)
  printParam ("NEv",pSep="/")
  printParam ("NSc",pSep="/")
  printParam ("NBlk")
  
  if gv.searchGoodDirs :
    printParam ("NSearch",pSep="/")
  if gv.searchBadDirs :
    printParam ("NSearch2",pSep="/")
    printParam ("NSearch2UnSc",pSep="/")
  #print()
  print ("X="+lstToStr(gv.X,":.1e"),end=" ")
  # = = = = = printFinishInfo


def printGridInfoTitle ( pFile, pPref="" ) :
  pFile.write("\n")
  if len(pPref)>0 : pFile.write(pPref)
  pFile.write(f"{'ss_cur':7} | {'GCSdist':8}|{'dFval':8}|")
  pFile.write(f"{'dNEv':4}/{'dNSc':4}/{'dNbl':4}")
  pFile.write(f"|{'dPLen':8}||")
  pFile.write(f"{'ss_mult'}")
  #pFile.write(f"\n")
# = = = = = printGridInfoTitle


def printGridInfo ( pFile, pPref="" ) :
  pFile.write("\n")
  if len(pPref)>0 : pFile.write(pPref)
  pFile.write(f"{gv.ss_cur:.1e} | {gv.GCSdist:.2e}|{gv.Fval-gv.prevFval:+.1e}")
  pFile.write(f"|{gv.NEv-gv.prevNEv:4}/{gv.NSc-gv.prevNSc:4}/{gv.NBlk-gv.prevNBlk:4}")
  pFile.write(f"|{gv.gridPathLen-gv.prevPathLen:.2e}||")
  # Множители увеличения шага
  for i in range (gv.dim) :
    pFile.write(f"{gv.ss_mult[i]}")
  
  # = = = = = printGridInfo


def printCoordInfoTitle () :
  gv.fInfoCoord.write("\n")
  #gv.fInfoCoord.write(f"{'ss_mult':gv.dim}|")
  gv.fInfoCoord.write(f"{'mult'}")
  for i in range (gv.dim-4) : gv.fInfoCoord.write(" ")
  gv.fInfoCoord.write(f"{'|'}")

  gv.fInfoCoord.write(f"{'dist[dir][coord]'}")
  for i in range(8*2*gv.dim-14) : gv.fInfoCoord.write(" ")

  #gv.fInfoCoord.write("\n")
# = = = = = printCoordInfoTitle


def printCoordInfo () :
  """ Вывод информации о переборе координат и направлений"""

  gv.fInfoCoord.write("\n")
  # Множители увеличения шага
  for i in range (gv.dim) :
    gv.fInfoCoord.write(f"{gv.ss_mult[i]}")
  
  # Расстояния до точек с возрастанием по направлениям  
  gv.fInfoCoord.write("|")
  for iDim in range (gv.dim) :
    for iDir in range (2) :
      gv.fInfoCoord.write(f"{gv.gridPathLen-gv.incDirDist[iDir][iDim]:.1e}")
      if iDir<1 : gv.fInfoCoord.write(" ")
    if iDim<gv.dim-1 : gv.fInfoCoord.write(";")

  #gv.fInfoCoord.write("\n")

# = = = = = printCoordInfo



def lstToStr ( pLst, pFormat="" ) :
  res = "["
  for i in range(len(pLst)) :
    res += ("{0"+pFormat+"}").format(pLst[i])
    if i<len(pLst)-1 : res += " "
  res+="]"
  return res
# = = = = = lstToStr

Test = 0
if Test!=0 :
  import sys
  print(lstToStr([1.1234, 2.2345, 3.3456],":.2e"))
  sys.exit(f"Проверка {__name__} завершилась штатно")

