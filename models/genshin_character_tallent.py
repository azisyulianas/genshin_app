from odoo import fields, api, models

class GenshinCharacterTalent(models.Model):
  _name = "genshin.character.talent"
  _description = "Model description for character's Skill Talent"
  _order = "level"

  name = fields.Char()
  unique_id = fields.Char()
  description = fields.Text()
  talent_type = fields.Selection([
    ("passive","Passive Talent"),
    ("skill","Skill Talent"),
  ])
  type = fields.Selection([
    ("NORMAL_ATTACK",'Normal Attack'),
    ("ELEMENTAL_SKILL",'Elemental Skill'),
    ("ELEMENTAL_BURST",'Elemental Burst'),
    ("OTHER",'other'),
  ])
  character_id = fields.Many2one(
    "genshin.character",
    "Character"
  )
  level = fields.Integer()
  image = fields.Binary()