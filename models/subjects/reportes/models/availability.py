from odoo import fields, models, api
from ..repository.availability_repository import availabilityRepository

class AvailabilityCourses(models.TransientModel):
    _name ="dara_mallas.availability_courses"
    _description="Disponibilidad de materias"
    
    subject = fields.Char(string="Código")
    result = fields.Char(string="Respuesta", readonly=True)
    
    type = fields.Selection(
        selection=[("asignatura","Asignatura"),("corte","Corte")],
        required=True,
        string="Disponibilidad de : ",
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
        
        repository = availabilityRepository(self.env)
        result = None    
            
        if self.type == 'asignatura':
            result = repository.get_availability_couses(subject)               
        else:
            result = repository.get_availability_curriculum(subject)            
        
        self.result = "Disponible" if result else "No Disponible"


    def action_search_availability(self):           
            self.findAsignature()         