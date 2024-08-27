"""Общие функции для методов прямого поиска"""
import datetime

import globVars as gv
import MHJ_print1 as print1

## Параметры расстояния приемлемости
self.coefTolDist = 0
self.GCSdist = 0     # приемл.расст. для Обобщённого Условия Дискретной Стационарности (ОУДС)
self.GCSdist_min = 0 # минимально допустимое приемлемое расстояние для ОУДС

self.incDirDist = [[],[]] # расстояние до точки с возрастанием по направлению
self.decDirDist = [[],[]] # расстояние до точки с убыванием по направлению







def finitFiles():
  if self.fInfoGrid is not None: self.fInfoGrid.close()
  if self.fInfoCoord is not None: self.fInfoCoord.close()
# = = = = = finitFiles


def initSearchGrid():
  print1.printCoordInfoTitle()
  # Сохранение данных до опроса направлений
  self.prevNEv = self.NEv
  self.prevNSc = self.NSc
  self.prevNBlk = self.NBlk
  self.prevFval = self.Fval
  self.prevPathLen = self.gridPathLen
  #prevX = self.pX.copy()

  if self.infoLevGrid > 0:
    print("\n+++grid:",
          f'prevFval={self.prevFval:.2e}, ss_cur={self.ss_cur:.1e}',
          end="")
    print(f', GCSdist={self.GCSdist:.2e}', end="")

  if self.infoLevCoord > 0: print("||", end="")
# = = = = = initSearchGrid


def finitSearchGrid():
  checkGSC()
  # Вывод инфо о поиске на текущей сетке: шаг, уменьшение функции, смещение приближения
  if self.infoLevGrid > 0:
    print("\n---grid: ", end="")
    print(
        f"dNEv/dNSc/dNBlk={self.NEv-self.prevNEv}/{self.NSc-self.prevNSc}/{self.NBlk-self.prevNBlk}",
        end="")
    print(f"; dFval={self.Fval-self.prevFval:+.1e}; ", end="")
    print(f"dPthLen={self.gridPathLen-self.prevPathLen:.2e}")  #,end="")
    #print(self.incDirDist) # отладка

  print1.printGridInfo(self.fInfoGrid)
# = = = = = finitSearchGrid


def findDirMaxDist():
  """Ищем индексы минимального элемента массива incDirDist (2024-08-13)
     Это направление, для которого точка с условием стационарности наиболее далека от текущей """

  iCoordMax0 = self.incDirDist[0].index(min(self.incDirDist[0]))
  iCoordMax1 = self.incDirDist[1].index(min(self.incDirDist[1]))
  if self.incDirDist[0][iCoordMax0] < self.incDirDist[1][iCoordMax1]:
    iDirMax = 0
    iCoordMax = iCoordMax0
  else:
    iDirMax = 1
    iCoordMax = iCoordMax1

  return iDirMax, iCoordMax, self.gridPathLen - self.incDirDist[iDirMax][iCoordMax]
# = = = = = findDirMaxDist


def incSSmult(pI):
  """ Увеличение множителя для размера шага сетки 2024-08-02"""
  self.ss_mult[pI] = min(self.ss_mult[pI] + 1, self.ss_mult_max)
  return


def decSSmult(pI):
  """ Уменьшение множителя для размера шага сетки 2024-08-02"""
  self.ss_mult[pI] = max(self.ss_mult[pI] // 2, 1)
  return


def checkGSC():
  """ Проверка выполнения ОУС после поиска по сетке 2024-08-12"""
  
  if self.NEv>=self.maxNEv : # Процесс завершился принудительно, 
    return               # проверка штатного условия завершения бессмыслена

  isFirst = True
  for iCoord in range(0, self.dim):
    for iDir in range(0, 2):
      distSC = self.gridPathLen - self.incDirDist[iDir][iCoord]
      if distSC > self.GCSdist:
        if isFirst:
          isFirst = False
          print(f"\n!!!Нет условия приемлемости ({self.ss_cur:.1e})", end=":")

        print(
            f"{iCoord} {iDir}; {self.gridPathLen:.1e}-{self.incDirDist[iDir][iCoord]:.1e}={distSC:.2e}>{self.GCSdist:.2e}",
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
