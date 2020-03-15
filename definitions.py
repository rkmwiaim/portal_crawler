import os
import logging


def get_logger():
  crawler_log = logging.getLogger('crawler')
  crawler_log.setLevel(logging.DEBUG)
  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'))
  crawler_log.addHandler(stream_handler)

  return crawler_log


log = get_logger()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
