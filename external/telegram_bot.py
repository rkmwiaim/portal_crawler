import requests
import os
import yaml
import definitions

with open(os.path.join(definitions.RESOURCE_DIR, 'telegram_conf.yaml')) as f:
  TELEGRAM_CONF = yaml.load(f, Loader=yaml.FullLoader)
  BOT_KEY = TELEGRAM_CONF['bot_key']
  telegram_ids = TELEGRAM_CONF['ids']


def get_updates():
  return requests.get('https://api.telegram.org/bot{}/getUpdates'.format(BOT_KEY)).text


def send_message(chat_id, msg):
  requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_KEY, chat_id, msg))


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


if __name__ == '__main__':
  r = send_file(telegram_ids['kmryu'], 'test.zip')
  print(r)
