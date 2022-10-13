from odoo import fields, models

class area(models.Model):
    _name="dara_mallas.area"
    
    name=fields.Char("Nombre")
    code=fields.Char("Codigo")
 

class area_homologation(models.Model):
    _name="dara_mallas.area_homologation"
    
    period_id=fields.Many2one("dara_mallas.period")
    area_id=fields.Many2one("dara_mallas.area")
    subject_rule_line_ids = fields.One2many("dara_mallas.subject_rule_line",inverse_name="area_homologation_id")