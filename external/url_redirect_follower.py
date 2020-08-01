import os

import definitions
import subprocess

script_path = os.path.join(definitions.ROOT_DIR, 'node_libs', 'url_redirect_follower.js')


def get_redirected_url(url):
    return subprocess.check_output(['node', script_path, url]).decode('utf-8').strip()


if __name__ == '__main__':
    target_url = 'https://aagag.com/mirror/re.php?ss=mlbpark_202006090043618064'
    result = get_redirected_url(target_url)
    print(result)
