import xlsxwriter  # type: ignore
import psycopg2  # type: ignore
import base64
import io
from odoo import fields, models, api  # type: ignore
from odoo.exceptions import UserError  # type: ignore
from io import BytesIO
from reportlab.pdfgen import canvas
import pandas as pd
from ..validador.homologaciones import metodos_validador as metodos
from datetime import date

# Obtener la fecha actual
fecha_actual = date.today()

class DataHomologation(models.Model):
    _name = "dara_mallas.data_homologations"
    _description = "Conexión a base de datos y generación de PDF"
    
    status = fields.Selection([("pruebas", "Pruebas"), ("produccion", "Producción")], string="Estado")
    period_id = fields.Many2one("dara_mallas.period", 'Periodo')
    file = fields.Binary("Archivo")    
    file_name = fields.Char("Nombre del Archivo")

    def generate_report(self):
        database_banner = 'banner' if self.status == 'produccion' else 'banner_test'
        validador = metodos.Validator(database_banner=database_banner)
        period = str(self.period_id.name)
        
        # Obtener los homologaciones
        res = validador.get_homologations_for_period(period=period)

        subjects_odoo_empty = []
        subjects_banner_empty = []
        data = []

        for cont, item in enumerate(res, start=1):
            print(f"{cont} de {len(res)}")

            homologaciones_odoo = validador.get_homologations_for_subject_period_area(
                subject_code=item['REGLA'],
                period=item['PERIODO'],
                area=item['AREA'],
                period_val=period
            )
            homologaciones_banner = validador.get_homologations_for_subject_period_area_banner(
                subject_code=item['REGLA'],
                period=period,
                area=item['AREA']
            )
            
            if not homologaciones_odoo:
                subjects_odoo_empty.append([item['REGLA'], item['PERIODO'], item['AREA']])
            if not homologaciones_banner:
                subjects_banner_empty.append([item['REGLA'], item['PERIODO'], item['AREA']])

                data.append({
                    'PERIODO': item['PERIODO'],
                    'AREA': item['AREA'],
                    'REGLA': item['REGLA'],
                    'CONECTOR': '',
                    'SIGLA': '',
                    'PRUEBA': '',
                    'TEST_PUNTAJE_MINIMO': '',
                    'TEST_PUNTAJE_MAXIMO': '',
                    'REGLA_PUNTAJE_MINIMO': '',
                    'REGLA_ATRIBUTO': '',
                    'ESTADO': f'En Banner {item["REGLA"]} no se encontró'
                })

            if homologaciones_banner and homologaciones_odoo:
                data_compare_to = self.compare_to(homologaciones_odoo=homologaciones_odoo, homologaciones_banner=homologaciones_banner)
                data.extend(data_compare_to)
        
        # Generación del archivo Excel
        output = io.BytesIO()
        resultado = pd.DataFrame(data)
       
        fecha = fecha_actual.strftime("%d%m%Y")
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            resultado.to_excel(writer, index=False, sheet_name='Homologaciones')
        
        output.seek(0)
        
        self.write({
            'file': base64.b64encode(output.getvalue()),
            'file_name': f'homologaciones-{fecha}-{self.period_id.name}.xlsx'
        })

    def compare_to(self, homologaciones_odoo, homologaciones_banner):
        data_compare = []
        for item_odoo in homologaciones_odoo:
            errores = ""
            exists = False
            conector = False
            
            for item_banner in homologaciones_banner:
                if self.compare_items(item_odoo, item_banner):
                    exists = True
                    conector = True
                    errores += self.generate_error_messages(item_odoo, item_banner)

            if not exists:
                errores += f"Sigla no existe en Banner {item_odoo['SIGLA']}"
            if not conector and exists:
                errores += f"Sigla existe en Banner {item_odoo['SIGLA']} pero el conector es incorrecto {item_odoo['CONECTOR']}"
            
            data_compare.append(self.format_comparison_result(item_odoo, errores))
        
        return data_compare

    def compare_items(self, item_odoo, item_banner):
        # Verifica si los items coinciden en los criterios
        return item_odoo['PERIODO'] == item_banner['PERIODO'] and \
               item_odoo['AREA'] == item_banner['AREA'] and \
               item_odoo['REGLA'] == item_banner['REGLA']

    def generate_error_messages(self, item_odoo, item_banner):
        errores = ""
        # Agregar la comparación detallada de los atributos
        for field in ['SIGLA', 'CONECTOR', 'PRUEBA', 'TEST_PUNTAJE_MINIMO', 'TEST_PUNTAJE_MAXIMO', 'REGLA_PUNTAJE_MINIMO', 'REGLA_ATRIBUTO']:
            if item_odoo[field] != item_banner[field]:
                errores += f"Error en {field} {item_odoo[field]} , {item_banner[field]} "
        return errores

    def format_comparison_result(self, item_odoo, errores):
        return {
            'PERIODO': item_odoo['PERIODO'],
            'AREA': item_odoo['AREA'],
            'REGLA': item_odoo['REGLA'],
            'CONECTOR': item_odoo['CONECTOR'],
            'SIGLA': item_odoo['SIGLA'],
            'PRUEBA': item_odoo['PRUEBA'],
            'TEST_PUNTAJE_MINIMO': item_odoo['TEST_PUNTAJE_MINIMO'],
            'TEST_PUNTAJE_MAXIMO': item_odoo['TEST_PUNTAJE_MAXIMO'],
            'REGLA_PUNTAJE_MINIMO': item_odoo['REGLA_PUNTAJE_MINIMO'],
            'REGLA_ATRIBUTO': item_odoo['REGLA_ATRIBUTO'],
            'ERRORES': errores
        }
