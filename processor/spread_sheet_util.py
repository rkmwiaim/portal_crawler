import re


def split_A1_notation(a1_notation):
  m = re.search('([A-Z]+)([0-9]+)', a1_notation)
  return (m.group(1), m.group(2))


def col2num(col):
  num = 0
  for c in col:
    if str.isascii(c):
      num = num * 26 + (ord(c.upper()) - ord('A')) + 1
  return num


def num2col(n):
  string = ""
  while n > 0:
    n, remainder = divmod(n - 1, 26)
    string = chr(65 + remainder) + string
  return string



if __name__ == '__main__':
  print(col2num('A'))
  print(col2num('AB'))
  print(col2num('Z'))

  print(split_A1_notation('A1'))
  print(split_A1_notation('AB23'))
  print(split_A1_notation('CC1'))

  print(num2col(1))
