'''
Created on Mar 13, 2019

@author: fbaez
'''



from odoo import models, fields,api
from odoo.exceptions import UserError


       
    
class program_code(models.Model): 
    _name="dara_mallas.program_code"
    
    name=fields.Char(string="Codigo de programa")
    type=fields.Char("Tipo Educacion")
    journey_id=fields.Many2one("dara_mallas.journey")       
    mode_id=fields.Many2one("dara_mallas.mode")
    saes_code_id=fields.Many2one("dara_mallas.saes_code")
    program_id=fields.Many2one("dara_mallas.program")
    
    @api.onchange('type','journey_id','mode_id','saes_code_id') 
    def onchange_code(self):
        type=self.type or ""
        journey=self.journey_id.code or ""
        mode=self.mode_id.code or ""
        saes_code=self.saes_code_id.name or ""
        self.name=type+journey+mode+saes_code 

class program(models.Model):
    _name="dara_mallas.program"
    
    name=fields.Char("Carrera / Programa")
    name_en=fields.Char("Career / Program")
    long_name=fields.Char("Nombre Completo")
    code_ids=fields.One2many("dara_mallas.program_code", inverse_name="program_id")
    description=fields.Char("Descripcion")
    program_min_pga=fields.Float("PGA minimo de programa")
    college_id=fields.Many2one("dara_mallas.college", string="Facultad / Escuela")

    specializations_ids=fields.One2many("dara_mallas.specialization",inverse_name="program_id") 

    #=======================================
    #                 catalogo de programas
    # ======================================
    duration_type = fields.Char("Tipo duración")
    period_id=fields.Many2one("dara_mallas.period","Periodo de catálogo")
    
    
class saes_code(models.Model):
    _name="dara_mallas.saes_code"
    
    name=fields.Char("Codigo SAES")