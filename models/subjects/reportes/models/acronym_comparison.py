from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository


class AcronymComparison(models.TransientModel):
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
        repository = acronymRepository(self.env)
        result = repository.get_acronym_per_comparison(acronym1, acronym2)
        print("Resultado ", result)

        # Verificar si hay datos suficientes
        if not result or len(result) < 2:
            self.line_ids = []  # Si no hay datos, no se muestran filas
            self.env.user.notify_warning(
                message="No se encontraron resultados suficientes para las siglas proporcionadas.",
                title="Sin resultados",
            )
            return

        # Definir los nombres de las columnas según el orden de los datos
        column_names = [
            'subj', 'term', 'horas_docencia', 'horas_docencia_presencial_h',
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

        # Convertir las tuplas en diccionarios
        result_dicts = [dict(zip(column_names, row)) for row in result]

        # Crear las líneas de comparación para la vista
        lines = []
        fields_to_compare = set(result_dicts[0].keys()).union(result_dicts[1].keys())
        for field in fields_to_compare:
            line = {
                'subj': field,
                'term_acronym1': result_dicts[0].get(field, ''),  # Valor para Sigla 1
                'term_acronym2': result_dicts[1].get(field, ''),  # Valor para Sigla 2
            }
            lines.append((0, 0, line))  # Agregar una línea temporal (no persistente)

        # Asignar las líneas al campo One2many
        self.line_ids = lines
            
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
    term_acronym1 = fields.Char(string='Sigla 2')  # Para el valor de la primera sigla
    term_acronym2 = fields.Char(string='Sigla 1')  # Para el valor de la segunda sigla