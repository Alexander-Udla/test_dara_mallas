import json
from odoo import fields, models, api
from ..repository.acronym_repository import acronymRepository


class AcronymComparison(models.Model):
    _name = "dara_mallas.acronym_comparison"
    _description = "Comparativo de siglas"
    
    # Campos principales
    acronym1 = fields.Char("Sigla 1")
    acronym2 = fields.Char("Sigla 2")
    
    # Relación con los resultad    
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

