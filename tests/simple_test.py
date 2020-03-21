import pymysql
from functional import seq

def t(i):
  print(i)
  return i

if __name__ == '__main__':
  seq([1,2,3,4,5]).map(t).for_each(print)