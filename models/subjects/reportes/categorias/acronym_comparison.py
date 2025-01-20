import json
from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository


class AcronymComparison(models.Model):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 1")
    acronym2 = fields.Char("Sigla 2")
    
    line_ids = fields.One2many(
        'dara_mallas.acronym_comparison.line',  # Modelo secundario
        'comparison_id',                       # Campo Many2one en el modelo secundario
        string="Detalles Comparativos"
    )
    
    
    # Relación con los resultad    
    def findAcronym(self):
        acronym1 = self.acronym1
        acronym2 = self.acronym2
        
        # Llamar al repositorio para obtener los datos
        repository = acronymRepository()
        result = repository.get_acronym_per_comparison(acronym1, acronym2)
        
        if result:
            self.respuesta= 'Con datos'
        else:
            self.result='Vacio'         
        
        # Limpiar las líneas anteriores
        self.line_ids.unlink()

        # Crear una línea para cada resultado                
        fields_to_compare = set(result[0].keys()).union(result[1].keys())  # Todos los campos únicos
        for field in fields_to_compare:
            # Crear una línea con el valor de cada campo para ambas siglas
            line_values = {
                'subj': field,
                'term_acronym1': result[0].get(field, ''),  # Valor para Sigla 1
                'term_acronym2': result[1].get(field, ''),  # Valor para Sigla 2
                'comparison_id': self.id  # Relacionar con la comparación actual
            }
            self.env['dara_mallas.acronym_comparison.line'].create(line_values)
            
class AcronymComparisonLine(models.Model):
    _name = 'dara_mallas.acronym_comparison.line'
    _description = 'Línea de comparación de siglas'

    # Relación con el modelo principal
    comparison_id = fields.Many2one(
        'dara_mallas.acronym_comparison',
        string="Comparación"
    )

    # Campos de los resultados
    subj = fields.Char(string='Campo')
    term_acronym1 = fields.Char(string='Sigla 2')  # Para el valor de la primera sigla
    term_acronym2 = fields.Char(string='Sigla 1')  # Para el valor de la segunda sigla