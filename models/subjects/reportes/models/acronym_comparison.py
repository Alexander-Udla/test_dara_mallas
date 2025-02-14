from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository
from odoo.exceptions import UserError


class AcronymComparison(models.TransientModel):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 1")
    acronym2 = fields.Char("Sigla 2")
    
    line_ids = fields.One2many(
        'dara_mallas.acronym_comparison.line',  
        'comparison_id',
        string="Detalles Comparativos"
    )

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    @api.onchange('acronym1')
    def _onchange_acronym1(self):
        if self.acronym1:
            self.acronym1 = self.acronym1.upper()

    @api.onchange('acronym2')
    def _onchange_acronym2(self):
        if self.acronym2:
            self.acronym2 = self.acronym2.upper()


    def findAcronym(self):
        acronym1 = self.acronym1
        acronym2 = self.acronym2

        if not acronym1 or not acronym2:
            raise UserError("Debe ingresar ambas siglas para la comparación.")

        if acronym1 == acronym2:
            raise UserError("Las siglas deben ser diferentes.")

        # Llamar al repositorio para obtener los datos
        repository = acronymRepository(self.env)
        result = repository.get_acronym_per_comparison(acronym1, acronym2)

        if len(result) > 2:
            raise UserError("Solo se permiten hasta 2 registros para la comparación.")

        if not result:
            self.write({'line_ids': []})  # Limpiar líneas si no hay datos
            return

        # Definir los nombres de las columnas según el orden de los datos
        column_names = [
            'titulo', 'credito', 'cobro', 'horas_contacto', 'subj', 'term',
            'horas_docencia', 'horas_docencia_presencial_h', 'horas_docencia_virtual_h',
            'horas_docencia_o', 'horas_laboratorio_docencia', 'horas_laboratorio_docencia_h',
            'horas_externado_docencia', 'horas_externado_docencia_h', 'horas_aplicacion',
            'horas_aplicacion_h', 'horas_aplicacion_o', 'horas_aplicacion_laboratorio',
            'horas_aplicacion_lab_h', 'horas_aplicacion_lab_o', 'horas_pract_preprofesionales',
            'horas_pract_preprof_h', 'horas_pract_preprof_o', 'horas_servicio_comunidad',
            'horas_servicio_comunidad_h', 'horas_servicio_comunidad_o', 'total_horas_autonomas',
            'total_horas_autonomas_h', 'total_horas_autonomas_o', 'horas_titulacion',
            'horas_titulacion_h', 'horas_titulacion_o', 'sesiones_docencia', 'sesiones_laboratorio',
            'sesiones_externado', 'sesiones_o', 'semanas_externado', 'semanas_laboratorio',
            'horas_adicionales_silabo'
        ]

        # Convertir resultado a diccionario con nombres de columna
        result_dicts = [dict(zip(column_names, row)) for row in result]

        # Asegurar que los datos se asignen correctamente respetando el orden de las siglas ingresadas
        lines = []
        if len(result_dicts) == 1:
            single_result = result_dicts[0]
            subj_value = single_result.get("subj", "")

            # Comparar con el orden de las siglas ingresadas
            if subj_value == acronym1:
                term_acronym1_data = single_result
                term_acronym2_data = {}
            elif subj_value == acronym2:
                term_acronym1_data = {}
                term_acronym2_data = single_result
            else:
                term_acronym1_data = {}
                term_acronym2_data = {}

            for field in column_names:
                lines.append((0, 0, {
                    'subj': field,
                    'term_acronym1': term_acronym1_data.get(field, ''),
                    'term_acronym2': term_acronym2_data.get(field, ''),
                }))

        elif len(result_dicts) == 2:
            # Determinar cuál resultado corresponde a cada sigla
            first_result = result_dicts[0]
            second_result = result_dicts[1]

            # Obtener los valores de `subj`
            first_subj = first_result.get("subj", "")
            second_subj = second_result.get("subj", "")

            # Asignar los valores al campo correcto respetando el orden de entrada de siglas
            if first_subj == acronym1 and second_subj == acronym2:
                term1_data = first_result
                term2_data = second_result
            elif first_subj == acronym2 and second_subj == acronym1:
                term1_data = second_result
                term2_data = first_result
            else:
                term1_data = {}
                term2_data = {}

            for field in column_names:
                lines.append((0, 0, {
                    'subj': field,
                    'term_acronym1': term1_data.get(field, ''),
                    'term_acronym2': term2_data.get(field, ''),
                }))

        self.write({'line_ids': lines})
        self = self.with_context(acronym1_name=acronym1, acronym2_name=acronym2)

            
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