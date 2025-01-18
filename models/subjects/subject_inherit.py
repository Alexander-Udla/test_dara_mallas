

from odoo import fields, models, api
#from  dara_mallas import subject_scadtl
class subject_inherit(models.Model):
    _name="dara_mallas.subject_inherit"

    _inherit = [#'dara_mallas.subject',
    #'dara_mallas.subject_scadtl',
    #'dara_mallas.subject_scacrse',
    #'dara_mallas.prerequisite_line'
    ]

    _columns = {
       
    }
    #subject
    subject_id = fields.Many2one("dara_mallas.subject")
    name=fields.Char(related="subject_id.name")
    name_en=fields.Char(related="subject_id.name_en") 
    short_name=fields.Char(related="subject_id.short_name")
    code=fields.Char(related="subject_id.code")
    course_number=fields.Char(related="subject_id.course_number")
    subject_name_id=fields.Many2one(related="subject_id.subject_name_id")
    new_subject=fields.Boolean(related="subject_id.new_subject")
    subject_class_ids=fields.One2many(related="subject_id.subject_class_ids")
     
    #scadtl
    subject_scadtl_id = fields.Many2one("dara_mallas.subject_scadtl")
    scadt_subject_id=fields.Many2one(related='subject_scadtl_id.subject_id')
    scadt_weighing_id=fields.Many2one(related='subject_scadtl_id.weighing_id')
    scadt_coordinador_id = fields.Many2one(related='subject_scadtl_id.coordinador_id')
    scadt_program_code_id = fields.Many2one(related='subject_scadtl_id.program_code_id')
    scadt_period_id=fields.Many2one(related="subject_scadtl_id.period_id")
    
    #modo calificacion 
    grade_mode_line_subject_id = fields.Many2one("dara_mallas.grade_mode_line_subject",string="Modo de Califición")
    grade_mode_line_ids = fields.One2many(related="grade_mode_line_subject_id.grade_mode_line_ids")
    
    #nivel de sigla
    grade_line_subject_id = fields.Many2one("dara_mallas.grade_line_subject",string="Nivel de Sigla")
    grade_line_ids = fields.One2many(related="grade_line_subject_id.grade_line_ids")
 
    #tipo de horario
    schedule_class_line_subject_id = fields.Many2one("dara_mallas.schedule_class_line_subject",string="Tipo de Horario")
    schedule_class_line_ids = fields.One2many(related="schedule_class_line_subject_id.schedule_class_line_ids")
    schedule_class_line_period_id=fields.Many2one(related="schedule_class_line_subject_id.period_id",string="Periodo")

    #scacrs
    subject_scacrse_id=fields.Many2one("dara_mallas.subject_scacrse")
    scad_period_id=fields.Many2one(related="subject_scacrse_id.period_id")
    scad_subject_id=fields.Many2one(related='subject_scacrse_id.subject_id')
    scad_college_id=fields.Many2one(related="subject_scacrse_id.college_id")
    scad_area_id=fields.Many2one(related="subject_scacrse_id.area_id")
    scad_status_id=fields.Many2one(related="subject_scacrse_id.status_id")
    scad_uec_credit_id=fields.Many2one(related="subject_scacrse_id.uec_credit_id")
    scad_billed_id=fields.Many2one(related="subject_scacrse_id.billed_id")
    scad_repeat_limit=fields.Integer(related="subject_scacrse_id.repeat_limit")
    scad_gpa=fields.Boolean(related="subject_scacrse_id.gpa")

    #====================================================== 
    #                      Componentes PRESENCIAL
    #======================================================
    scad_face_to_face=fields.Boolean(related="subject_scacrse_id.face_to_face")
    #Horas de docencia
    scad_academic_hours=fields.Integer(related="subject_scacrse_id.academic_hours",track_visibility='always')
    scad_lab_practicing_hours=fields.Integer(related="subject_scacrse_id.lab_practicing_hours",track_visibility='always')
    scad_externship_hours=fields.Integer(related="subject_scacrse_id.externship_hours")
    scad_additional_hours_whistle = fields.Integer(related="subject_scacrse_id.additional_hours_whistle")
    scad_total_academic_hours=fields.Integer(related="subject_scacrse_id.total_academic_hours")  #lab_practicing_hours+academic_hours+externship_hours

    #===========================================================================
    # HORAS ASISTIDAD=HORAS DE PRACTICAS+HORAS DE APLICACION + HORAS DE SERVICIO 
    # COMUNITARIO
    #===========================================================================
    #horas de aplicacion
    scad_application_hours=fields.Integer(related="subject_scacrse_id.application_hours",track_visibility='always')
    scad_practicing_hours=fields.Integer(related="subject_scacrse_id.practicing_hours",track_visibility='always')
    scad_community_service_hours=fields.Integer(related="subject_scacrse_id.community_service_hours",track_visibility='always')
    scad_lab_application_hours=fields.Integer(related="subject_scacrse_id.lab_application_hours",track_visibility='always')
    scad_asisted_hours=fields.Integer(related="subject_scacrse_id.asisted_hours",track_visibility='always')
    scad_externship_application_hours=fields.Integer(related="subject_scacrse_id.externship_application_hours",track_visibility='always')

    #horas autonomas
    scad_autonomus_hours=fields.Integer(related="subject_scacrse_id.autonomus_hours",track_visibility='always')
    scad_learning_organization=fields.Char(related="subject_scacrse_id.learning_organization",track_visibility='always')
    scad_tit_hours=fields.Integer(related="subject_scacrse_id.tit_hours",track_visibility='always')

    #======================================================
    #                      Componentes HIBRIDAS
    #======================================================
    scad_hybrid=fields.Boolean(related="subject_scacrse_id.hybrid")
    #horas docencia
    scad_hybrid_academic_hours=fields.Integer(related="subject_scacrse_id.hybrid_academic_hours")
    scad_hybrid_virtual_academic_hours=fields.Integer(related="subject_scacrse_id.hybrid_virtual_academic_hours")
    scad_hybrid_lab_practicing_hours=fields.Integer(related="subject_scacrse_id.hybrid_lab_practicing_hours")
    scad_hybrid_externship_hours=fields.Integer(related="subject_scacrse_id.hybrid_externship_hours")
    scad_hybrid_total_academic_hours=fields.Integer(related="subject_scacrse_id.hybrid_total_academic_hours")
    scad_hybrid_additional_hours_whistle = fields.Integer(related="subject_scacrse_id.hybrid_additional_hours_whistle")
    scad_hybrid_total_academic_hours=fields.Integer(related="subject_scacrse_id.hybrid_total_academic_hours")

    #horas aplicacion
    scad_hybrid_application_hours=fields.Integer(related="subject_scacrse_id.hybrid_application_hours")
    scad_hybrid_practicing_hours=fields.Integer(related="subject_scacrse_id.hybrid_practicing_hours")
    scad_hybrid_community_service_hours=fields.Integer(related="subject_scacrse_id.hybrid_community_service_hours")
    scad_hybrid_lab_application_hours=fields.Integer(related="subject_scacrse_id.hybrid_lab_application_hours")
    scad_hybrid_asisted_hours=fields.Integer(related="subject_scacrse_id.hybrid_asisted_hours")
    
    #horas autonomas
    scad_hybrid_autonomus_hours=fields.Integer(related="subject_scacrse_id.hybrid_autonomus_hours")
    
    #horas titulacion
    scad_hybrid_tit_hours=fields.Integer(related="subject_scacrse_id.hybrid_tit_hours")

    #======================================================
    #                      Componentes ONLINE
    #======================================================
    scad_online=fields.Boolean(related="subject_scacrse_id.online")
    #horas docencia
    scad_online_academic_hours=fields.Integer(related="subject_scacrse_id.online_academic_hours")

    #horas aplicacion
    scad_online_application_hours=fields.Integer(related="subject_scacrse_id.online_application_hours")
    scad_online_practicing_hours=fields.Integer(related="subject_scacrse_id.online_practicing_hours")
    scad_online_community_service_hours=fields.Integer(related="subject_scacrse_id.online_community_service_hours")
    scad_online_lab_application_hours=fields.Integer(related="subject_scacrse_id.online_lab_application_hours")
    scad_online_asisted_hours=fields.Integer(related="subject_scacrse_id.online_asisted_hours")

    #HORAS AUTONOMAS
    scad_online_autonomus_hours=fields.Integer(related="subject_scacrse_id.online_autonomus_hours")

    #SESIONES
    scad_online_sesions=fields.Float(related="subject_scacrse_id.online_sesions")

    #HORAS TITULACION
    scad_online_tit_hours=fields.Integer(related="subject_scacrse_id.online_tit_hours")
    #===========================================================================
    # HORAS TOTALES = ACADEMICAS + ASISTIDAS+ AUTONOMAS
    #===========================================================================
    scad_total_hours=fields.Integer(related="subject_scacrse_id.total_hours")

    #===========================================================================
    # CREDITOS    
    #===========================================================================
    scad_credits=fields.Float(related="subject_scacrse_id.credits",track_visibility='always')  #TOTAL DE CREDITOS
    scad_teaching_credits=fields.Float(related="subject_scacrse_id.teaching_credits")
    scad_externship_credits=fields.Float(related="subject_scacrse_id.externship_credits")
    scad_lab_credits=fields.Float(related="subject_scacrse_id.lab_credits",track_visibility='always')
    #===========================================================================
    # SESIONES 
    #===========================================================================
    scad_sesions=fields.Float(related="subject_scacrse_id.sesions",track_visibility='always') #TOTAL DE SESIONES
    scad_teaching_sesions=fields.Float(related="subject_scacrse_id.teaching_sesions")
    scad_externship_sesions=fields.Float(related="subject_scacrse_id.externship_sesions")
    scad_lab_sesions=fields.Float(related="subject_scacrse_id.lab_sesions")

    #internado y externado
    scad_externship_hours=fields.Integer(related="subject_scacrse_id.externship_hours")
    scad_internship_hours=fields.Integer(related="subject_scacrse_id.internship_hours")
    
    #===========================================================================
    # SEMANAS EXTERNADO Y LABORATORIO
    #===========================================================================
    scad_externship_weeks=fields.Integer(related="subject_scacrse_id.externship_weeks")
    scad_lab_weeks=fields.Integer(related="subject_scacrse_id.lab_weeks")

    #MENSAJE DE ERROR
    scad_hours_validation=fields.Char(related="subject_scacrse_id.hours_validation")

    # opciones adicionales
    itinerary=fields.Boolean(related="subject_scacrse_id.itinerary",string="Itinerario",track_visibility='always')
    elective=fields.Boolean(related="subject_scacrse_id.elective",string="Electiva",track_visibility='always')
    #===================================================================
    #   para identificar las asignaturas que son requisitos de graduación
    #==================================================================
    is_requisite_graduation = fields.Boolean(related="subject_scacrse_id.is_requisite_graduation",string="Requisito de graduación", default=False,track_visibility='always')
    is_web = fields.Boolean(related="subject_scacrse_id.is_web",string="Mostrar en Malla", default=True,track_visibility='always')

    
    #prerequisitos
    prerequisite_line_id=fields.Many2one("dara_mallas.prerequisite_line")
    preq_period_id=fields.Many2one(related="prerequisite_line_id.period_id")
    preq_subject_id=fields.Many2one(related='prerequisite_line_id.subject_id')
    preq_subject_code=fields.Char(related='prerequisite_line_id.subject_id.code')
    preq_subject_prerequisite_ids = fields.One2many(related="prerequisite_line_id.subject_prerequisite_ids")


    #correquisitos
    corequisite_line_id=fields.Many2one("dara_mallas.corequisite_line")
    core_period_id=fields.Many2one(related="corequisite_line_id.period_id")
    core_subject_id=fields.Many2one(related='corequisite_line_id.subject_id')
    core_subject_code=fields.Char(related='corequisite_line_id.subject_id.code')
    core_corequisite_ids = fields.One2many(related="corequisite_line_id.corequisite_ids")

    #reglas de homologacion
    subject_inherit_homologation_ids = fields.One2many("dara_mallas.subject_inherit_homologation",inverse_name ="subject_inherit_id")  

    #itinerarios
    itinerary_id=fields.Many2one("dara_mallas.itinerary_line")
    itin_period_id=fields.Many2one(related="itinerary_id.period_id")
    itin_subject_id=fields.Many2one(related='itinerary_id.subject_id')
    itin_subject_code=fields.Char(related='itinerary_id.subject_id.code')
    itin_itinerary_ids = fields.One2many(related="itinerary_id.itinerary_ids")  

    #electivas
    elective_id=fields.Many2one("dara_mallas.elective_line")
    elec_period_id=fields.Many2one(related="elective_id.period_id")
    elec_subject_id=fields.Many2one(related='elective_id.subject_id')
    elec_subject_code=fields.Char(related='elective_id.subject_id.code')
    elec_elective_ids = fields.One2many(related="elective_id.elective_ids")
    

    #atributos
    subject_attributes_id=fields.Many2one("dara_mallas.subject_attributes_subject")
    attr_period_id=fields.Many2one(related="subject_attributes_id.period_id")
    attr_subject_id=fields.Many2one(related='subject_attributes_id.subject_id')
    attr_subject_code=fields.Char(related='subject_attributes_id.subject_id.code')
    attr_subject_attributes_line_ids = fields.One2many(related="subject_attributes_id.subject_attributes_line_ids")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

   

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s ' % (str(rec.subject_id.code),str(rec.subject_id.name))))
        return result

    

            

class subject_inherit_area(models.Model):
    _name="dara_mallas.subject_inherit_area"

    _order="line_order asc"
    subject_inherit_id=fields.Many2one("dara_mallas.subject_inherit")
    subject_id=fields.Many2one(related="subject_inherit_id.subject_id")
    subject_code=fields.Char(related="subject_inherit_id.subject_id.code")
    subject_name=fields.Char(related="subject_inherit_id.subject_id.name")
    subject_scarse_period_id=fields.Many2one(related="subject_inherit_id.scad_period_id")
    line_order=fields.Integer("No.")
    study_field_id=fields.Many2one("dara_mallas.study_field")
    organization_unit_id=fields.Many2one("dara_mallas.organization_unit")
    #reverse name
    area_homologation_id = fields.Many2one("dara_mallas.area_homologation")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def name_get(self): 
        result = [] 
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_code),str(rec.subject_name))))
        return result
class subject_inherit_homologation(models.Model):
    _name="dara_mallas.subject_inherit_homologation"
 

    subject_rule_id=fields.Many2one("dara_mallas.subject_rule")
    homo_period_id=fields.Many2one(related="subject_rule_id.period_id")
    homo_subject_id=fields.Many2one(related='subject_rule_id.subject_id')
    homo_subject_code=fields.Char(related='subject_rule_id.subject_id.code')
    homo_area_id=fields.Many2one(related='subject_rule_id.area_id')
    homo_subject_homologation_ids = fields.One2many(related="subject_rule_id.subject_homologation_ids")

    #reverse name
    subject_inherit_id = fields.Many2one("dara_mallas.subject_inherit")
    # relacion con la ficha de asignatura historica
    subject_inherit_history_id = fields.Many2one('dara_mallas.subject_inherit_history')
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

class subject_inherit_area_history(models.Model):
    _name="dara_mallas.subject_inherit_area_history"

    _order="line_order asc"
    # relacion con fichas de asignatura historicas
    subject_inherit=fields.Many2one("dara_mallas.subject_inherit")
    subject_id=fields.Many2one(related="subject_inherit.subject_id")
    subject_code=fields.Char(related="subject_inherit.subject_id.code")
    subject_name=fields.Char(related="subject_inherit.subject_id.name")
    #subject_scarse_period_id=fields.Many2one(related="subject_inherit_id.scad_period_id")
    line_order=fields.Integer("No.")
    study_field_id=fields.Many2one("dara_mallas.study_field")
    organization_unit_id=fields.Many2one("dara_mallas.organization_unit")
  
    #relacion reversa con el modelo del area_homo_history
    area_homologation_history_id = fields.Many2one("dara_mallas.area_homologation_history")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
 