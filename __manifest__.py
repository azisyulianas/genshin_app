{
  'name': 'Genshin Applications',
  'version': '1.0',
  'summary': 'A module for managing Genshin-related applications',
  'description': 'This module provides features and functionalities for managing Genshin applications.',
  'author': 'Your Name',
  'website': 'https://yourwebsite.com',
  'category': 'Services/Genshin',
  'depends': [
    'base'
  ],
  'data': [
    'security/genshin_app_security.xml',
    'security/ir.model.access.csv',
    'views/genshin_menu.xml',
    'views/genshin_character_view.xml',
    'views/genshin_character_input.xml'
  ],
  'installable': True,
  'application': True,
  'license': 'LGPL-3',
}