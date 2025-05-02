from odoo import fields, api, models

class GenshinCharModel(models.Model):
  _name = "genshin.character"
  _description = "Genshin Character Information"
  _order = "name desc"

  name = fields.Char()
  unique_name = fields.Char()
  title = fields.Char()
  affilation = fields.Char()
  nation = fields.Char()
  rarity = fields.Selection([
    ("4","4 Star"),
    ("5","5 Star"),
  ], "Rarity")
  relase = fields.Date()
  description = fields.Text()
  constellation_name = fields.Char()
  birthday = fields.Char()
  vision = fields.Selection([
      ("ANEMO", "Anemo"),
      ("CRYO", "cryo"),
      ("DENDRO", "dendro"),
      ("ELECTRO", "electro"),
      ("GEO", "geo"),
      ("HYDRO", "hydro"),
      ("PYRO", "pyro"),
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



