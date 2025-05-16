from odoo import fields, api, models
import requests
import base64
import logging
_logger = logging.getLogger(__name__)

API_URL = "https://genshin.jmp.blue/"
API_URL_CHAR = API_URL+"characters/"

# AYAM GORENG

VISION = [
      ("ANEMO", "Anemo"), ("CRYO", "Cryo"),
      ("DENDRO", "Dendro"), ("ELECTRO", "Electro"),
      ("GEO", "Geo"), ("HYDRO", "Hydro"),
      ("PYRO", "Pyro"),]

WEAPON = [
    ("SWORD","Sword"), ("CLAYMORE","Claymore"),
    ("POLEARM","Polearm"), ("CATALYST","Catalyst"),
    ("BOW","Bow"),]

def get_image_data(character_name, image_name):
  LINK = API_URL_CHAR+character_name+'/'+ image_name
  data = ""
  try:
      data = base64.b64encode(requests.get(LINK).content).replace(b"\n", b"")
  except Exception as e:
      _logger.warning("Can't load the image from URL %s" % LINK)
      logging.exception(e)
  return data


class GenshinCharModel(models.Model):
  _name = "genshin.character"
  _description = "Genshin Character Information"
  _order = "name desc"

  _sql_constraints = [
    ("unique_name",'UNIQUEUNIQUE(unique_name)',"name alerdy exist")
  ]

  name = fields.Char()
  unique_name = fields.Char()
  title = fields.Char()
  affiliation = fields.Char()
  nation = fields.Char()
  rarity = fields.Selection([
    ("4","4 Star"),
    ("5","5 Star"),
  ], "Rarity")
  release = fields.Date()
  description = fields.Text()
  constellation_name = fields.Char()
  birthday = fields.Char()
  vision = fields.Selection(VISION)
  weapon = fields.Selection(WEAPON)
  ascension_material_ids = fields.Many2many(
    "genshin.character.ascensionmaterial"
  )
  constelation_ids = fields.One2many(
    "genshin.character.constelation",
    "character_id",
    "Constelaltion",
    compute="_compute_character_constelation",
    store=True
  )
  talent_ids = fields.One2many(
    "genshin.character.talent",
    "character_id",
    "Skill Talent",
    compute="_compute_character_talent",
    store=True
  )
  data = fields.Json()

  image_card = fields.Binary(
    "Card",
    compute="_compute_image_card",
    store=True,
  )
  image_gacha_card = fields.Binary(
    "Gacha Card",
    compute="_compute_image_gacha_card",
    store=True,
  )
  image_gacha_splash = fields.Binary(
    "Gacha Splash",
    compute="_compute_image_gacha_splash",
    store=True,
  )
  image_icon_big = fields.Binary(
    "Icon Big",
    compute="_compute_image_icon_big",
    store=True,
  )
  image_constelation = fields.Binary(
    "Constelation",
    compute="_compute_image_constelation",
    store=True,
  )
  
  @api.depends('unique_name','name')
  def _compute_character_talent(self):
    for record in self:
      for talent_skill in record.data['skillTalents']:
        unique_id = record.unique_name+talent_skill['name']
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
        talent = record.talent_ids.search([('unique_id','=',unique_id)], limit=1)
        if not talent.id:
          record.talent_ids.create({
            'unique_id':unique_id,
            'type':type,
            'name':talent_skill['name'],
            'description':talent_skill['description'],
            'talent_type':'skill',
            'character_id':record.id,
            'level':level,
            'image':get_image_data(record.unique_name, image)
          })
          continue
        talent.update({
          'type':type,
          'name':talent_skill['name'],
          'description':talent_skill['description'],
          'talent_type':'skill',
          'character_id':record.id,
          'level':level,
          'image':get_image_data(record.unique_name, image)
        })
      
      for talent_passive in record.data["passiveTalents"]:
        unique_id = record.unique_name+talent_passive["name"]
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
        talent = record.talent_ids.search([('unique_id','=',unique_id)], limit=1)
        data = {
          'type':type,
          'name':talent_passive['name'],
          'description':talent_passive['description'],
          'talent_type':'passive',
          'character_id':record.id,
          'level':level,
          'image':get_image_data(record.unique_name, image)
        }
        if not talent.id:
          data['unique_id'] = unique_id
          record.talent_ids.create(data)
        talent.update(data)
  
  @api.depends('unique_name')
  def _compute_image_card(self):
    for record in self:
      record.image_card = get_image_data(record.unique_name, "card")
 
  @api.depends('unique_name')
  def _compute_image_gacha_card(self):
    for record in self:
      record.image_gacha_card = get_image_data(record.unique_name, "gacha-card")
  
  @api.depends('unique_name')
  def _compute_image_gacha_splash(self):
    for record in self:
      record.image_gacha_splash = get_image_data(record.unique_name, "gacha-splash")
  
  @api.depends('unique_name')
  def _compute_image_icon_big(self):
    for record in self:
      record.image_icon_big = get_image_data(record.unique_name, "icon-big")
  
  @api.depends('unique_name')
  def _compute_image_constelation(self):
    for record in self:
      record.image_constelation = get_image_data(record.unique_name, "constellation")
  
  @api.depends('unique_name','name')
  def _compute_character_constelation(self):
    for record in self:
      if len(record.constelation_ids)>0:
        break
      for constellations in record.data['constellations']:
        unique_id = record.unique_name+'-constelation-'+str(constellations['level'])
        cons = record.constelation_ids.search([('unique_id','=',unique_id)], limit=1)
        if not cons.id:
          record.constelation_ids.create({
            'character_id':record.id,
            'name':constellations['name'],
            'description':constellations['description'],
            'level':constellations['level'],
            'image':get_image_data(record.unique_name, 'constellation-'+str(constellations['level'])),
            'unique_id':unique_id
          })
          continue
        cons.update({
          'character_id':record.id,
          'name':constellations['name'],
          'description':constellations['description'],
          'level':constellations['level'],
          'image':get_image_data(record.unique_name, 'constellation-'+str(constellations['level'])),
        })
  
  def action_generate_material(self):
    self.ensure_one()
    for key, values in self.data["ascension_materials"].items():
      if key == "level_20":
        for value in values:
          unique_id = value


  def input_via_api(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Input Character',
      'res_model': 'genshin.character.input',
      'view_mode': 'form',
      'view_type': 'form',
      'target': 'new',
    }

