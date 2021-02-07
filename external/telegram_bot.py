import os
import zipfile
from io import BytesIO

import requests
import yaml

import definitions

with open(os.path.join(definitions.RESOURCE_DIR, 'telegram_conf.yaml')) as f:
  TELEGRAM_CONF = yaml.load(f, Loader=yaml.FullLoader)
  BOT_KEY = TELEGRAM_CONF['bot_key']
  telegram_ids = TELEGRAM_CONF['ids']


def get_updates():
  return requests.get('https://api.telegram.org/bot{}/getUpdates'.format(BOT_KEY)).text


def send_message(chat_id, msg):
  data = {
    'chat_id': chat_id,
    'text': msg
  }
  return requests.post('https://api.telegram.org/bot{}/sendMessage'.format(BOT_KEY), data=data)
  # requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_KEY, chat_id, msg))


def send_file(chat_id, file_path):
  data = {
    'chat_id': chat_id
  }
  f = open(file_path, 'rb')
  files = {
    'document': f
  }
  response = requests.post('https://api.telegram.org/bot{}/sendDocument'.format(BOT_KEY), data=data, files=files)
  f.close()
  return response


def send_content_zip(chat_id, content, zip_file_name):
  buff = BytesIO()
  buff.name = 'error.zip'

  zip_archive = zipfile.ZipFile(buff, mode='w', compression=zipfile.ZIP_DEFLATED)
  zip_archive.filename = 'zip.zip'
  zip_archive.writestr('error.txt', content)
  zip_archive.compression
  zip_archive.close()

  zip_file_path = os.path.join(definitions.ERROR_FILE_DIR, zip_file_name)
  with open(zip_file_path, 'wb') as f:
    f.write(buff.getvalue())

  return send_file(chat_id, zip_file_path)


if __name__ == '__main__':
  res = send_message(telegram_ids['네이버실시간검색'], 'test message from bot')
  print(res)
  # print(get_updates())
