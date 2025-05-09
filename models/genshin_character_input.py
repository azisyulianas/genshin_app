from odoo import fields, models
import requests
API_URL = "https://genshin.jmp.blue/"


class ImportCharacter(models.TransientModel):
  _name = "genshin.character.input"
  _description = "Input character information from eksternal api"

  name_id = fields.Char(
    string='name'
  )

  def check(self):
    API_URL_CHAR = API_URL+"characters/"
    char = requests.get(API_URL_CHAR+self.name_id)
    json_data = char.json()
    Character = self.env['genshin.character']
    character = Character.search([("unique_name","=",self.name_id)], limit=1)
    if not character.id:
      Character.create([
        {
          'name':json_data['name'],
          'uni'
        }
      ])
    
      

