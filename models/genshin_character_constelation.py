from odoo import fields, api, models

class GenshinCharacterConstelaltion(models.Model):
  _name = "genshin.character.constelation"
  _description = "Model description for character's constelaltion"

  name = fields.Char()
  description = fields.Text()
  level = fields.Integer()
  character_id = fields.Many2one(
    "genshin.character",
    "Character"
  )
  image = fields.Binary()
