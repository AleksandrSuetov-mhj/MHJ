'''
Обобщённая функция Розенброка от нескольких переменных 
для тестирования методов минимизации, не использующих производные.
В случае двух переменных множества уровня функции похожи на "бананообразную долину".

f(\mathbf{x}) = \sum_{i=1}^{N-1} \left((1-x_i)^2+ 100 (x_{i+1} - x_i^2 )^2 \right) 
\quad \forall \mathbf{x}\in\mathbb{R}^N.
'''

def tsFnRosen ( x ) :
    #Rosenbroke's generalised func with N arguments 
    #f(x)=sum ((1-x[i])^2+ 100 (x[i+1] - x[i]^2)^2)
    dim = len(x)

    Result = 0.0
    #print (x)      
    #print(dim)
    for i in range(dim):
      Result += (1-x[i])**2 
      if i<dim-1 :
        Result += 100*(x[i+1]-x[i]**2)**2  

    return Result
    #= = = = = tf_rosenGen

