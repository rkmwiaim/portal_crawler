import external.url_redirect_follower as url_follower

url = 'https://aagag.com//mirror/re.php?ss=slrclub_38238669'
redirected_url = url_follower.get_redirected_url(url)
print(redirected_url)
