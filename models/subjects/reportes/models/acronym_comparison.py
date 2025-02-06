from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository
from odoo.exceptions import UserError


class AcronymComparison(models.TransientModel):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 2")
    acronym2 = fields.Char("Sigla 1")
    
    line_ids = fields.One2many(
        'dara_mallas.acronym_comparison.line',  
        'comparison_id',
        string="Detalles Comparativos"
    )

    @api.onchange('acronym1')
    def _onchange_acronym1(self):
        if self.acronym1:
            self.acronym1 = self.acronym1.upper()

    @api.onchange('acronym2')
    def _onchange_acronym2(self):
        if self.acronym2:
            self.acronym2 = self.acronym2.upper()
    
    
    # Relación con los resultad    
    def findAcronym(self):
        acronym1 = self.acronym1
        acronym2 = self.acronym2

        # Llamar al repositorio para obtener los datos
        repository = acronymRepository(self.env)
        result = repository.get_acronym_per_comparison(acronym1, acronym2)

        # Verificar si hay datos suficientes
        if len(result) > 2:
            raise UserError("Se encontraron más de 2 resultados, lo cual no es permitido.")

        if acronym1 == acronym2:
            raise UserError("Inserte siglas diferentes")

 
        if not result:
            self.line_ids = []  # Si no hay datos, limpiar las líneas
            return  # No seguir ejecutando

        # Definir los nombres de las columnas según el orden de los datos

        column_names = [
            'titulo', 'credito', 'cobro', 'horas_contacto',
            'subj', 'term', 
            'horas_docencia', 'horas_docencia_presencial_h',
            'horas_docencia_virtual_h', 'horas_docencia_o', 'horas_laboratorio_docencia',
            'horas_laboratorio_docencia_h', 'horas_externado_docencia',
            'horas_externado_docencia_h', 'horas_aplicacion', 'horas_aplicacion_h',
            'horas_aplicacion_o', 'horas_aplicacion_laboratorio', 'horas_aplicacion_lab_h',
            'horas_aplicacion_lab_o', 'horas_pract_preprofesionales', 'horas_pract_preprof_h',
            'horas_pract_preprof_o', 'horas_servicio_comunidad', 'horas_servicio_comunidad_h',
            'horas_servicio_comunidad_o', 'total_horas_autonomas', 'total_horas_autonomas_h',
            'total_horas_autonomas_o', 'horas_titulacion', 'horas_titulacion_h',
            'horas_titulacion_o', 'sesiones_docencia', 'sesiones_laboratorio',
            'sesiones_externado', 'sesiones_o', 'semanas_externado', 'semanas_laboratorio',
            'horas_adicionales_silabo'
        ]



        result_dicts = [dict(zip(column_names, row)) for row in result]
        lines = []

        if len(result_dicts) == 1:  # Si solo hay un resultado
            single_result = result_dicts[0]
            term_value = single_result.get("subj", "")

            # Definir qué columna ocupará el resultado basado en 'term'
            if term_value == acronym1:                
                term_acronym1_data = single_result
                term_acronym2_data = {}  # Vacío
            else:                
                term_acronym1_data = {}
                term_acronym2_data = single_result

            fields_to_compare = [col for col in column_names if col in single_result]
            for field in column_names:
                line = {
                    'subj': field,
                    'term_acronym1': term_acronym1_data.get(field, ''),
                    'term_acronym2': term_acronym2_data.get(field, ''),
                }
                lines.append((0, 0, line))

        elif len(result_dicts) == 2:  # Si hay dos resultados
            fields_to_compare = set(result_dicts[0].keys()).union(result_dicts[1].keys())
            for field in column_names:
                line = {
                    'subj': field,
                    'term_acronym1': result_dicts[0].get(field, ''),
                    'term_acronym2': result_dicts[1].get(field, ''),
                }
                lines.append((0, 0, line))

        self.line_ids = lines
        self.env.context = dict(self.env.context, acronym1_name=acronym1, acronym2_name=acronym2)

            
class AcronymComparisonLine(models.TransientModel):
    _name = 'dara_mallas.acronym_comparison.line'
    _description = 'Línea de comparación de siglas'

    # Relación con el modelo principal
    comparison_id = fields.Many2one(
        'dara_mallas.acronym_comparison',
        string="Comparación"
    )

    # Campos de los resultados
    subj = fields.Char(string='Campo')
    term_acronym1 = fields.Char(string='Sigla 1') 
    term_acronym2 = fields.Char(string='Sigla 2') 