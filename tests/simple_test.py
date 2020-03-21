import pymysql
from functional import seq


def t(i):
  raise ValueError()
  return i


def main():
  # result = seq([1, 2, 3, 4, 5]).map(t)
  result = map(lambda i: t(i), [1,2,3,4,5])
  return result


if __name__ == '__main__':
  try:
    r = main()
    print(list(r))
  except:
    print('error!')
