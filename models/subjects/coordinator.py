from odoo import models, api, fields

class coordinator(models.Model):
    _name="dara_mallas.coordinator"
    
    name=fields.Char("Nombres")
    idbanner=fields.Char("ID Banner")
