from odoo import fields, models,api
from odoo.exceptions import UserError
import base64
class area(models.Model):
    _name="dara_mallas.area"
    
    name=fields.Char("Nombre")
    code=fields.Char("Codigo")
 

class area_homologation(models.Model):
    _name="dara_mallas.area_homologation"
    
    period_id=fields.Many2one("dara_mallas.period")
    area_id=fields.Many2one("dara_mallas.area")
    dinamic=fields.Boolean("Areas Dinamicas",default=False)
    subject_inherit_area_ids = fields.One2many("dara_mallas.subject_inherit_area",inverse_name="area_homologation_id",string="Asignaturas")

    # campos que almacenarán el reporte
    file=fields.Binary("Reporte")
    file_name=fields.Char("Reporte de cambios")

    history_ids = fields.One2many('dara_mallas.area_homologation_history', 'area_homologation_id', string='Historial de Homologación')


    #@api.onchange('subject_inherit_area_ids') 
    def onchange_subject_inherit_area_ids(self):
        
        if not self.dinamic:
            for item in self.subject_inherit_area_ids:
                subject_inherit = self.env['dara_mallas.subject_inherit'].search([('id','=',item.subject_inherit_id.id)])
                if subject_inherit:
                    exists = False
                    objects = []
                    for subject in subject_inherit.subject_inherit_homologation_ids:
                        if subject.homo_area_id.id == self.area_id.id:
                            exists = True
                    if not exists:
                        subject_rule_id = self.env['dara_mallas.subject_rule'].search([('area_id.id','=',self.area_id.id),('subject_id.id','=',subject_inherit.subject_id.id)])
                        if subject_rule_id:
                            variable = subject_inherit.subject_inherit_homologation_ids
                            subject_inherit.subject_inherit_homologation_ids = [(6,0,[])]
                            for item in variable:
                                pre = {
                            'subject_rule_id':item.subject_rule_id.id,
                            'subject_inherit_id':subject_inherit.id,
                                }
                                object_create = self.env['dara_mallas.subject_inherit_homologation'].create(pre)
                                objects.append(object_create.id)
                            subject_rule_id = self.env['dara_mallas.subject_rule'].search([('area_id.id','=',self.area_id.id),('subject_id.id','=',subject_inherit.subject_id.id)])
                            pre = {
                        'subject_rule_id':subject_rule_id.id,
                        'subject_inherit_id':subject_inherit.id,
                            }
                            object_create = self.env['dara_mallas.subject_inherit_homologation'].create(pre)
                            objects.append(object_create.id)
                        else:
                            raise UserError("""La asignatura %s en el area %s no tiene reglas de homologacion \n crear en /asginaturas/reglas """%(subject_inherit.subject_id.code,self.area_id.name))     

    def copy(self,default=None):

        if default is None:
            default = {}
        new_object=super(area_homologation,self).copy(default=default)
        objects = []
        for item in self.subject_inherit_area_ids:
            pre = {
                'subject_inherit_id':item.subject_inherit_id.id,
                'line_order':item.line_order,
                'study_field_id':item.study_field_id.id,
                'organization_unit_id':item.organization_unit_id.id,
                'area_homologation_id':new_object.id,
            }
            object_create = self.env['dara_mallas.subject_inherit_area'].create(pre)
            objects.append(object_create.id)
        new_object.subject_inherit_area_ids=[(6,0,objects)]
        return new_object

    def copy_rules(self):
        subject_rule_new = []
        for item in self.subject_inherit_area_ids:
            subject_rule_all = self.env['dara_mallas.subject_rule'].search([
                ('subject_id','=',item.subject_id.id),
                ('area_id','=',self.area_id.id),
                ])
            if subject_rule_all:
                period_max = max(subject_rule_all, key=lambda rule: rule.period_id.name)
                subject_rule = self.env['dara_mallas.subject_rule'].search([
                    ('subject_id','=',item.subject_id.id),
                    ('area_id','=',self.area_id.id),
                    ('period_id','=',period_max.period_id.id),
                    ],limit=1)
                
                subject_rule = self.env['dara_mallas.subject_rule'].search([
                    ('id','=',subject_rule.id),
                    ])
                if self.period_id.name != subject_rule.period_id.name:
                    subject_rule_new_create = subject_rule.copy({'period_id':self.period_id.id})
                    subject_rule_new.append(subject_rule_new_create)
            else:
                subject_rule_all = self.env['dara_mallas.subject_rule'].search([
                ('subject_id','=',item.subject_id.id),
                ])
                if subject_rule_all:
                    period_max = max(subject_rule_all, key=lambda rule: rule.period_id.name)
                    subject_rule = self.env['dara_mallas.subject_rule'].search([
                        ('subject_id','=',item.subject_id.id),
                        ('period_id','=',period_max.period_id.id),
                        ],limit=1)
                    
                    subject_rule = self.env['dara_mallas.subject_rule'].search([
                        ('id','=',subject_rule.id),
                        ])
                    subject_rule_new_create = subject_rule.copy({'area_id':self.area_id.id,'period_id':self.period_id.id})
                    subject_rule_new.append(subject_rule_new_create)
                else:
                    object = {
                        'subject_id':item.subject_id.id,
                        'area_id':self.area_id.id,
                        'period_id':self.period_id.id

                    }
                    object_create = self.env['dara_mallas.subject_rule'].create(object)
                    subject_rule_new.append(object_create)

        #print("Reglas nuevas:", subject_rule_new)
        #buscar ficha
        for subject in subject_rule_new:
            subject_inherit_homologations = []
            subject_inherit = self.env['dara_mallas.subject_inherit'].search([
                        ('subject_id','=',subject.subject_id.id),
                        ])
            for subject_homologation in subject_inherit.subject_inherit_homologation_ids:
                #valida si la regla nueva esta en la misma area
                if subject_homologation.subject_rule_id.area_id.id != subject.area_id.id:
                    subject_inherit_homologations.append((0,0,{'subject_rule_id':subject_homologation.subject_rule_id.id}))
                else:
                    valida_study_plan_stop_new = self.stop_study_plan_flag(subject.area_id,subject)
                    #print(f"{subject.area_id.display_name} MC:",valida_study_plan_stop_new)
                    if not valida_study_plan_stop_new:
                        print("Periodo regla nueva", subject_homologation.subject_rule_id.period_id.name)
                        print("Periodo regla antigua",subject.period_id.name)
                        #comprueba que sea del mismo area y que este en una malla congelada
                        valida_study_plan_stop = self.is_stop_study_plan_area(subject_homologation.subject_rule_id.area_id,subject_homologation.subject_rule_id)
                        if subject_homologation.subject_rule_id.area_id.id == subject.area_id.id and valida_study_plan_stop:#revisar error
                            subject_inherit_homologations.append((0,0,{'subject_rule_id':subject_homologation.subject_rule_id.id}))
                        if subject_homologation.subject_rule_id.area_id.id == subject.area_id.id and subject_homologation.subject_rule_id.period_id.name > subject.period_id.name and not valida_study_plan_stop:#revisar error
                            subject_inherit_homologations.append((0,0,{'subject_rule_id':subject_homologation.subject_rule_id.id}))    
                    # cuando es malla congelada
                    else:
                        #if subject_homologation.subject_rule_id.area_id.id == subject.area_id.id and subject_homologation.subject_rule_id.period_id.name >subject.period_id.name:
                        if subject_homologation.subject_rule_id.area_id.id == subject.area_id.id and subject_homologation.subject_rule_id.period_id.name >subject.period_id.name:               
                            subject_inherit_homologations.append((0,0,{'subject_rule_id':subject_homologation.subject_rule_id.id}))

                        
                        
            subject_inherit_homologations.append((0,0,{'subject_rule_id':subject.id}))
            for modelo_subject in subject_inherit:
                modelo_subject.write({'subject_inherit_homologation_ids': [(5,)]})
                modelo_subject.write({
                        'subject_inherit_homologation_ids':subject_inherit_homologations

                    })


        print(subject_rule_new)
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.area_id.name),str(rec.period_id.name))))
        return result

    def is_stop_study_plan_area(self, area,rule,new=False):#regla
        """
        Validar si el área está dentro de una malla congelada
        """
        if area.name[0].isalpha():
            search_string = area.name[1:3]
        else:
            search_string = area.name[0:3]

        program_code = self.env['dara_mallas.program_code'].search([
            ('name', 'like', '%%%s' % search_string)
        ])

        for code in program_code:
            programs = self.env['dara_mallas.program'].search([
                ('id', '=', code.program_id.id)
            ])
            for program in programs:
                study_plans = self.env['dara_mallas.study_plan'].search([
                    ('program_id', '=', program.id)
                ])
                for study_plan in study_plans:
                    if study_plan.period_id.name <= rule.period_id.name:
                        for plan_line in study_plan.study_plan_lines_ids:
                            #if area.id == plan_line.area_homologation_id.area_id.id and study_plan.study_plan_stop: #subject_inherit_area_ids
                            if not new:
                                for subject_inherit in plan_line.area_homologation_id.subject_inherit_area_ids:
                                    for subject_rule_si in subject_inherit.subject_inherit_id.subject_inherit_homologation_ids:
                                        if subject_rule_si.subject_rule_id.id == rule.id and rule.area_id.id == plan_line.area_homologation_id.area_id.id and study_plan.study_plan_stop and study_plan.period_id.name>=rule.period_id.name:
                                            return True
                            else: 
                                # area.id == plan_line.area_homologation_id.area_id.id
                                if area.id == plan_line.area_homologation_id.area_id.id and study_plan.study_plan_stop:
                                    return True
        return False



    def stop_study_plan_flag(self, area, rule):
        """
        Validar si el area y regla están dentro de una malla congelada
        """
        if area.name[0].isalpha():
            search_string = area.name[1:3]
        else:
            search_string = area.name[0:3]

        program_code = self.env['dara_mallas.program_code'].search([
            ('name', 'like', '%%%s' % search_string)
        ])

        for code in program_code:
            programs = self.env['dara_mallas.program'].search([
                ('id', '=', code.program_id.id)
            ])
            for program in programs:
                study_plans = self.env['dara_mallas.study_plan'].search([
                    ('program_id', '=', program.id)
                ])
                # entro al area
                # busco area_homologation con esa area id
                # si dentro de esa area homologation esta la regla y la malla en donde esta esa area homologation es congelada return True
                # periodo menor o igual de las areas 
                for study_plan in study_plans:
                    for plan_line in study_plan.study_plan_lines_ids:
                            for subject_inherit in plan_line.area_homologation_id.subject_inherit_area_ids:
                                for subject_rule_si in subject_inherit.subject_inherit_id.subject_inherit_homologation_ids:
                                    # valida que la regla es la misma, que esté en el área actual, que la malla sea congelada y que la regla esté en un período menor al de la malla
                                    if subject_rule_si.subject_rule_id.id == rule.id and rule.area_id.id == plan_line.area_homologation_id.area_id.id and rule.period_id.name <= study_plan.period_id.name and study_plan.study_plan_stop:
                                        print(f"{study_plan.display_name} es Malla congelada")
                                        return True
        print(f"{study_plan.display_name} No es malla congelada")
        return False

    def compare_with_area_instance(self):
        """
        Comparar con el área que tenga el período menor al último registro, pero que sea el máximo entre los registros existentes.
        """
        current_areas = self.search([('area_id', '=', self.area_id.id)])

        current_period = self.period_id.name

        period_max = None 

        for area in current_areas:
            period = area.period_id.name
            if period < current_period and (period_max is None or period > period_max):
                period_max = period

        if period_max is None:
            print("No existe un período menor para realizar la comparativa.")
        
        last_area_max_period = self.search([
            ('area_id', '=', self.area_id.id),
            ('period_id', '=', period_max)
        ], limit=1)

        if not last_area_max_period:
            self.file = None
            self.file_name = ""
            raise UserError(f"No existe un período anterior al {self.period_id.name} con el cual realizar la comparativa.")
            
        else:

            existing_area_subject_ids = set(subject.subject_inherit_id.id for subject in self.subject_inherit_area_ids)

            previous_record_subject_ids = set(subject.subject_inherit_id.id for subject in last_area_max_period.subject_inherit_area_ids)


            removed_subject_ids = existing_area_subject_ids - previous_record_subject_ids

            added_subject_ids = previous_record_subject_ids - existing_area_subject_ids

            # Obtener los nombres de las asignaturas eliminadas
            removed_subject_names = []
            for subject_id in removed_subject_ids:
                    subject = self.env['dara_mallas.subject_inherit'].search([('id', '=', subject_id)])
                    if subject:
                        removed_subject_names.append(subject.display_name)
            # Obtener los nombres de las asignaturas añadidas
            added_subject_names = []
            for subject_id in added_subject_ids:
                    subject = self.env['dara_mallas.subject_inherit'].search([('id', '=', subject_id)])
                    if subject:
                        added_subject_names.append(subject.display_name)

            if len(added_subject_names) == 0 and len(removed_subject_names) == 0:
                differences_text = f"Período nuevo:{self.period_id.display_name}\nÁrea {self.area_id.display_name} \nPeríodo anterior:{last_area_max_period.period_id.display_name} \nNo se registran cambios."
                                
                # Escribir el contenido del archivo de texto en el campo 'file' del objeto actual
                self.write({
                        'file': base64.b64encode(differences_text.encode()),
                        'file_name': 'reporte.txt'
                    })
            else:
                # Unir las dos listas en una cadena de texto
                differences_text = f"Período nuevo:{self.period_id.display_name}\nÁrea {self.area_id.display_name} \nPeríodo anterior:{last_area_max_period.period_id.display_name} \n"
                for removed_subject in removed_subject_names:
                        differences_text += f"Asignatura(s) añadida(s): {removed_subject}\n"
                for added_subject in added_subject_names:
                        differences_text += f"Asignatura(s) eliminada(s): {added_subject}\n"
                    
                # Escribir el contenido del archivo de texto en el campo 'file' del objeto actual
                self.write({
                        'file': base64.b64encode(differences_text.encode()),
                        'file_name': 'reporte.txt'
                    })

    def compare_area_with_area_hist(self, area_record):
        """
        Comparar con el área que tenga el período menor al último registro, pero que sea el máximo entre los registros existentes.
        """
        current_areas = self.search([('area_id', '=', area_record.area_id.id)])

        current_period = area_record.period_id.name

        period_max = None 

        for area in current_areas:
            period = area.period_id.name
            if period < current_period and (period_max is None or period > period_max):
                period_max = period

        if period_max is None:
            return f"No existe un período menor para realizar la comparativa para el área {area_record.area_id.display_name}.\n"

        last_area_max_period = self.search([
            ('area_id', '=', area_record.area_id.id),
            ('period_id', '=', period_max)
        ], limit=1)

        if not last_area_max_period:
            return f"No existe un período anterior al {area_record.period_id.name} con el cual realizar la comparativa para el área {area_record.area_id.display_name}.\n"
        else:
            existing_area_subject_ids = set(subject.subject_inherit_id.id for subject in area_record.subject_inherit_area_ids)
            previous_record_subject_ids = set(subject.subject_inherit_id.id for subject in last_area_max_period.subject_inherit_area_ids)

            removed_subject_ids = existing_area_subject_ids - previous_record_subject_ids
            added_subject_ids = previous_record_subject_ids - existing_area_subject_ids

            # Obtener los nombres de las asignaturas eliminadas
            removed_subject_names = []
            for subject_id in removed_subject_ids:
                subject = self.env['dara_mallas.subject_inherit'].search([('id', '=', subject_id)])
                if subject:
                    removed_subject_names.append(subject.display_name)

            # Obtener los nombres de las asignaturas añadidas
            added_subject_names = []
            for subject_id in added_subject_ids:
                subject = self.env['dara_mallas.subject_inherit'].search([('id', '=', subject_id)])
                if subject:
                    added_subject_names.append(subject.display_name)

            if len(added_subject_names) == 0 and len(removed_subject_names) == 0:
                differences_text = f"Área: {area_record.area_id.display_name}\nPeríodo nuevo: {area_record.period_id.display_name}\nPeríodo anterior: {last_area_max_period.period_id.display_name}\nNo se registran cambios.\n"
            else:
                differences_text = f"Área: {area_record.area_id.display_name}\nPeríodo nuevo: {area_record.period_id.display_name}\nPeríodo anterior: {last_area_max_period.period_id.display_name}\n"
                for removed_subject in removed_subject_names:
                    differences_text += f"Asignatura(s) añadida(s): {removed_subject}\n"
                for added_subject in added_subject_names:
                    differences_text += f"Asignatura(s) eliminada(s): {added_subject}\n"

            return differences_text

class area_homologation_history(models.Model):
    _name = 'dara_mallas.area_homologation_history'
    
    area_homologation_id = fields.Many2one('dara_mallas.area_homologation', string='Area Homologation')
    period_id = fields.Many2one('dara_mallas.period', string='Period')
    area_id = fields.Many2one('dara_mallas.area', string='Area')
    dinamic = fields.Boolean(string='Dinamic')
    subject_inherit_area_ids = fields.One2many('dara_mallas.subject_inherit_area_history',inverse_name='area_homologation_history_id',string='Asignaturas') 