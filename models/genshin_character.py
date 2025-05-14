from odoo import fields, api, models

class GenshinCharModel(models.Model):
  _name = "genshin.character"
  _description = "Genshin Character Information"
  _order = "name desc"

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
  vision = fields.Selection([
      ("ANEMO", "Anemo"),
      ("CRYO", "Cryo"),
      ("DENDRO", "Dendro"),
      ("ELECTRO", "Electro"),
      ("GEO", "Geo"),
      ("HYDRO", "Hydro"),
      ("PYRO", "Pyro"),
    ], string="Vision")
  weapon = fields.Selection([
    ("SWORD","Sword"),
    ("CLAYMORE","Claymore"),
    ("POLEARM","Polearm"),
    ("CATALYST","Catalyst"),
    ("BOW","Bow"),
  ])
  ascension_material_ids = fields.Many2many(
    "genshin.character.ascensionmaterial"
  )
  constelation_ids = fields.One2many(
    "genshin.character.constelation",
    "character_id",
    "Constelaltion"
  )
  talent_ids = fields.One2many(
    "genshin.character.talent",
    "character_id",
    "Skill Talent"
  )

  image_card = fields.Binary("Card")
  image_gacha_card = fields.Binary("Gacha Card")
  image_gacha_splash = fields.Binary("Gacha Splash")
  image_icon_big = fields.Binary("Icon Big")
  image_constelation = fields.Binary("Constelation")

  _sql_constraints = [
    ("unique_name",'UNIQUEUNIQUE(unique_name)',"name alerdy exist")
  ]

  def input_via_api(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Input Character',
      'res_model': 'genshin.character.input',
      'view_mode': 'form',
      'view_type': 'form',
      'target': 'new',
    }

