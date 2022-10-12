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

class subject_attributes_subject(models.Model):
    _name="dara_mallas.subject_attributes_subject" 
    
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_attributes_id = fields.Many2one("dara_mallas.subject_attributes")
    period_id=fields.Many2one("dara_mallas.period")


 


