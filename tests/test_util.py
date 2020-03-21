import os

from bs4 import BeautifulSoup

import definitions


def file_to_soup(file_name):
  test_file_path = os.path.join(definitions.TEST_RESOURCE_DIR, file_name)
  f = open(test_file_path, 'r')
  try:
    html = f.read()
    return BeautifulSoup(html, 'html.parser')
  finally:
    f.close()