from odoo import fields, api, models

MATERIAL_TYPE = [
  ("boss-material","Bos Material"), ("character-ascension","Character Ascension"),
  ("character-experience","Character Experience"), ("common-ascension","Common Ascension"),
  ("cooking-ingredients","Cooking Ingredients"), ("local-specialties","Local Specialties"),
  ("talent-book","Talent Book"), ("talent-boss","Talent Bos"),
  ("weapon-ascension","Weapon Ascension"), ("weapon-experience","Weapon Experience"),
]

class GenshinMaterial(models.Model):
  _name = "genshin.material"
  _description = "Genshin Material Information"
  
  unique_name = fields.Char(
    readonly=True,
  )
  name = fields.Char()
  rarity = fields.Integer()
  image = fields.Binary()
  material_type = fields.Selection(MATERIAL_TYPE)
  