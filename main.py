#import experims.exPrint2file
#import experims.exDateTimeNow

import MHJ_proc.MHJ_globVars as gv
import MHJ_proc.MHJ_kl_0 as mk0
import MHJ_proc.MHJ_kl_1 as mk1
import MHJ_proc.MHJ_kl_2 as mk2
from MHJ_proc.MHJ_GS_1 import MHJ_GS_1 as mhj_gs_1
from tsFuncs.tsFnRosen import tsFnRosen
from tsFuncs.tsFnBVP1d import tsFnBVP1d

ts_ss_init = 0.4
ts_ss_min = 2e-1
ts_coefTolDist = 2
ts_N = 2

gv.infoLevGrid = 0
gv.infoLevCoord = 0

tsFn = tsFnRosen

def ts0 (pN) :
  X=[1]*pN
  X[0]=-1
  mk0.HJM_0(tsFn,X,nev_max=100000, ss_min=ts_ss_min, ss_init=ts_ss_init)
# = = = = = ts0


def ts1 (pN, ss_init=ts_ss_init, ss_min=ts_ss_min) :
  X=[1]*pN
  X[0]=-1
  mk1.HJM_1(tsFn,X,nev_max=100000, ss_min=ss_min, ss_init=ss_init)
# = = = = = ts1

def ts1_2 (pN, ss_init=ts_ss_init, ss_min=ts_ss_min) :
  X=[1]*pN
  X[0]=-1
  mk2.HJM_2(tsFn,X,nev_max=500*pN, ss_min=ss_min, ss_init=ss_init)
# = = = = = ts1

def ts2 (pN, ss_init=ts_ss_init, ss_min=ts_ss_min, pCoefTolDist=ts_coefTolDist) :
  X=[1]*pN
  X[0]=-1
  mhj_gs_1(tsFn,X,nev_max=500*pN, ss_min=ss_min, pCoefTolDist=pCoefTolDist, ss_init=ss_init)
# = = = = = ts1

def ts_cmp () :
  """Сравнение навороченного классического и обобщённого методов:
   оба должны давать одинаковые результаты при расстоянии приемлемости==0
  """
  gv.infoLevMeth = 1  
  gv.infoLevGrid = 0
  gv.infoLevCoord= 0
  gv.ss_mult_max = 2
  ts1(1)
  print()
  ts2(1)
  print(); print()
  global ts_ss_min
  ts_ss_min = 1e-4
  ts1(2)
  print()
  ts2(2)
  print(); print()
  ts1(3)
  print()
  ts2(3)
  print(); print()
# = = = = = ts_cmp

def ts_20240806 ( pDim = 2, pFunc=tsFnRosen ) :
  print("\n\n+ + + ts_20240806 + + +")
  global tsFn
  tsFn = pFunc
  gv.infoLevMeth = 1
  gv.infoLevGrid = 0
  gv.infoLevCoord = 0
  gv.searchGoodDirs = False
  #ts_cmp()
  gv.ss_mult_max = 2
  gv.ss_mult_init= min(2,gv.ss_mult_max)
  #gv.useSearchGoodDirs = True
  ts_ss_init = 4e-3
  ts_ss_min = 1e-4
  ts_coefTolDist = 0.5/pDim #Добавить в глобальные переменные 2024-08-08
  #ts_coefTolDist_min = 2  #Добавить в глобальные переменные 2024-08-08
  
  ts1_2(pDim,ss_init=ts_ss_init, ss_min=ts_ss_min)
  gv.ss_mult_init= min(2,gv.ss_mult_max)
  ts2(pDim,ss_init=ts_ss_init, ss_min=ts_ss_min, pCoefTolDist=ts_coefTolDist*gv.ss_mult_init)
  #ts2(2,ss_init=1e-2,ss_min=1e-3)
# = = = = = ts_20240806

  
ts_20240806 (2,tsFnBVP1d)
ts_20240806 (3,tsFnBVP1d)
ts_20240806 (24,tsFnBVP1d)

'''
ts2(ts_N)

print()

#gv.ss_mult_max = 1
ts1(ts_N)
ts0(ts_N)



# ts
# print1.printParam("infoLevCoord")


python -m test_MHJ.test_dimN

'''