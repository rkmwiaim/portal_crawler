import pymysql

if __name__ == '__main__':
  conn = pymysql.connect(host='ziem.iptime.org',
                         port=10023,
                         user='archive', password='a9205419!',
                         db='portal_crawler', charset='utf8')

  curs = conn.cursor()
  sql = "select * from article"
  curs.execute(sql)

  rows = curs.fetchall()
  print(rows)

  conn.close()