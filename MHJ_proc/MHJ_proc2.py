

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
