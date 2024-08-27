import sys

def myPrint (*args,**kwargs) : 
  print(*args,**kwargs)


def checkMyPrint (*args,**kwargs) :
  myPrint(*args,**kwargs)

checkMyPrint("раз",2,"three",end="\n!!!\n", sep="---")
sys.exit(f"Эксперимент {__name__} завершен штатно")

