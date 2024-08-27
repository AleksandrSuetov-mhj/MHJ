import sys
import datetime

a = datetime.datetime.today()
print(a) # datetime.datetime(2017, 4, 5, 0, 16, 54, 989663)

b = datetime.datetime.now()
print(b) # datetime.datetime(2017, 4, 5, 0, 17, 8, 24239)


a = datetime.datetime.today().strftime("%Y%m%d")
print(a) # '20170405'

today = datetime.datetime.today()
print( today.strftime("%m/%d/%Y") ) # '04/05/2017'

print( today.strftime("%Y-%m-%d/%Hч%Mм%Sс") ) # 2017-04-05-00.18.00
print( datetime.datetime.today().strftime("%Y-%m-%d/%Hч%Mм%Sс") ) # 2017-04-05-00.18.00

sys.exit(f"Эксперимент {__name__} завершен штатно")
