from odoo import fields, api, models

class GenshinCharacterSkillTalent(models.Model):
  _name = "genshin.character.skilltalent"
  _description = "Model description for character's Skill Talent"

  name = fields.Char()
  description = fields.Text()
  type = fields.Selection([
    ("NORMAL_ATTACK",'Normal Attack'),
    ("ELEMENTAL_SKILL",'Elemental Skill'),
    ("ELEMENTAL_BURST",'Elemental Burst'),
  ])
  character_id = fields.Many2one(
    "genshin.character",
    "Character"
  )
  image = fields.Binary()