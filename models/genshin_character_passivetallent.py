from odoo import fields, api, models

class GenshinCharacterPassiveTalent(models.Model):
  _name = "genshin.character.passivealent"
  _description = "Model description for character's Passive Talent"

  name = fields.Char()
  description = fields.Text()
  character_id = fields.Many2one(
    "genshin.character",
    "Character"
  )
  image = fields.Binary()