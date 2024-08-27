"""Тестирование в одномерном пространстве"""
import unittest

import globVars as gv
import MHJ_kl_0 as mk0
import MHJ_kl_1 as mk1
import MHJ_kl_2 as mk2
from MHJ_GS_1 import MHJ_GS_1 as mhj_gs_1
from tsFuncs.tsFnRosen import tsFnRosen


class Test_my(unittest.TestCase):
  def myAssertEqual (self, pVal1, pVal2, pMess) :
    """ Имена сравниваемых переменных передаём один раз в виде строк,  
        Каждое используется трижды
    """
    val1=eval("self."+pVal1)
    val2=eval("self."+pVal2)
    self.assertEqual(val1,val2,f"{pMess} {pVal1}={val1}, {pVal2}={val2}")
    # = = = = = myAssertEqual


class Test_dim1(Test_my):

  def test_dim1_1 (self) :
    """Сравнение вариантов МХД:  базового, навороченного и обобщённого с постоянным шагом поиска 
      в одномерном пространстве;
      результаты должны совпадать
    """
    gv.infoLevGrid = 0
    gv.infoLevCoord= 0
    gv.ss_mult_max = 1
    test_ss_init = 0.4
    test_ss_min = 2e-1
    test_coef = 0
    

    print("Одномерная минимизация")
    print("Сравнение базового МХД и навороченного с ВЫКЛюченными наворотами")
    gv.infoLevMeth=1
    X=[-1]
    gv.useSearchGoodDirs = False
    mk0.HJM_0(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    NEv_0 = gv.NEv
    NSc_0 = gv.NSc

    X=[-1]

    mk1.HJM_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    NEv_1 = gv.NEv
    NSc_1 = gv.NSc
    self.assertEqual(NEv_0,NEv_1,f"Количество вычислений должно совпадать, но не совпадает: NEv_0={NEv_0}, NEv_1={NEv_1}")
    self.assertEqual(NSc_0,NSc_1,f"Количество Успехов должно совпадать, но не совпадает: NSc_0={NSc_0}, NSc_1={NSc_1}" )

    print("\nСравнение навороченного МХД и обобщённого с ВЫКЛюченными наворотами")
    # NEv_1 и NSc_1 определены выше
    X=[-1]
    mhj_gs_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    NEv_2 = gv.NEv
    NSc_2 = gv.NSc
    self.assertEqual(NEv_1,NEv_2,f"Количество Вычислений должно совпадать, но не совпадает: NEv_1={NEv_1}, NEv_1={NEv_2}" )
    self.assertEqual(NSc_1,NSc_2,f"Количество Успехов должно совпадать, но не совпадает: NSc_1={NSc_1}, NSc_2={NSc_2}" )

    
    print("\nСравнение навороченного МХД и обобщённого с шагами по суммарному направлению")
    gv.useSearchGoodDirs = True
    X=[-1]
    mk1.HJM_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_2_1 = gv.NEv
    self.NSc_2_1 = gv.NSc
  
    X=[-1]
    mhj_gs_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_2_2 = gv.NEv
    self.NSc_2_2 = gv.NSc
    self.myAssertEqual("NEv_2_1","NEv_2_2","Количество Вычислений должно совпадать, но не совпадает:")
    self.myAssertEqual("NSc_2_1","NSc_2_2","Количество Успехов должно совпадать, но не совпадает:")
  # = = = = = test_dim1_1


  def test_dim1_2 (self) :
    """Сравнение вариантов МХД:  классического и обобщённого с переменным шагом поиска 
      (+поиск по суммам успешных направлений)
      в Одномерном пространстве; результаты должны совпадать
    """
    gv.infoLevGrid = 0
    gv.infoLevCoord= 0
    gv.ss_mult_max = 1
    test_ss_init = 0.4
    test_ss_min = 2e-1
    test_coef = 0
  

    gv.useSearchGoodDirs = True
    gv.infoLevMeth=0

    print("\nОдномерная минимизация- классический МХД c переменным и постоянным шагом поиска")
    X=[-1] 
    print("\nСравнение классических МХД для постоянного и переменного шага")
    mk1.HJM_1(tsFnRosen, X, nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_1 = gv.NEv
    self.NSc_1 = gv.NSc
    X=[-1]
    gv.ss_mult_max = 1
    gv.ss_mult_init = 1
    mk2.HJM_2(tsFnRosen, X, nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_2 = gv.NEv
    self.NSc_2 = gv.NSc
    self.myAssertEqual("NEv_1","NEv_2","Количество вычислений должно совпадать, но не совпадает: ")
    self.myAssertEqual("NSc_1","NSc_2","Количество Успехов должно совпадать, но не совпадает: " )

    #gv.infoLevMeth = 1
    #gv.infoLevCoord= 1
    print("\nСравнение классического МХД и обобщённого с Переменным шагом поиска")
    X=[-1]
    gv.ss_mult_max = 2
    gv.ss_mult_init = 2
    mk2.HJM_2(tsFnRosen, X, nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_3 = gv.NEv
    self.NSc_3 = gv.NSc

    X=[-1]
    mhj_gs_1(tsFnRosen,X,nev_max=100000, ss_min=test_ss_min, ss_init=test_ss_init)
    self.NEv_4 = gv.NEv
    self.NSc_4 = gv.NSc
    self.myAssertEqual("NEv_3","NEv_4","Количество вычислений должно совпадать, но не совпадает: ")
    self.myAssertEqual("NSc_3","NSc_4","Количество Успехов должно совпадать, но не совпадает: " )
  
  # = = = = = test_dim1_2
  
# = = = = = Test_dim1

if __name__ == '__main__':
    unittest.main()