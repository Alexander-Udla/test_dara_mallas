from odoo import fields, models

class field_wide(models.Model):
    _name='dara_mallas.field_wide'
    
    
    name=fields.Char('Campo amplio')
    code = fields.Char('Código de campo amplio')

class field_specific(models.Model):
    _name='dara_mallas.field_specific'
    
    
    name=fields.Char('Campo especifico')
    code = fields.Char('Código de campo especifico')
    field_wide_id = fields.Many2one('dara_mallas.field_wide')

class field_detailed(models.Model):
    _name='dara_mallas.field_detailed'
    
    
    name=fields.Char('Campo detallado')
    code = fields.Char('Código de campo detallado')
    field_specific_id = fields.Many2one('dara_mallas.field_specific')