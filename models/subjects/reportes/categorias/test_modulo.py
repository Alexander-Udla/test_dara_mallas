from odoo import fields, models # type: ignore

class ModuloPrueba(models.Model):
    _name = "dara_mallas.prueba"
    _description = "Modulo de prueba para multiuniversidad"
    
    #campos principales
    numero = fields.Char(string = "Número")
    texto = fields.Char(string = "texto")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    