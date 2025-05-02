from odoo import fields, api, models

class GenshinCharacterAscensionMaterials(models.Model):
  _name = "genshin.character.ascensionmaterial"
  _description = "Model description for character's Ascension Materials"

  level = fields.Selection([
    ("level_20","20"),
    ("level_40","40"),
    ("level_50","50"),
    ("level_60","60"),
    ("level_70","70"),
    ("level_80","80"),
  ])
  material_id = fields.Many2one(
    'genshin.material',
    "Material")
  value = fields.Integer()
  unique_id=fields.Char(
    readonly=True 
  )