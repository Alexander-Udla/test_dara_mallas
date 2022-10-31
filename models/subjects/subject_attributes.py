from odoo import fields, models,api 

class subject_attributes(models.Model):
    _name="dara_mallas.subject_attributes" 
    
    name = fields.Char("Código")
    description = fields.Char("Descripción")

    def name_get(self):
        res = []
        for element in self:
            name = ''
            name += element.name or ' '
            name += '-'
            name += element.description or ' '
           
            res.append((element.id, name))
        return res

class subject_attributes_line(models.Model):
    _name="dara_mallas.subject_attributes_line" 
    
    subject_attributes_id = fields.Many2one("dara_mallas.subject_attributes")
    subject_attributes_des = fields.Char("Descripción",related="subject_attributes_id.description")

    subject_attributes_subject_id = fields.Many2one("dara_mallas.subject_attributes_subject")
class subject_attributes_subject(models.Model):
    _name="dara_mallas.subject_attributes_subject" 
    
    subject_id=fields.Many2one("dara_mallas.subject")
    period_id=fields.Many2one("dara_mallas.period")
    subject_attributes_line_ids = fields.One2many("dara_mallas.subject_attributes_line",inverse_name="subject_attributes_subject_id")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result

 


