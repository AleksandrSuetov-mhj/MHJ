"""Класс для вывода информации на экран"""

import sys
#from MHJ_obj.MHJ00_wrt import MHJ00_wrt
import MHJ_proc.MHJ_proc2 as proc2


class MHJ00_prn :
  """ Класс для вывода на экран информации о работе базового алгоритма MHJ_obj.MHJ00_cls
  """

  obj_num = 0


  def __init__ ( self, pMHJ_obj ) :
    self.mhj = pMHJ_obj

    self.__class__.obj_num += 1
    print(f"\nСоздан объект {self.__class__.__name__}№{self.__class__.obj_num}", end="")

  # = = = = = __init__


  def printParam ( self, pParamName, pFormat="", pSep="; ", pEnd="") :
    """Вывод одного параметра - атрибута объ"""
    self.mhj.wrt.writeParam(sys.stdout, pParamName, pFormat, pSep, pEnd)
    return
  # = = = = = printParam
  
  
  def printInitInfo ( self ) :  
    """Вывод параметров метода"""
    self.mhj.wrt.writeInitInfo(sys.stdout)

  # = = = = = printInitInfo
  
  
  def printFinishInfo ( self ) :
    """Вывод итоговой информации"""
    self.mhj.wrt.writeFinitInfo(sys.stdout)
    
  # = = = = = printFinishInfo
  
  

# = = = = = MHJ00_prn



def trash () :
  """Для отходов производства"""

  
  """  Перенесено из printInitInfo  2024-08-27  
    format1 = ".2e"
    print()
    print(f"+ + + {pProc Name} MHJ_obj/объект №{self.mhj.__class__.obj_num}: ",end="")

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
    print(f"- - - {pProc Name}: ",end="")
  
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


if __name__=="__main__" :
  #python -m MHJ_obj.MHJ00_prn
  import sys

  print("\n+ + + + + Модуль "+__file__+" - Проверка работы + + + + +",end="")

  mhj00_wrt = MHJ00_prn(None)

  sys.exit("\n- - - - - Проверка работы модуля "+__file__+" завешилась штатно - - - - -\n")

# = = = = = if __main__/MHJ00_prn

