from odoo import fields, models, api
from ..repository.availability_repository import availabilityRepository

class AvailabilityCourses(models.Model):
    _name ="dara_mallas.availability_courses"
    _description="Disponibilidad de materias"
    
    subject = fields.Char("materia")
    result = fields.Char(string="Disponibilidad", readonly=True)
    
    type = fields.Selection(
        selection=[("asignatura","Asignatura"),("corte","Corte")],
        required=True,
        string="Disponibilidad de tipo: ",
        help="Seleccione el tipo de disponibilidad a buscar.")
    
    
    @api.onchange('type')
    def _onchange_type(self):
        if not self.type:
            self.subject = False 

    
    @api.onchange('subject')
    def _onchange_subject(self):
        if self.subject:
            self.subject = self.subject.upper()
            
    
    def findAsignature(self):
        subject = self.subject        
        
        repository = availabilityRepository()
        result = None
        #courses = repository.get_availability_couses(subject)
        #curriculum = repository.get_availability_curriculum(subject)
    
            
        if self.type == 'asignatura':
            result = repository.get_availability_couses(subject)
            print("asignatura")     
        else:
            result = repository.get_availability_curriculum(subject)
            print("Corte")
        
        self.result = "Disponible" if result else "No Disponible"


    def action_search_availability(self):           
            self.findAsignature()         