'''
Created on Mar 13, 2019

@author: fbaez
'''

from odoo import models, fields,api
from lxml import etree
import logging


_logger = logging.getLogger(__name__)


class study_plan(models.Model):
    _name="dara_mallas.study_plan"
    
    
    
    program_id=fields.Many2one('dara_mallas.program')
    program_name_en=fields.Char('Program',related="program_id.name_en")
    
    period_id=fields.Many2one("dara_mallas.period")
    description=fields.Char("Descripcion")
    #grade=fields.Char("Nivel")
    grade_id=fields.Many2one("dara_mallas.grade")
    banner_grade_id=fields.Many2one("dara_mallas.banner_grade")

    with_students=fields.Boolean("Tiene carga")
    study_plan_class_id=fields.Many2one("dara_mallas.study_plan_class")
    college_id=fields.Many2one("dara_mallas.college", related="program_id.college_id")
    area_id=fields.Many2one("dara_mallas.subject_department", string="Área")
    program_codes_ids=fields.One2many(related="program_id.code_ids")
    
    graduation_profile=fields.Text("Perfil de egreso")
    graduation_profile_en=fields.Text("Graduate profile")

    #plo_ids=fields.One2many("dara_mallas.plo",inverse_name='study_plan_id') 
    
    study_plan_lines_ids=fields.One2many("dara_mallas.study_plan_line",inverse_name="study_plan_id")
    study_plan_lines_simple_ids=fields.One2many("dara_mallas.study_plan_line_simple",inverse_name="study_plan_id")
    
    state=fields.Selection((('borrador','Borrador'),('vigente','Vigente'),('registro','NO vigente')), string="Estado")
    file=fields.Binary("Archivo")
    file_name=fields.Char("nombre de archivo")
    plan_template_file=fields.Binary("Archivo")
    plan_template_file_name=fields.Char("nombre de archivo")
    prerequisite_file=fields.Binary("Archivo")
    prerequisite_file_name=fields.Char("nombre de archivo")
    corequisite_file=fields.Binary("Archivo")
    corequisite_file_name=fields.Char("nombre de archivo")
    homologation_file=fields.Binary("Archivo")
    homologation_file_name=fields.Char("nombre de archivo")
    
    sniese_program_id=fields.Many2one("dara_mallas.sniese_program")
    redesign_code_id=fields.Many2one("dara_mallas.sniese_program" , string="Código de Rediseño")

    campus_id = fields.Many2one("dara_mallas.campus")

    hours_max = fields.Float("Horas Maximas")
    hours_min = fields.Float("Horas Minimas")
    #=======================================
    #                 catalogo de programas
    # ======================================
    #subjects_qs_id = fields.Many2one("dara_mallas.subject_qs")
    #subjects_th_id = fields.Many2one("dara_mallas.subject_th")
    #dean_id = fields.Char(string="Decano",related="college_id.dean_id.name")

    coordinator_id = fields.Many2one("dara_mallas.coordinator")
    #graduation_mode_ids = fields.One2many("dara_mallas.graduation_mode",inverse_name="study_plan_id")

    #study_plan_update_id=fields.Many2one("dara_mallas.study_plan_update")
    #study_plan_exist_id=fields.Many2one("dara_mallas.study_plan_exist")

    #==============================================
    #        REQUISITOS DE GRADUACION
    #==============================================
    #no_course_ids = fields.One2many("dara_mallas.subject_no_course",inverse_name="study_plan_id")

    #==============================================
    #              PUBLICACIONES
    # =============================================

    mallas_web = fields.Boolean("Publicar Mallas Web ?")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.program_id.name),str(rec.period_id.name))))
        return result
      
    

    @api.onchange('study_plan_lines_ids') 
    def onchange_study_plan_lines_ids(self):
        self.write({
                                        'study_plan_lines_simple_ids':[(6, 0, [])]
                    })
        for item in self.study_plan_lines_ids:
            for item_two in item.area_subject_inherit_area_ids:
                self.write({
                                        'study_plan_lines_simple_ids':[(0,0,{ 
                                                    'subject_id':item_two.subject_id.id,
                                                    'period_subject_id':item_two.subject_scarse_period_id.id,
                                                    'period_id':item.area_homologation_id.period_id.id,
                                                    'area_id':item.area_homologation_id.area_id.id
                                                    })]
                                    })

 


class study_plan_line(models.Model):
    _name="dara_mallas.study_plan_line"
    #_rec_name="subject_id"
    _order="line_order asc"
    line_order=fields.Integer("No.")
    area_homologation_id=fields.Many2one("dara_mallas.area_homologation", string="Areas")
    area_homologation_code=fields.Char("Codigo Area",related="area_homologation_id.area_id.code")
    area_subject_inherit_area_ids=fields.One2many(related="area_homologation_id.subject_inherit_area_ids") 
    #level_id=fields.Many2one("dara_mallas.level")
    #study_field_id=fields.Many2one("dara_mallas.study_field")
    #study_field_order_number=fields.Integer("Orden para malla",related="study_field_id.number", store=True)
    study_plan_id=fields.Many2one("dara_mallas.study_plan")
    #study_plan_period_id=fields.Char("periodo", related="study_plan_id.period_id.name")
    #study_plan_program_id=fields.Char("programa", related="study_plan_id.program_id.name")
    #organization_unit_id=fields.Many2one("dara_mallas.organization_unit") 
    #period_id=fields.Many2one("dara_mallas.period")
    
class study_plan_line_simple(models.Model):
    _name = "dara_mallas.study_plan_line_simple"

    period_id=fields.Many2one("dara_mallas.period")
    area_id=fields.Many2one("dara_mallas.area")
    period_subject_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char(related="subject_id.code")
 
    study_plan_id=fields.Many2one("dara_mallas.study_plan") 


   
class level(models.Model):
    _name="dara_mallas.level"
    
    name=fields.Char("Periodo")
    number=fields.Integer("Numero")

class campus(models.Model):
    _name="dara_mallas.campus"
    
    name=fields.Char("Nombre")
    code=fields.Char("Code")
  
    
    
    
