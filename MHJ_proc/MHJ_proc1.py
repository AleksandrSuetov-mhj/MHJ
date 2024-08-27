"""Общие функции для методов прямого поиска"""
import datetime

import MHJ_proc.MHJ_globVars as gv
import MHJ_proc.MHJ_print1 as print1


def searchGoodDirs(pX, prevX):
  """Поиск в направлении суммарного смещения 2024-08-01"""
  if not gv.useSearchGoodDirs: return
  searchX = [0] * gv.dim
  l1disp = 0
  for i in range(0, gv.dim):
    dx = pX[i] - prevX[i]
    l1disp += abs(dx)
    searchX[i] = 2 * pX[i] - prevX[i]

  searchFval = gv.func(searchX)
  if gv.infoLevCoord > 0:
    print(f"!{gv.Fval-searchFval:+.1e}", end="; ")

  if searchFval < gv.Fval:
    gv.Fval = searchFval
    gv.NSearch += 1
    gv.gridPathLen += l1disp
    for i in range(0, gv.dim):
      pX[i] = searchX[i]
  else:
    gv.NSearchUnSc += 1
  return
# = = = = = searchGoodDirs


def searchBadDirs(pX, prevX, prevPathLen, ss_cur):
  """Поиск в направлении суммы неуспешных направлений 2024-08-01"""
  searchX = [0] * gv.dim
  l1disp = 0
  numBadDirs = 0
  for iCoord in range(0, gv.dim):
    for iDir in range(0, 2):
      # Проверка пригодности направления возрастания для поиска:
      # Данное направление проверялось и оказалось возрастающим
      if (gv.incDirDist[iDir][iCoord] > prevPathLen and
          # Противополжное направление не проверялось, т.к. недалеко обнруживалось возрастание
          prevPathLen - gv.incDirDist[1 - iDir][iCoord] < gv.GCSdist):
        numBadDirs += 1
        dx = -ss_cur if iDir == 1 else ss_cur  # сдвиг в направлении, противоположном возрастанию
        l1disp += abs(dx)
        searchX[iDir] = pX[iDir] + dx
        # - - - if
      # - - - for iDir
    # - - - for iCoord

  if numBadDirs == 0:
    return

  searchFval = gv.func(searchX)
  if searchFval < gv.Fval:
    gv.Fval = searchFval
    gv.NSearch2 += 1
    gv.gridPathLen += l1disp
    for i in range(0, gv.dim):
      pX[i] = searchX[i]
  else:
    gv.NSearch2UnSc += 1
  return
# = = = = = searchBadDirs


def initFiles(pFNInfoGrid=gv.fnInfoGrid, pFNInfoCoord=gv.fnInfoCoord):
  #finitFiles()
  gv.fInfoGrid = open(pFNInfoGrid, "w")
  gv.fInfoGrid.write(datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс") +
                     "\n")

  gv.fInfoCoord = open(pFNInfoCoord, "w")
  gv.fInfoCoord.write(
      datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс") + "\n")


# = = = = = initFiles


def finitFiles():
  if gv.fInfoGrid is not None: gv.fInfoGrid.close()
  if gv.fInfoCoord is not None: gv.fInfoCoord.close()
# = = = = = finitFiles


def initGlobVars(pX, pFun, nev_max, ss_init, ss_min, ss_сoef, pCoefTolDist=-1):
  """Инициализация глобальных переменных 2024-08-01"""
  """
  gv.fInfoGrid = open(gv.fnInfoGrid, "w")
  gv.fInfoGrid.write( datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n" ) 

  gv.fInfoCoord = open(gv.fnInfoCoord, "w")
  gv.fInfoCoord.write( datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс")+"\n" ) 
  """

  gv.ss_mult_max = max(1, gv.ss_mult_max)  # Не д.б. меньше 1
  gv.Func = pFun
  gv.X = pX
  gv.Fval = gv.Func(pX)
  gv.dim = len(pX)
  gv.maxNEv = nev_max
  gv.ss_init = ss_init
  gv.ss_min = ss_min
  gv.ss_сoef = ss_сoef
  gv.coefTolDist = pCoefTolDist

  gv.incDirDist = [[-0.1] * gv.dim, [-0.1] * gv.dim]

  if gv.infoLevCoord > 0:
    gv.infoLevGrid = max(1, gv.infoLevGrid)

  if gv.infoLevGrid > 0:
    gv.infoLevMeth = max(1, gv.infoLevMeth)

  gv.NEv = 0
  gv.NSc = 0
  gv.NBlk = 0
  gv.prevNEv = 0
  gv.prevNSc = 0
  gv.prevNBlk = 0
  gv.NSearch = 0
  gv.NSearchUnSc = 0
  gv.NSearch2 = 0
  gv.NSearch2UnSc = 0
  #gv.totalPathLen = None
  
  gv.gridPathLen = 0
# = = = = = = initGlobVars


def initSearchGrid():
  print1.printCoordInfoTitle()
  # Сохранение данных до опроса направлений
  gv.prevNEv = gv.NEv
  gv.prevNSc = gv.NSc
  gv.prevNBlk = gv.NBlk
  gv.prevFval = gv.Fval
  gv.prevPathLen = gv.gridPathLen
  #prevX = gv.pX.copy()

  if gv.infoLevGrid > 0:
    print("\n+++grid:",
          f'prevFval={gv.prevFval:.2e}, ss_cur={gv.ss_cur:.1e}',
          end="")
    print(f', GCSdist={gv.GCSdist:.2e}', end="")

  if gv.infoLevCoord > 0: print("||", end="")
# = = = = = initSearchGrid


def finitSearchGrid():
  checkGSC()
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if gv.infoLevGrid > 0:
    print("\n---grid: ", end="")
    print(
        f"dNEv/dNSc/dNBlk={gv.NEv-gv.prevNEv}/{gv.NSc-gv.prevNSc}/{gv.NBlk-gv.prevNBlk}",
        end="")
    print(f"; dFval={gv.Fval-gv.prevFval:+.1e}; ", end="")
    print(f"dPthLen={gv.gridPathLen-gv.prevPathLen:.2e}")  #,end="")
    #print(gv.incDirDist) # отладка

  print1.printGridInfo(gv.fInfoGrid)
# = = = = = finitSearchGrid


def findDirMaxDist():
  """Ищем индексы минимального элемента массива incDirDist (2024-08-13)
     Это направление, для которого точка с условием стационарности наиболее далека от текущей """

  iCoordMax0 = gv.incDirDist[0].index(min(gv.incDirDist[0]))
  iCoordMax1 = gv.incDirDist[1].index(min(gv.incDirDist[1]))
  if gv.incDirDist[0][iCoordMax0] < gv.incDirDist[1][iCoordMax1]:
    iDirMax = 0
    iCoordMax = iCoordMax0
  else:
    iDirMax = 1
    iCoordMax = iCoordMax1

  return iDirMax, iCoordMax, gv.gridPathLen - gv.incDirDist[iDirMax][iCoordMax]
# = = = = = findDirMaxDist


def incSSmult(pI):
  """ Увеличение множителя для размера шага сетки 2024-08-02"""
  gv.ss_mult[pI] = min(gv.ss_mult[pI] + 1, gv.ss_mult_max)
  return


def decSSmult(pI):
  """ Уменьшение множителя для размера шага сетки 2024-08-02"""
  gv.ss_mult[pI] = max(gv.ss_mult[pI] // 2, 1)
  return


def checkGSC():
  """ Проверка выполнения ОУС после поиска по сетке 2024-08-12"""
  
  if gv.NEv>=gv.maxNEv : # Процесс завершился принудительно, 
    return               # проверка штатного условия завершения бессмыслена

  isFirst = True
  for iCoord in range(0, gv.dim):
    for iDir in range(0, 2):
      distSC = gv.gridPathLen - gv.incDirDist[iDir][iCoord]
      if distSC > gv.GCSdist:
        if isFirst:
          isFirst = False
          print(f"\n!!!Нет условия приемлемости ({gv.ss_cur:.1e})", end=":")

        print(
            f"{iCoord} {iDir}; {gv.gridPathLen:.1e}-{gv.incDirDist[iDir][iCoord]:.1e}={distSC:.2e}>{gv.GCSdist:.2e}",
            end=" // ")
  # - - - for iCoord, iDir
  return


# = = = = = = checkGSC

# Отладка
"""
import sys

initFiles("infGridKL1.txt","infCoorKL1.txt")
finitFiles()
sys.exit(f"Эксперимент {__name__} завершен штатно")
"""
