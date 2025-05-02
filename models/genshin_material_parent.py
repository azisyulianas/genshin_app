from odoo import fields, api, models

class GenshinMaterialParent(models.Model):
  _name = "genshin.material.parent"
  _description = "Genshin Material Parent Information"

  name = fields.Char()