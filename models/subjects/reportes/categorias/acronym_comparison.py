import json
from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository


class AcronymComparison(models.Model):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 1")
    acronym2 = fields.Char("Sigla 2")
    
    # Relación con los resultados
   
    
    results_202210_ids = fields.One2many(
        "dara_mallas.acronym_comparison_result_202210",
        "acronym_comparison_id_202210",
        string="Resultados 202210",
        create=False, 
        edit=False, 
        delete=False,
        readonly=True
    )
    
    results_202310_ids = fields.One2many(
        "dara_mallas.acronym_comparison_result_202310",
        "acronym_comparison_id_202310",
        string="Resultados 202310",
        create=False, 
        edit=False, 
        delete=False,
        readonly=True
    )
    
   

    
    def findAcronym(self):
        acronym1 = self.acronym1
        acronym2 = self.acronym2
        
        # Llamar al repositorio para obtener los datos
        repository = acronymRepository()
        result = repository.get_acronym_per_comparison(acronym1, acronym2)
        
        # Asegurarse de que haya exactamente 2 valores únicos en TERM
        unique_terms = list({item['TERM'] for item in result})
        if len(unique_terms) != 2:
            raise ValueError("Se esperaban exactamente 2 valores únicos de TERM")

        # Inicializar diccionarios para las listas
        separated_data = {term: [] for term in unique_terms}

        # Clasificar los datos según TERM
        for item in result:
            separated_data[item['TERM']].append(item)
        
        print("Datos separados por TERM:")
        print("Grupo 1 -", unique_terms[0], ": ", separated_data[unique_terms[0]])
        print("Grupo 2 -", unique_terms[1], ": ", separated_data[unique_terms[1]])
        
        # Preparar los datos para la tabla
        group1_title = unique_terms[0]
        group2_title = unique_terms[1]

        headers = set()
        for item in separated_data[group1_title] + separated_data[group2_title]:
            headers.update(item.keys())
        headers = sorted(headers)

        table_data = []
        for header in headers:
            row = {
                "header": header,
                "group1": next((item.get(header, "") for item in separated_data[group1_title] if header in item), ""),
                "group2": next((item.get(header, "") for item in separated_data[group2_title] if header in item), ""),
            }
            table_data.append(row)

        # Guardar los datos en formato JSON en el campo 'table_data'
        self.table_data = json.dumps({
            "group1_title": group1_title,
            "group2_title": group2_title,
            "table_data": table_data,
        })

class AcronymComparisonResult(models.Model):
    _name = "dara_mallas.acronym_comparison_result_202210"
    _description = "Resultado de Comparativo de Siglas"

    # Relación con el modelo principal
    acronym_comparison_id_202210 = fields.Many2one(
        "dara_mallas.acronym_comparison", 
        string="Comparación de Siglas", 
        ondelete="cascade"
    )
    # Campo para almacenar el valor de SUBJ
    subj = fields.Char("SUBJ")
    term = fields.Char("TERM")
    horas_docencia = fields.Float("HORAS_DOCENCIA")
    horas_docencia_presencial_h = fields.Float("HORAS_DOCENCIA_PRESENCIAL_H")
    horas_docencia_virtual_h = fields.Float("HORAS_DOCENCIA_VIRTUAL_H")
    horas_docencia_o = fields.Float("HORAS_DOCENCIA_O")
    horas_laboratorio_docencia = fields.Float("HORAS_LABORATORIO_DOCENCIA")
    horas_laboratorio_docencia_h = fields.Float("HORAS_LABORATORIO_DOCENCIA_H")
    horas_externado_docencia = fields.Float("HORAS_EXTERNADO_DOCENCIA")
    horas_externado_docencia_h = fields.Float("HORAS_EXTERNADO_DOCENCIA_H")
    horas_aplicacion = fields.Float("HORAS_APLICACION")
    horas_aplicacion_h = fields.Float("HORAS_APLICACION_H")
    horas_aplicacion_o = fields.Float("HORAS_APLICACION_O")
    horas_aplicacion_laboratorio = fields.Float("HORAS_APLICACION_LABORATORIO")
    horas_aplicacion_lab_h = fields.Float("HORAS_APLICACION_LAB_H")
    horas_aplicacion_lab_o = fields.Float("HORAS_APLICACION_LAB_O")
    horas_pract_preprofesionales = fields.Float("HORAS_PRACT_PREPROFESIONALES")
    horas_pract_preprof_h = fields.Float("HORAS_PRACT_PREPROF_H")
    horas_pract_preprof_o = fields.Float("HORAS_PRACT_PREPROF_O")
    horas_servicio_comunidad = fields.Float("HORAS_SERVICIO_COMUNIDAD")
    horas_servicio_comunidad_h = fields.Float("HORAS_SERVICIO_COMUNIDAD_H")
    horas_servicio_comunidad_o = fields.Float("HORAS_SERVICIO_COMUNIDAD_O")
    total_horas_autonomas = fields.Float("TOTAL_HORAS_AUTONOMAS")
    total_horas_autonomas_h = fields.Float("TOTAL_HORAS_AUTONOMAS_H")
    total_horas_autonomas_o = fields.Float("TOTAL_HORAS_AUTONOMAS_O")
    horas_titulacion = fields.Float("HORAS_TITULACION")
    horas_titulacion_h = fields.Float("HORAS_TITULACION_H")
    horas_titulacion_o = fields.Float("HORAS_TITULACION_O")
    sesiones_docencia = fields.Float("SESIONES_DOCENCIA")
    sesiones_laboratorio = fields.Float("SESIONES_LABORATORIO")
    sesiones_externado = fields.Float("SESIONES_EXTERNADO")
    sesiones_o = fields.Float("SESIONES_O")
    semanas_externado = fields.Float("SEMANAS_EXTERNADO")
    semanas_laboratorio = fields.Float("SEMANAS_LABORATORIO")
    horas_adicionales_silabo = fields.Float("HORAS_ADICIONALES_SILABO")
    
    
class AcronymComparisonResult(models.Model):
    _name = "dara_mallas.acronym_comparison_result_202310"
    _description = "Resultado de Comparativo de Siglas"

    # Relación con el modelo principal
    acronym_comparison_id_202310 = fields.Many2one(
        "dara_mallas.acronym_comparison", 
        string="Comparación de Siglas", 
        ondelete="cascade"
    )
    # Campo para almacenar el valor de SUBJ
    subj = fields.Char("SUBJ")
    term = fields.Char("TERM")
    horas_docencia = fields.Float("HORAS_DOCENCIA")
    horas_docencia_presencial_h = fields.Float("HORAS_DOCENCIA_PRESENCIAL_H")
    horas_docencia_virtual_h = fields.Float("HORAS_DOCENCIA_VIRTUAL_H")
    horas_docencia_o = fields.Float("HORAS_DOCENCIA_O")
    horas_laboratorio_docencia = fields.Float("HORAS_LABORATORIO_DOCENCIA")
    horas_laboratorio_docencia_h = fields.Float("HORAS_LABORATORIO_DOCENCIA_H")
    horas_externado_docencia = fields.Float("HORAS_EXTERNADO_DOCENCIA")
    horas_externado_docencia_h = fields.Float("HORAS_EXTERNADO_DOCENCIA_H")
    horas_aplicacion = fields.Float("HORAS_APLICACION")
    horas_aplicacion_h = fields.Float("HORAS_APLICACION_H")
    horas_aplicacion_o = fields.Float("HORAS_APLICACION_O")
    horas_aplicacion_laboratorio = fields.Float("HORAS_APLICACION_LABORATORIO")
    horas_aplicacion_lab_h = fields.Float("HORAS_APLICACION_LAB_H")
    horas_aplicacion_lab_o = fields.Float("HORAS_APLICACION_LAB_O")
    horas_pract_preprofesionales = fields.Float("HORAS_PRACT_PREPROFESIONALES")
    horas_pract_preprof_h = fields.Float("HORAS_PRACT_PREPROF_H")
    horas_pract_preprof_o = fields.Float("HORAS_PRACT_PREPROF_O")
    horas_servicio_comunidad = fields.Float("HORAS_SERVICIO_COMUNIDAD")
    horas_servicio_comunidad_h = fields.Float("HORAS_SERVICIO_COMUNIDAD_H")
    horas_servicio_comunidad_o = fields.Float("HORAS_SERVICIO_COMUNIDAD_O")
    total_horas_autonomas = fields.Float("TOTAL_HORAS_AUTONOMAS")
    total_horas_autonomas_h = fields.Float("TOTAL_HORAS_AUTONOMAS_H")
    total_horas_autonomas_o = fields.Float("TOTAL_HORAS_AUTONOMAS_O")
    horas_titulacion = fields.Float("HORAS_TITULACION")
    horas_titulacion_h = fields.Float("HORAS_TITULACION_H")
    horas_titulacion_o = fields.Float("HORAS_TITULACION_O")
    sesiones_docencia = fields.Float("SESIONES_DOCENCIA")
    sesiones_laboratorio = fields.Float("SESIONES_LABORATORIO")
    sesiones_externado = fields.Float("SESIONES_EXTERNADO")
    sesiones_o = fields.Float("SESIONES_O")
    semanas_externado = fields.Float("SEMANAS_EXTERNADO")
    semanas_laboratorio = fields.Float("SEMANAS_LABORATORIO")
    horas_adicionales_silabo = fields.Float("HORAS_ADICIONALES_SILABO") 
    
    
    