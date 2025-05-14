from odoo import fields, models
import requests
import base64
import logging
_logger = logging.getLogger(__name__)

API_URL = "https://genshin.jmp.blue/"
API_URL_CHAR = API_URL+"characters/"

class ImportCharacter(models.TransientModel):
  _name = "genshin.character.input"
  _description = "Input character information from eksternal api"

  name_id = fields.Char(
    string='name'
  )

  def get_list_image(self, character_name)->list:
    LINK = API_URL_CHAR+character_name+'/list'
    res = requests.get(LINK)
    if res.status_code == 200:
      return res.json()
    return []

  def get_image_data(self, character_name, image_name):
    LINK = API_URL_CHAR+character_name+'/'+ image_name
    data = ""
    try:
        data = base64.b64encode(requests.get(LINK).content).replace(b"\n", b"")
    except Exception as e:
        _logger.warning("Can't load the image from URL %s" % LINK)
        logging.exception(e)
    return data

  def check(self):
    LINK = API_URL_CHAR+self.name_id
    CHAR_NAME = self.name_id
    char = requests.get(LINK)
    json_data = char.json()
    Character = self.env['genshin.character']
    character = Character.search([("unique_name","=",CHAR_NAME)], limit=1)
    if not character.id:
      new_char = Character.create([
        {
          'name':json_data['name'], 'unique_name':self.name_id, 'title':json_data['title'], 
          'description':json_data['description'], 'affiliation':json_data['affiliation'],
          'birthday':'/'.join((json_data['birthday'].split('-')[1::])),
          'vision':json_data['vision_key'], 'weapon':json_data['weapon_type'],
          'rarity':str(json_data['rarity']),'nation':json_data['nation'],
          'constellation_name':json_data['constellation'],'release':fields.Date.to_date(json_data['release']),
        }
      ])

      for image_name in self.get_list_image(CHAR_NAME):
        if 'card' == image_name:
          new_char.update({
            'image_card':self.get_image_data(CHAR_NAME, image_name)
          })
        if 'gacha-card' == image_name:
          new_char.update({
            'image_gacha_card':self.get_image_data(CHAR_NAME, image_name)
          })
        if 'gacha-splash' == image_name:
          new_char.update({
            'image_gacha_splash':self.get_image_data(CHAR_NAME, image_name)
          })
        if 'icon-big' == image_name:
          new_char.update({
            'image_icon_big':self.get_image_data(CHAR_NAME, image_name)
          })

    return {
      'type': 'ir.actions.act_window',
      'res_model': 'genshin.character',
      'view_mode': 'tree,form'
    }
    
      

