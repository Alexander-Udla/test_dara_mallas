'''
Created on Mar 13, 2019

@author: fbaez
'''
from odoo import models, fields,api

class sniese_program(models.Model):
    _name="dara_mallas.sniese_program"
    _rec_name="sniese_code"
    
    sniese_code=fields.Char("codigo")
    status=fields.Char("Estado")
    approval_resolution=fields.Char("Resolución")
    duration=fields.Integer("Duración")
    regime=fields.Char("Régimen")
    #redesign_code=fields.Char("Codigo Rediseño")
    ces_date=fields.Date("Fecha Ingreso CES")
    ces_approval_date=fields.Date("Fecha Aprobación CES")
    council_approval_date=fields.Date("Fecha Aprobación Consejo Universitario")
    effectiveness_end_date=fields.Date("Fecha de fin de Vigencia")
    hours_credits=fields.Char("Horas/Creditos")
    study_plan_ids=fields.One2many("dara_mallas.study_plan", inverse_name='sniese_program_id') 
    first_cohort_date=fields.Date("Inicio clases primera corhorte")
    courses=fields.Integer("Número de paralelos")
    students=fields.Integer("Número de estudiantes")
    homologation_name_id=fields.Many2one("dara_mallas.name_approved")

    #===========================================
    #            catalogo de programas
    #===========================================
    banner_complete_name = fields.Char("Nombre completo BANNER")
    sniese_name = fields.Char("Nombre SNIESE")
    transitional_provision = fields.Selection((('SEGUNDA','SEGUNDA'),('TERCERA','TERCERA'),('APROBACION NORMAL','APROBACION NORMAL')), string="Transitoria")
    field_wide_id = fields.Many2one('dara_mallas.field_wide','Campo amplio')
    field_specific_id = fields.Many2one('dara_mallas.field_specific','Campo especifico')
    field_detailed_id = fields.Many2one('dara_mallas.field_detailed','Campo detallado')

    #resoluions

    firsth_approval_resolution_id = fields.Many2one('dara_mallas.resolutions','Resolución de primera aprobación')
    actualization_resolution_id = fields.Many2one('dara_mallas.resolutions','Resolución de actualización')
    resolution_to_bid_id = fields.Many2one('dara_mallas.resolutions','Resolución para ofertar')
    non_validity_resolution_id = fields.Many2one('dara_mallas.resolutions','Resolución de no vigencia')


    #@api.onchange('field_wide_id','field_specific_id')
    #def onchange_code(self):
        #type=self.type or ""
        #journey=self.journey_id.code or ""
        #mode=self.mode_id.code or ""
        #saes_code=self.saes_code_id.name or ""
        #self.name=type+journey+mode+saes_code 

#nombre homologado
class name_approved(models.Model): 
    _name="dara_mallas.name_approved"
    
    name=fields.Char("Nombre Homologado")
    


