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
    string='Name'
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
      character = Character.create([
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
        character.update({
          'image_card':self.get_image_data(CHAR_NAME, image_name)
        })
        continue
      if 'gacha-card' == image_name:
        character.update({
          'image_gacha_card':self.get_image_data(CHAR_NAME, image_name)
        })
        continue
      if 'gacha-splash' == image_name:
        character.update({
          'image_gacha_splash':self.get_image_data(CHAR_NAME, image_name)
        })
        continue
      if 'icon-big' == image_name:
        character.update({
          'image_icon_big':self.get_image_data(CHAR_NAME, image_name)
        })
        continue
      if 'constellation' == image_name:
        character.update({
          'image_constelation':self.get_image_data(CHAR_NAME, image_name)
        })
        continue

    for constelation in json_data['constellations']:
      unique_id = CHAR_NAME+'-constelation'+str(constelation['level'])
      cons = self.env['genshin.character.constelation'].search([('unique_id','=',unique_id)], limit=1)
      if not cons.id:
        self.env['genshin.character.constelation'].create({
          'character_id':character.id,
          'name':constelation['name'],
          'description':constelation['description'],
          'level':constelation['level'],
          'image':self.get_image_data(CHAR_NAME, 'constellation-'+str(constelation['level'])),
          'unique_id':unique_id
        })
        continue
      cons.update({
        'character_id':character.id,
        'name':constelation['name'],
        'description':constelation['description'],
        'level':constelation['level'],
        'image':self.get_image_data(CHAR_NAME, 'constellation-'+str(constelation['level'])),
      })
    
    for talent_skill in json_data['skillTalents']:
      unique_id = CHAR_NAME+talent_skill['name']
      if 'type' in talent_skill:
        if talent_skill['type'] == "NORMAL_ATTACK":
          type = "NORMAL_ATTACK"
          level = 1
          image = "talent-na"
        elif talent_skill['type'] == "ELEMENTAL_SKILL":
          type = "ELEMENTAL_SKILL"
          level = 2
          image = "talent-skill"
        else:
          type = "ELEMENTAL_BURST"
          level = 3
          image = "talent-burst"
      else:
        level = 4
        type = "OTHER"
        image = "talent-passive-misc"
      talent = self.env['genshin.character.talent'].search([('unique_id','=',unique_id)], limit=1)
      if not talent.id:
        self.env['genshin.character.talent'].create({
          'unique_id':unique_id,
          'type':type,
          'name':talent_skill['name'],
          'description':talent_skill['description'],
          'talent_type':'skill',
          'character_id':character.id,
          'level':level,
          'image':self.get_image_data(CHAR_NAME, image)
        })
        continue
      talent.update({
        'type':type,
        'name':talent_skill['name'],
        'description':talent_skill['description'],
        'talent_type':'skill',
        'character_id':character.id,
        'level':level,
        'image':self.get_image_data(CHAR_NAME, image)
      })

    for talent_passive in json_data["passiveTalents"]:
      unique_id = CHAR_NAME+talent_passive["name"]
      type = "OTHER"
      if 'level' in talent_passive:
        if talent_passive['level'] == 1:
          level = 5
          image = "talent-passive-1"
        else:
          level = 6
          image = "talent-passive-2"
      else:
        level = 7
        image = "talent-passive-0"
        level += 1
      talent = self.env['genshin.character.talent'].search([('unique_id','=',unique_id)], limit=1)
      data = {
        'type':type,
        'name':talent_passive['name'],
        'description':talent_passive['description'],
        'talent_type':'passive',
        'character_id':character.id,
        'level':level,
        'image':self.get_image_data(CHAR_NAME, image)
      }
      if not talent.id:
        data['unique_id'] = unique_id
        self.env['genshin.character.talent'].create(data)
      talent.update(data)

    return {
      'type': 'ir.actions.act_window',
      'res_model': 'genshin.character',
      'view_mode': 'tree,form'
    }
    
      

