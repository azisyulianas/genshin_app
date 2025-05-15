import requests
import base64
import logging
_logger = logging.getLogger(__name__)

API_URL = "https://genshin.jmp.blue/"
API_URL_CHAR = API_URL+"characters/"

def get_image_data(character_name, image_name):
  LINK = API_URL_CHAR+character_name+'/'+ image_name
  data = ""
  try:
      data = base64.b64encode(requests.get(LINK).content).replace(b"\n", b"")
  except Exception as e:
      _logger.warning("Can't load the image from URL %s" % LINK)
      logging.exception(e)
  return data