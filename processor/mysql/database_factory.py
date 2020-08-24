from processor.mysql import default_mysql, aagag_mysql

databases = {
    '네이버뉴스': default_mysql,
    '네이버블로그': default_mysql,
    '네이버카페': default_mysql,
    '네이버실시간검색': default_mysql,
    '기타커뮤니티': aagag_mysql
}


def get(channel_key):
    return databases[channel_key]
