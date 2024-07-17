from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class subject(models.Model):
   
    _name="dara_mallas.subject"

    name=fields.Char("Asignatura, curso o equivalente")
    name_en=fields.Char("Subject, course or equivalent ") 

    short_name=fields.Char("Nombre Corto", size=30)
    code=fields.Char("Sigla", default='ccc-nnnn')
    course_number=fields.Char("Course", size=4, default="nnnn")
    subject_name_id=fields.Many2one("dara_mallas.subject_name")
      
    subject_class_ids = fields.One2many("dara_mallas.subject_class",inverse_name="subject_id")

    new_subject = fields.Boolean("Nueva", default=True,track_visibility='always')

    ## se controla que la longitud maxima del nombre de la asignatura sea 27 mantenimiento los 30 caracteres.
    @api.onchange('short_name')
    def check_name_field_length(self):
        if self.short_name:
            if len(self.short_name) > 27:
                raise ValidationError("El campo debe tener máximo 27 caracteres.")

    @api.onchange('subject_name_id','course_number')
    def onchange_subject_code(self):
        subject_name="xxxx"
        course_number="nnnn"
        if self.subject_name_id:
            subject_name=self.subject_name_id.code
        if self.course_number:
            if len(self.course_number)<4:
                raise UserError("Course number debe tener 4 digitos")
            course_number=self.course_number
        
        
        
        self.code=subject_name+course_number 

class subject_rule(models.Model):
    _name="dara_mallas.subject_rule"

    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char(related="subject_id.code")
    area_id=fields.Many2one("dara_mallas.area") 
    subject_homologation_ids = fields.One2many("dara_mallas.homologation",inverse_name="subject_rule_id",string="Homologaciones")

    #relacion con el espejo
    subject_rule_mirror_ids = fields.One2many("dara_mallas.subject_rule_mirror",inverse_name="subject_rule_id",string="Versiones")


    def write(self,vals):
        '''
        Almacena los valores originales previo a realizar modificaciones en las tablas espejo de 
        la cabecera de reglas (subject_rule) y su detalle (homologations)
        '''
        print("Area actual de la regla:",self.area_id)
        print("ID de la regla actual:", self.id)
        stop_study_plan = self.env['dara_mallas.area_homologation'].stop_study_plan_flag(self.area_id, self)
        if stop_study_plan:    
            for record in self:
                existing_rule_mirror = self.env['dara_mallas.subject_rule_mirror'].search([
                ('subject_rule_id', '=', record.id)
                ])
                if not existing_rule_mirror:
                    new_subject_rule_mirror = self.env['dara_mallas.subject_rule_mirror'].create(
                    {
                    'period_id': record.period_id.id,
                    'subject_id': record.subject_id.id,
                    'subject_code': record.subject_code,
                    'area_id': record.area_id.id,
                    'subject_rule_id': record.id,
                    }
                    )
                    new_homologation_ids = []

                    for homo in record.subject_homologation_ids:
                        new_homologation = self.env['dara_mallas.homologation_mirror'].create(
                        {
                            'homologation_subject_id': homo.homologation_subject_id.id,
                            'homologation_subject_code': homo.homologation_subject_code,
                            'subject_rule_subject_id': homo.subject_rule_subject_id.id,
                            'subject_attributes_id': homo.subject_attributes_id.id,
                            'group_id': homo.group_id.id,
                            'condition': homo.condition,
                            'test': homo.test,
                            'min_score': homo.min_score,
                            'max_score': homo.max_score,
                            'rule_min_score_id': homo.rule_min_score_id.id,
                            'subject_rule_id': new_subject_rule_mirror.id
                        }
                    )
                        new_homologation_ids.append(new_homologation.id)
                
                    new_subject_rule_mirror.write(
                        {
                            'subject_homologation_ids':[(6,0, new_homologation_ids)]
                        }
                    )

                    print("---------------------------")
                    print("Regla creada: ",new_subject_rule_mirror.subject_id.display_name)

                    for regla in new_subject_rule_mirror.subject_homologation_ids:
                        if regla.homologation_subject_id.display_name:
                            print("Homologacion: ",regla.homologation_subject_id.display_name)
                        else: 
                            print("Homologacion: ",regla.test)
                else:
                    print("Copia ya existe")
        else:
            print("NO SE CREARA LA COPIA EN ESPEJO")
        
        return super(subject_rule, self).write(vals)


    def copy(self,default=None):
        new_object=super(subject_rule,self).copy(default=default)
        objects = []
        for item in self.subject_homologation_ids:
            pre = {
                'homologation_subject_id':item.homologation_subject_id.id,
                'subject_rule_subject_id':item.subject_rule_subject_id.id,
                'subject_attributes_id':item.subject_attributes_id.id,
                'group_id':item.group_id.id,
                'condition':item.condition,
                'test':item.test,
                'min_score':item.min_score,
                'max_score':item.max_score,
                'rule_min_score_id':item.rule_min_score_id.id,
                'subject_rule_id':new_object.id,
            }
            object_create = self.env['dara_mallas.homologation'].create(pre)
            objects.append(object_create.id)
        new_object.subject_homologation_ids=[(6,0,objects)]
        return new_object
    
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_id.code),str(rec.subject_id.name))))
        return result

class subject_rule_mirror(models.Model):
    _name="dara_mallas.subject_rule_mirror"

    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char(related="subject_id.code")
    area_id=fields.Many2one("dara_mallas.area") 
    subject_homologation_ids = fields.One2many("dara_mallas.homologation_mirror",inverse_name="subject_rule_id",string="Homologaciones")

    #relacion con la tabla original
    subject_rule_id = fields.Many2one("dara_mallas.subject_rule")
    
class homologation_mirror(models.Model):
    _name="dara_mallas.homologation_mirror"
   
    homologation_subject_id=fields.Many2one("dara_mallas.subject",track_visibility='always')
    homologation_subject_code=fields.Char("Sigla",related="homologation_subject_id.code",track_visibility='always')
    #subject_rule_rule_id = fields.Many2one("dara_mallas.subject_rule",track_visibility='always')
    subject_rule_subject_id = fields.Many2one("dara_mallas.subject_inherit",track_visibility='always')
    subject_attributes_id = fields.Many2one("dara_mallas.subject_attributes")
    group_id=fields.Many2one("dara_mallas.group_rule",track_visibility='always') 
    condition=fields.Char("Condiciones",track_visibility='always')
    test=fields.Char("Prueba",track_visibility='always')
    min_score=fields.Integer("Puntaje Minimo",track_visibility='always')
    max_score=fields.Integer("Puntaje maximo",track_visibility='always')
    rule_min_score_id=fields.Many2one('dara_mallas.rule_score', string="Calificacion minima")
    subject_rule_id = fields.Many2one("dara_mallas.subject_rule_mirror",track_visibility='always')


class subject_rule_line(models.Model):
    _name="dara_mallas.subject_rule_line"

    line_order=fields.Integer("No.")
    subject_rule_id=fields.Many2one("dara_mallas.subject_rule")
    subject_rule_period=fields.Char("Periodo",related="subject_rule_id.period_id.name")
    name=fields.Char("Sigla",related="subject_rule_id.subject_id.code")

    area_homologation_id=fields.Many2one("dara_mallas.area_homologation")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_rule_id.subject_id.code),str(rec.subject_rule_id.subject_id.name))))
        return result

class homologation(models.Model):
    _name="dara_mallas.homologation"
    #_order="group_id,homologation_subject_id"
    #_order="CASE WHEN subject_rule_subject_id is null THEN group_id desc ELSE 0"

    homologation_subject_id=fields.Many2one("dara_mallas.subject",track_visibility='always')
    homologation_subject_code=fields.Char("Sigla",related="homologation_subject_id.code",track_visibility='always')
    #subject_rule_rule_id = fields.Many2one("dara_mallas.subject_rule",track_visibility='always')
    subject_rule_subject_id = fields.Many2one("dara_mallas.subject_inherit",track_visibility='always')
    subject_attributes_id = fields.Many2one("dara_mallas.subject_attributes")
    group_id=fields.Many2one("dara_mallas.group_rule",track_visibility='always') 
    condition=fields.Char("Condiciones",track_visibility='always')
    test=fields.Char("Prueba",track_visibility='always')
    min_score=fields.Integer("Puntaje Minimo",track_visibility='always')
    max_score=fields.Integer("Puntaje maximo",track_visibility='always')
    rule_min_score_id=fields.Many2one('dara_mallas.rule_score', string="Calificacion minima")

    subject_rule_id = fields.Many2one("dara_mallas.subject_rule",track_visibility='always')

    def _generate_order_by(self, order_spec, query):
        order_by = super(homologation, self)._generate_order_by(order_spec, query)
        my_order = "CASE WHEN subject_rule_subject_id is null  THEN 1 ELSE homologation_subject_id END ,group_id"            
        #if order_spec:
            #return super(sale_order, self)._generate_order_by(order_spec, query) + ", " + my_order
        return " order by " + my_order

    

    def name_get(self):
        result = []
        for rec in self:
            if rec.homologation_subject_id:
                result.append((rec.id,'%s - %s' % (str(rec.homologation_subject_id.code),str(rec.homologation_subject_id.name))))
            elif rec.test:
                result.append((rec.id,'%s' % (str(rec.test))))

        return result

class group_rule(models.Model):
    _name="dara_mallas.group_rule"
    
    name=fields.Char("Agrupador")

class rule_score(models.Model):
    _name="dara_mallas.rule_score"
    
    name=fields.Char("Calificacion")  

class elective_line(models.Model):
    _name="dara_mallas.elective_line"
     
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char("Code",related="subject_id.code")

    elective_ids=fields.One2many("dara_mallas.elective",inverse_name="elective_line_id")
    
    def copy(self,default=None):
        new_object=super(elective_line,self).copy(default=default)
        objects = []
        for item in self.elective_ids:
            pre = {
                'elective_subject_inherit_id':item.elective_subject_inherit_id.id,
                'elective_line_id':new_object.id,
            }
            object_create = self.env['dara_mallas.elective'].create(pre)
            objects.append(object_create.id)
        new_object.elective_ids=[(6,0,objects)]
        return new_object
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_code),str(rec.subject_id.name))))
        return result

class elective(models.Model):
    _name="dara_mallas.elective"
   
    elective_subject_inherit_id=fields.Many2one("dara_mallas.subject_inherit")
    elective_subject_code=fields.Char("Sigla",related="elective_subject_inherit_id.code")

    elective_line_id=fields.Many2one("dara_mallas.elective_line")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.elective_subject_code))))
        return result

class itinerary_line(models.Model):
    _name="dara_mallas.itinerary_line"
     
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char("Code",related="subject_id.code")
    itinerary_ids=fields.One2many("dara_mallas.itinerary",inverse_name="itinerary_line_id")

    def copy(self,default=None):
        new_object=super(itinerary_line,self).copy(default=default)
        objects = []
        for item in self.itinerary_ids:
            pre = {
                'itinerary_subject_id':item.itinerary_subject_id.id,
                'itinerary_subject_inherit_id':item.itinerary_subject_inherit_id.id,
                'specialization_id':item.specialization_id.id,
                'itinerary_line_id':new_object.id,
            }
            object_create = self.env['dara_mallas.itinerary'].create(pre)
            objects.append(object_create.id)
        new_object.elective_ids=[(6,0,objects)]
        return new_object
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_code),str(rec.subject_id.name))))
        return result

class itinerary(models.Model):
    _name="dara_mallas.itinerary"

   
    itinerary_subject_inherit_id=fields.Many2one("dara_mallas.subject_inherit")
    itinerary_subject_code=fields.Char("Sigla",related="itinerary_subject_inherit_id.code")
    specialization_id=fields.Many2one("dara_mallas.specialization")

    itinerary_line_id=fields.Many2one("dara_mallas.itinerary_line")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.itinerary_subject_code))))
        return result