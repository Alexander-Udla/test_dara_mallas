from odoo import fields, models

class college(models.Model):
    _name="dara_mallas.college"
    
    name=fields.Char("Facultad")
    name_en=fields.Char("College")
    name_short=fields.Char("Facultad Nombre Corto")
    code=fields.Char("Codigo")
    #dean_id = fields.Many2one("dara_mallas.dean") 

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )