"""Тестирование в одномерном пространстве"""
import unittest

import globVars as gv
import MHJ_kl_0 as mk0
import MHJ_kl_1 as mk1
#import MHJ_print1 as print1
import test_MHJ.test_dim1
from MHJ_GS_1 import MHJ_GS_1 as mhj_gs_1
from tsFuncs.tsFnRosen import tsFnRosen


class Test_dimN(test_MHJ.test_dim1.Test_my):
   

  def test_dimN (self) :
    """Сравнение вариантов МХД:  базового, навороченного и обобщённого 
      для размерностей > 1;
      результаты должны совпадать
    """
    gv.infoLevGrid = 0
    gv.infoLevCoord= 0
    gv.ss_mult_max = 1
    test_ss_init = 1e-2
    test_ss_min = 1e-3
    test_coef = 0
    
    gv.infoLevMeth = 1
    print("\nДвумерная минимизация",end="")
    print("\nСравнение базового МХД и навороченного с ВЫКЛюченными наворотами",end="")
    X=[-1,1]
    #gv.infoLevGrid=1
    gv.useSearchGoodDirs = False
    mk0.HJM_0(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_0 = gv.NEv
    self.NSc_0 = gv.NSc

    X=[-1,1]
    #gv.infoLevCoord = 1
    #gv.infoLevMeth = 1
    mk1.HJM_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_1 = gv.NEv
    self.NSc_1 = gv.NSc
    self.myAssertEqual("NEv_0","NEv_1","Количество вычислений должно совпадать, но не совпадает: ")
    self.myAssertEqual("NSc_0","NSc_1","Количество Успехов должно совпадать, но не совпадает: " )

    print("\nСравнение навороченного МХД и обобщённого с ВЫКЛюченными наворотами",end="")
    # NEv_1 и NSc_1 определены выше
    #gv.infoLevCoord = 1
    X=[-1,1]
    mhj_gs_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init,pCoefTolDist=0)
    self.NEv_2 = gv.NEv
    self.NSc_2 = gv.NSc
    self.myAssertEqual("NEv_1","NEv_2","Количество Вычислений должно совпадать, но не совпадает:" )
    self.myAssertEqual("NSc_1","NSc_2","Количество Успехов должно совпадать, но не совпадает:" )

    
    print("\nСравнение навороченного МХД и обобщённого с шагами по суммарному направлению",end="")
    gv.useSearchGoodDirs = True
    X=[-1,1]
    mk1.HJM_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_2_1 = gv.NEv
    self.NSc_2_1 = gv.NSc

    X=[-1,1]
    mhj_gs_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_2_2 = gv.NEv
    self.NSc_2_2 = gv.NSc
    self.myAssertEqual("NEv_2_1","NEv_2_2","Количество Вычислений должно совпадать, но не совпадает:")
    self.myAssertEqual("NSc_2_1","NSc_2_2","Количество Успехов должно совпадать, но не совпадает:")

if __name__ == '__main__':
    unittest.main()