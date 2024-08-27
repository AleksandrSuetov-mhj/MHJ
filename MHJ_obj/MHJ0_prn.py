"""Класс для вывода информации на экран"""

import sys
#from MHJ_obj.MHJ0_wrt import MHJ0_wrt
import MHJ_proc.MHJ_proc2 as proc2


class MHJ0_prn :
  """ Класс для вывода на экран информации о работе базового алгоритма MHJ_obj.MHJ0_cls
  """

  obj_num = 0


  def __init__ ( self, pMHJ_obj ) :
    self.mhj = pMHJ_obj

    MHJ0_prn.obj_num += 1
    print(f"\nСоздан объект MHJ0_prn №{MHJ0_prn.obj_num}", end="")

  # = = = = = __init__


  def printParam ( self, pParamName, pFormat="", pSep="; ", pEnd="") :
    """Вывод одного параметра - атрибута объ"""
    self.mhj.wrt.writeParam(sys.stdout, pParamName, pFormat, pSep, pEnd)
    return
  # = = = = = printParam
  
  
  def printInitInfo ( self, pProcName="" ) :  
    """Вывод параметров метода"""
    self.mhj.wrt.writeInitInfo(sys.stdout, pProcName)

  # = = = = = printInitInfo
  
  
  def printFinishInfo ( self, pProcName="" ) :
    """Вывод итоговой информации"""
    self.mhj.wrt.writeFinitInfo(sys.stdout, pProcName)
    
  # = = = = = printFinishInfo
  
  

# = = = = = MHJ0_prn



def trash () :
  """Для отходов производства"""

  
  """  Перенесено из printInitInfo  2024-08-27  
    format1 = ".2e"
    print()
    print(f"+ + + {pProcName} MHJ_obj/объект №{self.mhj.__class__.obj_num}: ",end="")

    self.printParam ("dim")

    self.printParam ("Fval",format1)
    #, "Функция: ", self.Func.__name__)
    self.printParam ("ss_init",format1)
    self.printParam ("ss_min",format1)  
    self.printParam ("ss_coef")  
    self.printParam ("minFval",format1)
    self.printParam ("maxNEv")
    self.printParam ("X")
  """

  """  Перенесено из printFinitInfo  2024-08-27
    format1 = ".2e"
    print()
    print(f"- - - {pProcName}: ",end="")
  
    self.printParam ("Fval",format1)
  
    self.printParam ("ss_cur",format1)
    self.printParam ("pathLen",format1)
    self.printParam ("NEv",pSep="/")
    self.printParam ("NSc",pSep="/")
  
    #print()
    print ("X="+proc2.lstToStr(self.mhj.X,"+.1e"),end=" ")
  
    print()
  """

  """Перенесено из printInitInfo  2024-08-27
  """

  pass

# = = = = = trash
