import traceback


def base():
  try:
    raise ValueError
  except:
    handle_error()



def handle_error():
  traces = traceback.format_exc()
  print('------------------------------')
  print(traces)
  print('------------------------------')
  raise

if __name__ == '__main__':
  base()
