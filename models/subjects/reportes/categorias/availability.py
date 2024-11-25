from odoo import fields, models

class AvailabilityCourses(models.Model):
    _name ="dara_mallas.availability_courses"
    _description="Disponibilidad de materias"
    
    subject = fields.Char("materia")
    result = fields.Char("disponibilidad")
    type = fields.Selection(selection=[("asignatura","Asignatura"),("corte","Corte")])
    

