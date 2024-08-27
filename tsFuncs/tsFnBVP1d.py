#TODO: Функционал энергии для одномерной краевой задачи

def tsFnBVP1d ( x ) :
  #Rosenbroke's generalised func with N arguments 
  #f(x)=sum ((1-x[i])^2+ 100 (x[i+1] - x[i]^2)^2)
  dim = len(x)

  if dim==0 : return -1
  Result = x[0]**2

  for i in range(0,dim-2):
    Result += (x[i+1]-x[i])**2  

  Result += x[dim-1]**2

  Result *= dim
  return Result
  #= = = = = tsFnBVP1d


if __name__=="main" :
  import sys
  
  for i in range(1, 5) :
    print(tsFnBVP1d([1]*i))
  
  for i in range(1, 5) :
    print(tsFnBVP1d([i]*i))
  
  sys.exit(f"Работа tsFnBVP1d завершена штатно")
  