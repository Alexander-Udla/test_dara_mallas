'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class subject_scacrse(models.Model):
    _name="dara_mallas.subject_scacrse"
    
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one('dara_mallas.subject')
    subject_code=fields.Char(related="subject_id.code")
    college_id=fields.Many2one("dara_mallas.college", string="Facultad / Escuela")
    area_id=fields.Many2one("dara_mallas.subject_department", string="Área de conocimiento")
    status_id=fields.Many2one("dara_mallas.subject_status","Estado")
    uec_credit_id=fields.Many2one("dara_mallas.uec_credit",'UEC o Credito')
    billed_id=fields.Many2one("dara_mallas.billed","Cobro")
    repeat_limit=fields.Integer("Limite repeticion")

    #======================================================
    #                      Componentes PRESENCIAL
    #======================================================
    face_to_face=fields.Boolean("Presencial")
    #Horas de docencia
    academic_hours=fields.Integer("H. academicas",track_visibility='always')
    lab_practicing_hours=fields.Integer("H. Practicas lab.",track_visibility='always')
    externship_hours=fields.Integer("Horas de externado")
    additional_hours_whistle = fields.Integer("Horas adicionales silabo")
    total_academic_hours=fields.Integer("Total Académicas Pre.")  #lab_practicing_hours+academic_hours+externship_hours

    #===========================================================================
    # HORAS ASISTIDAD=HORAS DE PRACTICAS+HORAS DE APLICACION + HORAS DE SERVICIO 
    # COMUNITARIO
    #===========================================================================
    #horas de aplicacion
    application_hours=fields.Integer("H. Aplicacion",track_visibility='always')
    practicing_hours=fields.Integer("H. Prac. Pre.",track_visibility='always')
    community_service_hours=fields.Integer("H. Ser. Com.",track_visibility='always')
    lab_application_hours=fields.Integer("H. Lab. Aplicacion",track_visibility='always')
    asisted_hours=fields.Integer("Total Asistido",track_visibility='always')

    #horas autonomas
    autonomus_hours=fields.Integer("Total Autonomo Pre.",track_visibility='always')
    learning_organization=fields.Char("Organización de aprendizaje",track_visibility='always')
    tit_hours=fields.Integer("Horas de titulacion",track_visibility='always')

    #======================================================
    #                      Componentes HIBRIDAS
    #======================================================
    hybrid=fields.Boolean("Híbrida")
    #horas docencia
    hybrid_academic_hours=fields.Integer("H. Docencia Presencial")
    hybrid_virtual_academic_hours=fields.Integer("H. Virtuales")
    hybrid_lab_practicing_hours=fields.Integer("H. laboratorio docencia ")
    hybrid_externship_hours=fields.Integer("H. Externado")
    hybrid_total_academic_hours=fields.Integer("Total Académicas Pre.")
    hybrid_additional_hours_whistle = fields.Integer("H. Horas adicionales silabo")
    hybrid_total_academic_hours=fields.Integer("Total Académicas Pre.")

    #horas aplicacion
    hybrid_application_hours=fields.Integer("H. de aplicación")
    hybrid_practicing_hours=fields.Integer("H. Prac. Pre.")
    hybrid_community_service_hours=fields.Integer("H. Ser. Com.")
    hybrid_lab_application_hours=fields.Integer("H. Lab. Aplicacion")
    hybrid_asisted_hours=fields.Integer("Total Asistido")
    
    #horas autonomas
    hybrid_autonomus_hours=fields.Integer("H. Autonomas")
    
    #horas titulacion
    hybrid_tit_hours=fields.Integer("H. Titulacion")

    #======================================================
    #                      Componentes ONLINE
    #======================================================
    online=fields.Boolean("On line")
    #horas docencia
    online_academic_hours=fields.Integer("H. Docencia Presencial")

    #horas aplicacion
    online_application_hours=fields.Integer("H. de aplicación")
    online_practicing_hours=fields.Integer("H. Prac. Pre.")
    online_community_service_hours=fields.Integer("H. Ser. Com.")
    online_lab_application_hours=fields.Integer("H. Lab. Aplicacion")
    online_asisted_hours=fields.Integer("Total Asistido")

    #HORAS AUTONOMAS
    online_autonomus_hours=fields.Integer("H. Autonomas")

    #SESIONES
    online_sesions=fields.Float("Sesiones")

    #HORAS TITULACION
    online_tit_hours=fields.Integer("H. Titulacion")
    #===========================================================================
    # HORAS TOTALES = ACADEMICAS + ASISTIDAS+ AUTONOMAS
    #===========================================================================
    total_hours=fields.Integer("Horas Totales")

    #===========================================================================
    # CREDITOS    
    #===========================================================================
    credits=fields.Float("Total Creditos",track_visibility='always')  #TOTAL DE CREDITOS
    teaching_credits=fields.Float("Creditos Docencia")
    externship_credits=fields.Float("Creditos Externado")
    lab_credits=fields.Float("Creditos laboratorios",track_visibility='always')
    #===========================================================================
    # SESIONES 
    #===========================================================================
    sesions=fields.Float("Sesiones",track_visibility='always') #TOTAL DE SESIONES
    teaching_sesions=fields.Float("Sesiones docencia")
    externship_sesions=fields.Float("Sesiones externado")
    lab_sesions=fields.Float("Sesiones laboratorio")

    #internado y externado
    externship_hours=fields.Integer("Horas de externado")
    internship_hours=fields.Integer("Horas de internado")
    
    #===========================================================================
    # SEMANAS EXTERNADO Y LABORATORIO
    #===========================================================================
    externship_weeks=fields.Integer("Semanas Externado")
    lab_weeks=fields.Integer("Semanas Laboratorio")

    #MENSAJE DE ERROR
    hours_validation=fields.Char("Validacion")

    #@api.constrains('subject_id','period_id')
    def save(self):
       
        #for record in self:
        scacrse = self.env['dara_mallas.subject_scacrse'].search([])
        cis = [str(item.subject_id.code)+str(item.period_id.name) for item in scacrse]
       
        #print(cis.count(str(self.subject_id.code)+str(self.period_id.name)))
        if cis.count(str(self.subject_id.code)+str(self.period_id.name))>1:
            raise ValidationError("ya existe el registro "+str(self.subject_id.code)+str(self.period_id.name))


    @api.onchange('practicing_hours','application_hours','community_service_hours','lab_application_hours') 
    def onchange_asisted_hours(self):
        self.asisted_hours=self.practicing_hours+self.application_hours+self.community_service_hours+self.lab_application_hours       
        self.check_total_hours()
    @api.onchange('academic_hours','lab_practicing_hours','externship_hours') 
    def onchange_academic_face_to_face_hours(self):
        self.total_academic_hours=self.academic_hours+self.lab_practicing_hours+self.externship_hours
        self.check_total_hours()
    
    @api.onchange('hybrid','online','face_to_face') 
    def onchange_type(self):
        self.check_total_hours()

    @api.onchange('hybrid_academic_hours','hybrid_virtual_academic_hours','hybrid_lab_practicing_hours','hybrid_externship_hours')
    def onchange_academic_hybrid_hours(self):
        self.hybrid_total_academic_hours=self.hybrid_academic_hours+self.hybrid_virtual_academic_hours+self.hybrid_lab_practicing_hours+self.hybrid_externship_hours
        self.check_total_hours()
    @api.onchange('hybrid_practicing_hours','hybrid_application_hours','hybrid_community_service_hours','hybrid_lab_application_hours') 
    def onchange_hybrid_asisted_hours(self):
        self.hybrid_asisted_hours=self.hybrid_practicing_hours+self.hybrid_application_hours+self.hybrid_community_service_hours+self.hybrid_lab_application_hours       
        self.check_total_hours()
    @api.onchange('online_practicing_hours','online_application_hours','online_community_service_hours','online_lab_application_hours') 
    def onchange_online_asisted_hours(self):
        self.online_asisted_hours=self.online_practicing_hours+self.online_application_hours+self.online_community_service_hours+self.online_lab_application_hours       
        self.check_total_hours()
        
    @api.onchange('hybrid_autonomus_hours','online_academic_hours','online_autonomus_hours','autonomus_hours','total_hours')
    def onchange_single_field_hours(self):
        self.check_total_hours()

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result

    def check_total_hours(self):
        errors=''
        if self.face_to_face :
            if self.total_academic_hours+self.asisted_hours+self.autonomus_hours != self.total_hours:
                errors+=' Presencial '
        if self.hybrid:
            if self.hybrid_total_academic_hours+self.hybrid_asisted_hours+self.hybrid_autonomus_hours != self.total_hours:
                errors+=' Híbridas '
        if self.online:
            if self.online_academic_hours+self.online_asisted_hours+self.online_autonomus_hours != self.total_hours:
                errors+=' Online '
        if errors:
            self.hours_validation="Errores en "+errors    
        else:
            self.hours_validation=""