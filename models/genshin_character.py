from odoo import fields, api, models

class GenshinCharModel(models.Model):
  _name = "genshin.character"
  _description = "Genshin Character Information"
  _order = "name desc"

  name = fields.Char()
  title = fields.Char()
  affilation = fields.char()
  rarity = fields.Integer()
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
  constelation_ids = fields.One2many(
    "genshin.character.constelation",
    "character_id",
    "Constelaltion"
  )
  passive_talent_ids = fields.One2many(
    "genshin.character.passivealent",
    "character_id",
    "Passive Talent"
  )
  skill_talent_ids = fields.One2many(
    "genshin.character.skilltalent",
    "character_id",
    "Skill Talent"
  )
  image_card = fields.Binary("Card")
  image_gacha_card = fields.Binary("Gacha Card")
  image_gacha_splash = fields.Binary("Gacha Splash")



