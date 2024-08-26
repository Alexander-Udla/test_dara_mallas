from email.mime import application
from ntpath import join
from odoo import models, api, fields
from odoo.exceptions import UserError
from io import BytesIO, StringIO
import io
import base64
from openpyxl import load_workbook
import pandas as pd
import logging
_logger = logging.getLogger(__name__)


class subject_create(models.Model):    
    
    _name="dara_mallas.subject_create"

    name=fields.Char("nombre del Archivo")
    state=fields.Selection([('pendiente','Pendiente'),('error','Error'),('aprobado','Aprobado')])
    csv_file=fields.Binary("Archivo de Carrera")
    name_file=fields.Char("nombre de archivo")
    result = fields.Text("Resultados")
    file_result=fields.Binary("Errores")
    name_file_result=fields.Char("nombre de archivo error") 
 

    
    def openfile(self):
       
        data =base64.b64decode(self.csv_file)
        xls_filelike = io.BytesIO(data)
        df = pd.read_excel(xls_filelike)
        for index,item in df.iterrows():
            #collage
            res = self.create_subject(item)
        
        
        
        errors = ""
        # Will print all the row values
        try:
            if res:
                self.write({
                                    'state':'aprobado',
                                })
            else:
                self.write({
                                    'state':'error',
                                    'file_result':base64.b64encode(errors.encode()) if errors else '',
                                    'name_file_result':'errores.txt' if errors else ''
                                })
                
        except Exception as e:
            self.write({
                                'state':'error',
                                'file_result':base64.b64encode(errors.encode()),
                                'name_file_result':'errores.txt'
                            })
    def create_subject(self,item):
        #clase
        try:
            facultad_code = "0"+str(item['CODIGO_FACULTAD']) if len(str(item['CODIGO_FACULTAD']))<=1 else item['CODIGO_FACULTAD']
            college = self.env['dara_mallas.college'].search([('code','=',facultad_code)]) 

            subject_class_name = self.env['dara_mallas.subject_class_name'].search([('name','=','Carrera')])

            #grade 
            grade = self.env['dara_mallas.grade'].search([('description','=',item['NIVEL_DE_SIGLA'])]) 
            
            #cprogram_code
            programa_code = self.env['dara_mallas.program_code'].search([('name','=',item['PROGRAMA'])],limit=1)
            
            #area
            area_code = item['CODIGO_AREA_CONOCIMIENTO'] if len(str(item['CODIGO_AREA_CONOCIMIENTO'])) ==3 else "0"+str(item['CODIGO_AREA_CONOCIMIENTO']) if len(str(item['CODIGO_AREA_CONOCIMIENTO']))==2 else "00"+str(item['CODIGO_AREA_CONOCIMIENTO']) if len(str(item['CODIGO_AREA_CONOCIMIENTO']))==1 else "000"
            area = self.env['dara_mallas.subject_department'].search([('code','=',area_code)]) 
            
            #UEC
            uec = self.env['dara_mallas.uec_credit'].search([('name','=',str(item['CREDITO_MINIMO']))]) 

            #cobro 
            cobro = self.env['dara_mallas.billed'].search([('name','=',str(item['COBRO_MINIMO']))])  
        
            #estatus
            status = self.env['dara_mallas.subject_status'].search([('name','=','Activo')])

            
            #tipo de hoaria
            var = ['TEO','PRA','PRS']
            d = []
            code = []
            sub = []
            uec_ = 0
            for x in var:
                schedule = self.env['dara_mallas.schedule_class'].search([('code','=',x)]) 
                d.append(schedule.id)
                code.append(schedule.code)
        
           
            #Subject Name
            subject_name = self.env['dara_mallas.subject_name']
            res = subject_name.search([('code','=',item['SUBJECT'])])
                    
            #period
            period = self.env['dara_mallas.period'].search([('name','=',item['PERIODO DE LA SIGLA'])])
         
                        
            #coordinador
            subject_owner = self.env['dara_mallas.coordinator'].search([('idbanner','=',item['COORDINADOR_SIGLA'])])
            if not subject_owner or item['COORDINADOR_SIGLA'] == None:
                error = "El Coordinador con "+str(item['COORDINADOR_SIGLA'])+" no existe en el sistema o no esta bien definida"
                #yield error
                    
            #ponderacion
            weighing = self.env['dara_mallas.weighing'].search([('code','=',item['PONDERACION'])])
            if not weighing or item['PONDERACION'] == None:
                error = "La ponderacion "+str(item['PONDERACION'])+" no existe en el sistema o no esta bien definida"
                #yield error

            #griup
            #group = self.env['dara_mallas.group_rule'].search([('name','=','A-100')])
                    
            #rule_min_score_id
            #rule = self.env['dara_mallas.rule_score'].search([('name','=',float(mat[31]))])
            #if not rule or mat[31] == None:
                #error = "La Calificación "+str(mat[31])+" no existe en el sistema o no esta bien definida"
                #yield error
                    
                    
                    #sub.append(str(res.code+str(mat[5])))
                    
            #modo calificacion
            grade_mode = self.env['dara_mallas.grade_mode'].search([('name','=',item['MODO_CALIFICACION'])])
            
            course = str(item['COURSE']) if len(str(item['COURSE']))==4 else "0"+str(item['COURSE']) if len(str(item['COURSE']))==3 else "00"+str(item['COURSE']) if len(str(item['COURSE']))==2 else "000"+str(item['COURSE']) if len(str(item['COURSE']))==1 else "0000"
            subject_code = str(item['SUBJECT'])+course
            subject = self.env['dara_mallas.subject'].search([('code', '=', subject_code)])
                
            if not subject:
                subject_create_new = self.env['dara_mallas.subject'].create({
                        'name':str(item['ASIGNATURA']).strip(),
                        'short_name':str(item['SIGLA']).strip(),
                        'new_subject':True,
                        'course_number':course,
                        'subject_name_id':res.id,
                        'code':subject_code,
                        #'subject_class_id':subject_class_name.id,
                        
                        })
                subject_scacrse_new = self.env['dara_mallas.subject_scacrse'].create({
                        'period_id':period.id,
                        'college_id':college.id,
                        'subject_id':subject_create_new.id,
                        'credits':item['OTRAS'],
                        'academic_hours':item['HORAS_DOCENCIA'],
                        'total_academic_hours':item['HORAS_DOCENCIA'],
                        'hybrid_academic_hours':item['HORAS_DOCENCIA_PRESENCIAL_H'],
                        'hybrid_total_academic_hours':int(item['HORAS_DOCENCIA_PRESENCIAL_H'])+int(item['HORAS_DOCENCIA_VIRTUAL_H'])+int(item['HORAS_LABORATORIO_DOCENCIA'])+int(item['HORAS_EXTERNADO_DOCENCIA_H']),
                        'hybrid_asisted_hours':int(item['HORAS_APLICACION_H'])+int(item['HORAS_PRACT_PREPROF_H'])+int(item['HORAS_SERVICIO_COMUNIDAD_H'])+int(item['HORAS_APLICACION_LAB_H']),
                        'hybrid_virtual_academic_hours':item['HORAS_DOCENCIA_VIRTUAL_H'],
                        'online_academic_hours':item['HORAS_DOCENCIA_O'],
                        'lab_practicing_hours':item['HORAS_LABORATORIO_DOCENCIA'],
                        'hybrid_lab_practicing_hours':item['HORAS_LABORATORIO_DOCENCIA_H'],
                        'externship_hours':item['HORAS_EXTERNADO_DOCENCIA'],
                        'hybrid_externship_hours':item['HORAS_EXTERNADO_DOCENCIA_H'],
                        'application_hours':item['HORAS_APLICACION'],
                        'hybrid_application_hours':item['HORAS_APLICACION_H'],
                        'online_application_hours':item['HORAS_APLICACION_O'],
                        'lab_application_hours':item['HORAS_APLICACION_LABORATORIO'],
                        'hybrid_lab_application_hours':item['HORAS_APLICACION_LAB_H'],
                        'online_lab_application_hours':item['HORAS_APLICACION_LAB_O'],
                        #'internship_hours':item['HORAS_PRACT_PREPROFESIONALES'],
                        'practicing_hours':item['HORAS_PRACT_PREPROFESIONALES'],
                        'hybrid_practicing_hours':item['HORAS_PRACT_PREPROF_H'],
                        'online_practicing_hours':item['HORAS_PRACT_PREPROF_O'],
                        'community_service_hours':item['HORAS_SERVICIO_COMUNIDAD'],
                        'hybrid_community_service_hours':item['HORAS_SERVICIO_COMUNIDAD_H'],
                        'online_community_service_hours':item['HORAS_SERVICIO_COMUNIDAD_O'],
                        'autonomus_hours':item['TOTAL_HORAS_AUTONOMAS'],
                        'hybrid_autonomus_hours':item['TOTAL_HORAS_AUTONOMAS_H'],
                        'online_autonomus_hours':item['TOTAL_HORAS_AUTONOMAS_O'],
                        'tit_hours':item['HORAS_TITULACION'],
                        'hybrid_tit_hours':item['HORAS_TITULACION_H'],
                        'online_tit_hours':item['HORAS_TITULACION_O'],
                        'teaching_sesions':item['SESIONES_DOCENCIA'],
                        'teaching_credits':item['OTRAS'],
                        #'asisted_hours':int(mat[13]if mat[13]!=None else 0)+int(mat[14]if mat[14]!=None else 0)+int(mat[17]if mat[17]!=None else 0),
                        'sesions':item['CONTACTO'],
                        'externship_sesions':item['SESIONES_EXTERNADO'],
                        'lab_sesions':item['SESIONES_LABORATORIO'],
                        'online_sesions':item['SESIONES_O'],
                        'externship_weeks':item['SEMANAS_EXTERNADO'],
                        'lab_weeks':item['SEMANAS_LABORATORIO'],
                        'additional_hours_whistle':item['HORAS_ADICIONALES_SILABO'],
                        'total_hours':item['TEORIA'],
                        'college_id': college.id,
                        'area_id':area.id,
                        'uec_credit_id': uec.id,
                        'billed_id': cobro.id,
                        'status_id': status.id,
                        'repeat_limit':item['LIMITE_REPETICIONES'],
                        'gpa':True,
                        'face_to_face' : True if int(item['HORAS_DOCENCIA']) != 0 or int(item['HORAS_PRACT_PREPROFESIONALES']) !=0 else False,
                        'hybrid' : True if (int(item['HORAS_DOCENCIA_PRESENCIAL_H']) != 0 and int(item['HORAS_DOCENCIA_VIRTUAL_H']) !=0 ) or int(item['HORAS_PRACT_PREPROF_H']) !=0 else False,
                        'online' : True if int(item['HORAS_DOCENCIA_O']) !=0 or int(item['HORAS_PRACT_PREPROF_O']) != 0 else False
                })
                subject_scadtl_new = self.env['dara_mallas.subject_scadtl'].create({

                        'subject_id':subject_create_new.id,
                        'period_id':period.id,
                        'coordinador_id':subject_owner.id,
                        'program_code_id': programa_code.id,
                        'weighing_id':weighing.id,

                })
                subject_schule_class_new = self.env['dara_mallas.schedule_class_line_subject'].create({
                    'subject_id':subject_create_new.id,
                    'period_id':period.id,
                    'schedule_class_line_ids':[ 
                            (0,0,{'schedule_class_id':d[0],'schedule_class_code':code[0]}),
                            (0,0,{'schedule_class_id':d[1],'schedule_class_code':code[1]}),
                            (0,0,{'schedule_class_id':d[2],'schedule_class_code':code[2]})
                            ],
                        #'grade_id':grade.id,
                    
                })
                subject_class_new = self.env['dara_mallas.subject_class'].create({
                    'subject_id':subject_create_new.id,
                    'subject_class_id':subject_class_name.id
                })
                        #tipo de calificacion
                subject_grade_new = self.env['dara_mallas.grade_mode_line_subject'].create({
                    'subject_id':subject_create_new.id,
                    'period_id':period.id,
                    
                })
                subject_grade_mode_line = self.env['dara_mallas.grade_mode_line'].create({
                    'grade_mode_id':grade_mode.id,
                    'grade_mode_line_subject_id':subject_grade_new.id
                })

                       
                        
                #nivel de sigla
                grade_line_subject_new = self.env['dara_mallas.grade_line_subject'].create({
                    'period_id':period.id,
                    'subject_id':subject_create_new.id,

                })
                grade_line_new = self.env['dara_mallas.grade_line'].create({
                    'grade_id':grade.id,
                    'grade_line_subject_id':grade_line_subject_new.id,

                })
                        #crear sigla con todos los componentes
                subject_inherit_new = self.env['dara_mallas.subject_inherit'].create(
                    {
                    'subject_id':subject_create_new.id,
                    'subject_scadtl_id':subject_scadtl_new.id,
                    'grade_mode_line_subject_id':subject_grade_new.id,
                    'schedule_class_line_subject_id':subject_schule_class_new.id,
                    'subject_scacrse_id':subject_scacrse_new.id,
                    'grade_line_subject_id':grade_line_subject_new.id
                    }
                )

                
                _logger.warning("La materia: "+subject_code+" fue creada con exito") 
            return True
            #self.create_study_plan(sheet_obj,max_col,college,grade,max_row,sub,program_code_,nam_career_,uec_,period,grade_,campus_,area_)            
        except Exception as e:
            print(e)
            return False
    
    def create_study_plan(self,sheet_object,max_col,collage,grade,max_row,sub,program_code_,nam_career_,uec_,period,grade_,campus_,area_):

        try:
            #Grado/Titulo
            grade_title = self.env['dara_mallas.banner_grade'].search([('name','=',grade_)])
            #campus
            campus = self.env['dara_mallas.campus'].search([('name','=',campus_)]) 
            #program
            program = self.env['dara_mallas.program'].search([('name','=',nam_career_)])
            #program code
            program_code = self.env['dara_mallas.program_code'].search([('name','=',program_code_)],limit=1)
            #print(program.name)
            study_plan_new =  self.env['dara_mallas.study_plan'].create({
                'college_id':collage.id,
                'period_id':period.id,
                'program_id':program.id,
                'program_codes_ids':[(6,0,[program_code.id])] ,
                'grade_id':grade.id,
                'hours_max':uec_,
                'hours_min':1,
                'banner_grade_id':grade_title.id,
                'campus_id':campus.id ,
                'state':'vigente'
            })
            _logger.warning("La malla: "+program.name+" fue creada con exito")
            self.add_subject(sub,period,nam_career_,area_,study_plan_new)
        except Exception as e:
            self.result = "La malla: "+program.name+" ya existe en el sistema"
            _logger.error("La malla: "+program.name+" ya existe en el sistema")
          
    def add_subject(self,subjects,period,nam_career_,area_,study_plan_):
        #program
        program = self.env['dara_mallas.program'].search([('name','=',nam_career_)])
        #study_plan
        study_plan = self.env['dara_mallas.study_plan'].search([('program_id', '=', program.id)])
        #study_plan
        level = self.env['dara_mallas.level'].search([('number', '=', 1)])

        #crear areas para studyplan
        are_homologation_new = self.env['dara_mallas.area_homologation'].create({
            'area_id':area_.id,
            'period_id':period.id
        })

        #for item in subjects:
           
        #agrega las areas a la malla
        study_plan_line_new = self.env['dara_mallas.study_plan_line'].create({
            'study_plan_id':study_plan_.id,
            'line_order':int(area_.code[-1:] if area_.code[-1:]!= 0 else area_.code[-2:]),
            'area_homologation_id':are_homologation_new.id
        })

       
        for item in subjects:
                try:
                    subject_inherit_area_new = self.env['dara_mallas.subject_inherit_area'].create({
                'subject_inherit_id':item.id,
                'area_homologation_id':are_homologation_new.id
            })
                    _logger.warning("La materia: "+item.name+" fue agregado correctacmente a "+program.name)
                except Exception as e:
                    self.result = "La materia: "+item.name+" fue NO agregado correctacmente a "+program.name
                    _logger.error("La materia: "+item.name+" fue NO agregado correctacmente a "+program.name)
                  
    def open_study_plan_create(self):
      
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dara_mallas.study_plan',
            'view_mode': 'tree,form',
            #'view_type': 'form',
            'target': 'concurrent',
            'name': 'Nuevo EDCO',
            'domain': [('program_id.name','=',self.name)],
            #'view_id': view_id,
            
        }              
        

       
                
    
    