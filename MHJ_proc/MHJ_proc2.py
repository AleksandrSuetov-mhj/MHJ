

def lstToStr ( pLst, pFormEl="" ) :
  """Выводит список в строку форматируя элементы по указанному формату pFormEl"""
  res = ""
  for i in range(len(pLst)) :
    if len(pFormEl)>0 :
      res += ("{0:"+pFormEl+"}").format(pLst[i])
    else :
      res += str(pLst[i])
      
    if i<len(pLst)-1 : res += " "
      
  return res
# = = = = = lstToStr



def lstToStr2 ( pLst, pFormEl="" ) :
  """Выводит список в строку форматируя элементы по указанному формату pFormEl
     Нулевые элементы заменяются на пробелы  
  """
  res = ""
  for i in range(len(pLst)) :
    if len(pFormEl)>0 :
      elem = ("{0:"+pFormEl+"}").format(pLst[i])
    else :
      elem = str(pLst[i])

    if pLst[i]==0 : 
      elem = ("{0:"+str(len(elem))+"}").format("")

    res += elem

    if i<len(pLst)-1 : 
      res += " "

  
  return res
# = = = = = lstToStr2/MHJ_proc2.py

