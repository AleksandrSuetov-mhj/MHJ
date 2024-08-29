"""Класс для вывода информации на экран"""

import sys
from MHJ_obj.MHJ00_wrt import MHJ00_wrt
from MHJ_obj.MHJ00_prn import MHJ00_prn
import MHJ_proc.MHJ_proc2 as proc2


class MHJ01_prn ( MHJ00_prn ):
  """ Класс для вывода на экран информации о работе алгоритма MHJ_obj.MHJ01_cls
      дополнительно к MHJ_obj.MHJ00_cls
  """

  obj_num = 0

  # Ничего дополнительного инициализировать не нужно 2024-08-29,чт
  ''' 
  def __init__ ( self, pMHJ_obj ) :
    super().__init__(pMHJ_obj)

  # = = = = = __init__
  '''

  
  def printFinishInfo ( self ) :
    """Вывод итоговой информации"""
    self.mhj.wrt.writeFinitInfo(sys.stdout)
    
  # = = = = = printFinishInfo
  
  

# = = = = = MHJ01_prn



def trash () :
  """Для отходов производства"""

  
  """
  """

  pass

# = = = = = trash
