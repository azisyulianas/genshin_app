from odoo import fields, api, models

class GenshinMaterial(models.Model):
  _name = "genshin.material"
  _description = "Genshin Material Information"
  
  unique_name = fields.Char(
    readonly=True,
  )
  name = fields.Char()
  rarity = fields.Integer()
  image = fields.Binary()
  parent = fields.Many2one(
    'genshin.material.parent',
    'Parent'
  )
  