from odoo import fields, models,api
from odoo.exceptions import UserError
class area(models.Model):
    _name="dara_mallas.area"
    
    name=fields.Char("Nombre")
    code=fields.Char("Codigo")
 

class area_homologation(models.Model):
    _name="dara_mallas.area_homologation"
    
    period_id=fields.Many2one("dara_mallas.period")
    area_id=fields.Many2one("dara_mallas.area")
    #subject_rule_line_ids = fields.One2many("dara_mallas.subject_rule_line",inverse_name="area_homologation_id")
    subject_inherit_area_ids = fields.One2many("dara_mallas.subject_inherit_area",inverse_name="area_homologation_id",string="Asignaturas")

    @api.onchange('subject_inherit_area_ids') 
    def onchange_subject_inherit_area_ids(self):
        
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

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.area_id.name),str(rec.period_id.name))))
        return result
        
