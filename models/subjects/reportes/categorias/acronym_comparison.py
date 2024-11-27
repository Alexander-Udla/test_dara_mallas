from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository


class AcronymComparison(models.Model):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 1")
    acronym2 = fields.Char("Sigla 2")
    result = fields.Text("Resultado")
    
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
        
        result_term_202210 = []
        result_term_202310 = []

         
        if not acronym1 or not acronym2:
            raise ValueError("Ambas siglas son necesarias para la comparación.")
        
        repository = acronymRepository()
        result = repository.get_acronym_per_comparison(acronym1, acronym2)
        self.result = str(result)
       
        if self.results_202210_ids:
            self.results_202210_ids.unlink()
        if self.results_202310_ids:
            self.results_202310_ids.unlink()

        
        for item in result:
            if item['TERM'] == '202210':
                result_term_202210.append(item)
            elif item['TERM'] == '202310':
                result_term_202310.append(item)
     
        for record in result_term_202210:
            cleaned_record = {}            
            
            for key, value in record.items():
                if key not in ['SUBJ', 'TERM']:  
                    key = key.strip("'")  
                cleaned_record[key] = value

            data_to_store = {
                'acronym_comparison_id_202210': self.id,
            }
            
            if 'SUBJ' in cleaned_record:
                data_to_store['subj'] = cleaned_record['SUBJ']
            
            if 'TERM' in cleaned_record:
                data_to_store['term'] = cleaned_record['TERM']
           
            if 'HORAS_DOCENCIA' in cleaned_record:
                data_to_store['horas_docencia'] = cleaned_record['HORAS_DOCENCIA']

            if 'HORAS_DOCENCIA_PRESENCIAL_H' in cleaned_record:
                data_to_store['horas_docencia_presencial_h'] = cleaned_record['HORAS_DOCENCIA_PRESENCIAL_H']

            if 'HORAS_DOCENCIA_VIRTUAL_H' in cleaned_record:
                data_to_store['horas_docencia_virtual_h'] = cleaned_record['HORAS_DOCENCIA_VIRTUAL_H']

            if 'HORAS_DOCENCIA_O' in cleaned_record:
                data_to_store['horas_docencia_o'] = cleaned_record['HORAS_DOCENCIA_O']

            if 'HORAS_LABORATORIO_DOCENCIA' in cleaned_record:
                data_to_store['horas_laboratorio_docencia'] = cleaned_record['HORAS_LABORATORIO_DOCENCIA']

            if 'HORAS_LABORATORIO_DOCENCIA_H' in cleaned_record:
                data_to_store['horas_laboratorio_docencia_h'] = cleaned_record['HORAS_LABORATORIO_DOCENCIA_H']

            if 'HORAS_EXTERNADO_DOCENCIA' in cleaned_record:
                data_to_store['horas_externado_docencia'] = cleaned_record['HORAS_EXTERNADO_DOCENCIA']

            if 'HORAS_EXTERNADO_DOCENCIA_H' in cleaned_record:
                data_to_store['horas_externado_docencia_h'] = cleaned_record['HORAS_EXTERNADO_DOCENCIA_H']

            if 'HORAS_APLICACION' in cleaned_record:
                data_to_store['horas_aplicacion'] = cleaned_record['HORAS_APLICACION']

            if 'HORAS_APLICACION_H' in cleaned_record:
                data_to_store['horas_aplicacion_h'] = cleaned_record['HORAS_APLICACION_H']

            if 'HORAS_APLICACION_O' in cleaned_record:
                data_to_store['horas_aplicacion_o'] = cleaned_record['HORAS_APLICACION_O']

            if 'HORAS_APLICACION_LABORATORIO' in cleaned_record:
                data_to_store['horas_aplicacion_laboratorio'] = cleaned_record['HORAS_APLICACION_LABORATORIO']

            if 'HORAS_APLICACION_LAB_H' in cleaned_record:
                data_to_store['horas_aplicacion_lab_h'] = cleaned_record['HORAS_APLICACION_LAB_H']

            if 'HORAS_APLICACION_LAB_O' in cleaned_record:
                data_to_store['horas_aplicacion_lab_o'] = cleaned_record['HORAS_APLICACION_LAB_O']

            if 'HORAS_PRACT_PREPROFESIONALES' in cleaned_record:
                data_to_store['horas_pract_preprofesionales'] = cleaned_record['HORAS_PRACT_PREPROFESIONALES']

            if 'HORAS_PRACT_PREPROF_H' in cleaned_record:
                data_to_store['horas_pract_preprof_h'] = cleaned_record['HORAS_PRACT_PREPROF_H']

            if 'HORAS_PRACT_PREPROF_O' in cleaned_record:
                data_to_store['horas_pract_preprof_o'] = cleaned_record['HORAS_PRACT_PREPROF_O']

            if 'HORAS_SERVICIO_COMUNIDAD' in cleaned_record:
                data_to_store['horas_servicio_comunidad'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD']

            if 'HORAS_SERVICIO_COMUNIDAD_H' in cleaned_record:
                data_to_store['horas_servicio_comunidad_h'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD_H']

            if 'HORAS_SERVICIO_COMUNIDAD_O' in cleaned_record:
                data_to_store['horas_servicio_comunidad_o'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD_O']

            if 'TOTAL_HORAS_AUTONOMAS' in cleaned_record:
                data_to_store['total_horas_autonomas'] = cleaned_record['TOTAL_HORAS_AUTONOMAS']

            if 'TOTAL_HORAS_AUTONOMAS_H' in cleaned_record:
                data_to_store['total_horas_autonomas_h'] = cleaned_record['TOTAL_HORAS_AUTONOMAS_H']

            if 'TOTAL_HORAS_AUTONOMAS_O' in cleaned_record:
                data_to_store['total_horas_autonomas_o'] = cleaned_record['TOTAL_HORAS_AUTONOMAS_O']

            if 'HORAS_TITULACION' in cleaned_record:
                data_to_store['horas_titulacion'] = cleaned_record['HORAS_TITULACION']

            if 'HORAS_TITULACION_H' in cleaned_record:
                data_to_store['horas_titulacion_h'] = cleaned_record['HORAS_TITULACION_H']

            if 'HORAS_TITULACION_O' in cleaned_record:
                data_to_store['horas_titulacion_o'] = cleaned_record['HORAS_TITULACION_O']

            if 'SESIONES_DOCENCIA' in cleaned_record:
                data_to_store['sesiones_docencia'] = cleaned_record['SESIONES_DOCENCIA']

            if 'SESIONES_LABORATORIO' in cleaned_record:
                data_to_store['sesiones_laboratorio'] = cleaned_record['SESIONES_LABORATORIO']

            if 'SESIONES_EXTERNADO' in cleaned_record:
                data_to_store['sesiones_externado'] = cleaned_record['SESIONES_EXTERNADO']

            if 'SEMANAS_EXTERNADO' in cleaned_record:
                data_to_store['semanas_externado'] = cleaned_record['SEMANAS_EXTERNADO']

            if 'SEMANAS_LABORATORIO' in cleaned_record:
                data_to_store['semanas_laboratorio'] = cleaned_record['SEMANAS_LABORATORIO']

            if 'HORAS_ADICIONALES_SILABO' in cleaned_record:
                data_to_store['horas_adicionales_silabo'] = cleaned_record['HORAS_ADICIONALES_SILABO']

            self.env['dara_mallas.acronym_comparison_result_202210'].create(data_to_store)

        for record in result_term_202310:
            cleaned_record = {}            
            
            for key, value in record.items():
                if key not in ['SUBJ', 'TERM']:  
                    key = key.strip("'")  
                cleaned_record[key] = value

            data_to_store = {
                'acronym_comparison_id_202310': self.id,
            }
            
            if 'SUBJ' in cleaned_record:
                data_to_store['subj'] = cleaned_record['SUBJ']
            
            if 'TERM' in cleaned_record:
                data_to_store['term'] = cleaned_record['TERM']
           
            if 'HORAS_DOCENCIA' in cleaned_record:
                data_to_store['horas_docencia'] = cleaned_record['HORAS_DOCENCIA']

            if 'HORAS_DOCENCIA_PRESENCIAL_H' in cleaned_record:
                data_to_store['horas_docencia_presencial_h'] = cleaned_record['HORAS_DOCENCIA_PRESENCIAL_H']

            if 'HORAS_DOCENCIA_VIRTUAL_H' in cleaned_record:
                data_to_store['horas_docencia_virtual_h'] = cleaned_record['HORAS_DOCENCIA_VIRTUAL_H']

            if 'HORAS_DOCENCIA_O' in cleaned_record:
                data_to_store['horas_docencia_o'] = cleaned_record['HORAS_DOCENCIA_O']

            if 'HORAS_LABORATORIO_DOCENCIA' in cleaned_record:
                data_to_store['horas_laboratorio_docencia'] = cleaned_record['HORAS_LABORATORIO_DOCENCIA']

            if 'HORAS_LABORATORIO_DOCENCIA_H' in cleaned_record:
                data_to_store['horas_laboratorio_docencia_h'] = cleaned_record['HORAS_LABORATORIO_DOCENCIA_H']

            if 'HORAS_EXTERNADO_DOCENCIA' in cleaned_record:
                data_to_store['horas_externado_docencia'] = cleaned_record['HORAS_EXTERNADO_DOCENCIA']

            if 'HORAS_EXTERNADO_DOCENCIA_H' in cleaned_record:
                data_to_store['horas_externado_docencia_h'] = cleaned_record['HORAS_EXTERNADO_DOCENCIA_H']

            if 'HORAS_APLICACION' in cleaned_record:
                data_to_store['horas_aplicacion'] = cleaned_record['HORAS_APLICACION']

            if 'HORAS_APLICACION_H' in cleaned_record:
                data_to_store['horas_aplicacion_h'] = cleaned_record['HORAS_APLICACION_H']

            if 'HORAS_APLICACION_O' in cleaned_record:
                data_to_store['horas_aplicacion_o'] = cleaned_record['HORAS_APLICACION_O']

            if 'HORAS_APLICACION_LABORATORIO' in cleaned_record:
                data_to_store['horas_aplicacion_laboratorio'] = cleaned_record['HORAS_APLICACION_LABORATORIO']

            if 'HORAS_APLICACION_LAB_H' in cleaned_record:
                data_to_store['horas_aplicacion_lab_h'] = cleaned_record['HORAS_APLICACION_LAB_H']

            if 'HORAS_APLICACION_LAB_O' in cleaned_record:
                data_to_store['horas_aplicacion_lab_o'] = cleaned_record['HORAS_APLICACION_LAB_O']

            if 'HORAS_PRACT_PREPROFESIONALES' in cleaned_record:
                data_to_store['horas_pract_preprofesionales'] = cleaned_record['HORAS_PRACT_PREPROFESIONALES']

            if 'HORAS_PRACT_PREPROF_H' in cleaned_record:
                data_to_store['horas_pract_preprof_h'] = cleaned_record['HORAS_PRACT_PREPROF_H']

            if 'HORAS_PRACT_PREPROF_O' in cleaned_record:
                data_to_store['horas_pract_preprof_o'] = cleaned_record['HORAS_PRACT_PREPROF_O']

            if 'HORAS_SERVICIO_COMUNIDAD' in cleaned_record:
                data_to_store['horas_servicio_comunidad'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD']

            if 'HORAS_SERVICIO_COMUNIDAD_H' in cleaned_record:
                data_to_store['horas_servicio_comunidad_h'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD_H']

            if 'HORAS_SERVICIO_COMUNIDAD_O' in cleaned_record:
                data_to_store['horas_servicio_comunidad_o'] = cleaned_record['HORAS_SERVICIO_COMUNIDAD_O']

            if 'TOTAL_HORAS_AUTONOMAS' in cleaned_record:
                data_to_store['total_horas_autonomas'] = cleaned_record['TOTAL_HORAS_AUTONOMAS']

            if 'TOTAL_HORAS_AUTONOMAS_H' in cleaned_record:
                data_to_store['total_horas_autonomas_h'] = cleaned_record['TOTAL_HORAS_AUTONOMAS_H']

            if 'TOTAL_HORAS_AUTONOMAS_O' in cleaned_record:
                data_to_store['total_horas_autonomas_o'] = cleaned_record['TOTAL_HORAS_AUTONOMAS_O']

            if 'HORAS_TITULACION' in cleaned_record:
                data_to_store['horas_titulacion'] = cleaned_record['HORAS_TITULACION']

            if 'HORAS_TITULACION_H' in cleaned_record:
                data_to_store['horas_titulacion_h'] = cleaned_record['HORAS_TITULACION_H']

            if 'HORAS_TITULACION_O' in cleaned_record:
                data_to_store['horas_titulacion_o'] = cleaned_record['HORAS_TITULACION_O']

            if 'SESIONES_DOCENCIA' in cleaned_record:
                data_to_store['sesiones_docencia'] = cleaned_record['SESIONES_DOCENCIA']

            if 'SESIONES_LABORATORIO' in cleaned_record:
                data_to_store['sesiones_laboratorio'] = cleaned_record['SESIONES_LABORATORIO']

            if 'SESIONES_EXTERNADO' in cleaned_record:
                data_to_store['sesiones_externado'] = cleaned_record['SESIONES_EXTERNADO']

            if 'SEMANAS_EXTERNADO' in cleaned_record:
                data_to_store['semanas_externado'] = cleaned_record['SEMANAS_EXTERNADO']

            if 'SEMANAS_LABORATORIO' in cleaned_record:
                data_to_store['semanas_laboratorio'] = cleaned_record['SEMANAS_LABORATORIO']

            if 'HORAS_ADICIONALES_SILABO' in cleaned_record:
                data_to_store['horas_adicionales_silabo'] = cleaned_record['HORAS_ADICIONALES_SILABO']

            self.env['dara_mallas.acronym_comparison_result_202310'].create(data_to_store)




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