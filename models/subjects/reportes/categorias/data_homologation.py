import xlsxwriter  # type: ignore
import psycopg2  # type: ignore
import base64
import io
from odoo import fields, models, api # type: ignore
from odoo.exceptions import UserError  # type: ignore
from io import BytesIO
from reportlab.pdfgen import canvas
import pandas as pd
from ..validador.homologaciones import metodos_validador as metodos
from datetime import date
from odoo.addons.queue_job.job import job  # Importa el decorador



# Obtener la fecha actual
fecha_actual = date.today()

class DataHomologation(models.Model):
    _name = "dara_mallas.data_homologations"
    _description = "Conexión a base de datos y generación de PDF"
    
    status = fields.Selection([("pruebas", "Pruebas"), ("produccion", "Producción")], string="Estado")
    period_id = fields.Many2one("dara_mallas.period", 'Periodo')
    file = fields.Binary("Archivo")    
    file_name = fields.Char("Nombre del Archivo")
    
    
    def action_generate_report_in_background(self):
        """Crea una tarea en la cola para generar el reporte"""
        self.ensure_one()  # Asegúrate de que solo se opera sobre un registro
        self.with_delay().generate_report()

    """
    @job
    def generate_report(self):
        database_banner = 'banner' if self.status == 'produccion' else 'banner_test'
        validador = metodos.Validator(database_banner=database_banner)
        period = str(self.period_id.name)
        
        # Obtener los homologaciones
        res = validador.get_homologations_for_period(period=period)
        print("respuesta ", res)
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
            
        print("datos finales ", data)
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})  
        sheet = workbook.add_worksheet("Reporte")
        header_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
        format1 = workbook.add_format({'font_size': 13, 'align': 'vcenter', 'bold': True})
        
        headers = [
            "Periodo", "Area", "Regla", "Conector", "Sigla", "Prueba", 
            "Test Puntaje Mínimo", "Test Puntaje Máximo", 
            "Regla Puntaje Mínimo", "Regla Atributo", "Errores"
        ]
        
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)
            
            
        for i, row in enumerate(data, start=1):
            sheet.write(i, 0, row.get('PERIODO', "Sin Definir"), format1)
            sheet.write(i, 1, row.get('AREA', "Sin Definir"), format1)
            sheet.write(i, 2, row.get('REGLA', "Sin Definir"), format1)
            sheet.write(i, 3, row.get('CONECTOR', "Sin Definir"), format1)
            sheet.write(i, 4, row.get('SIGLA', "Sin Definir"), format1)
            sheet.write(i, 5, row.get('PRUEBA', "Sin Definir"), format1)
            sheet.write(i, 6, row.get('TEST_PUNTAJE_MINIMO', "Sin Definir"), format1)
            sheet.write(i, 7, row.get('TEST_PUNTAJE_MAXIMO', "Sin Definir"), format1)
            sheet.write(i, 8, row.get('REGLA_PUNTAJE_MINIMO', "Sin Definir"), format1)
            sheet.write(i, 9, row.get('REGLA_ATRIBUTO', "Sin Definir"), format1)
            sheet.write(i, 10, row.get('ERRORES', "Sin Definir"), format1)

        workbook.close()
        output.seek(0)
        
        # Codificar en base64
        encoded_excel = base64.b64encode(output.read())
        print("Encoded Excel:", encoded_excel)
        
        self.write({
            'file': encoded_excel,
            'file_name': f"Homologacion_{self.period_id.name}.xlsx"
        })
        
        output.close()
        
        return {
        'type': 'ir.actions.act_url',
        'url': f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{encoded_excel.decode()}',
        'target': 'self',
        'download': self.period_id.name,
        
        }
                    
    """
    @job   
    def generate_report(self):
        try:
            database_banner = 'banner' if self.status == 'produccion' else 'banner_test'
            validador = metodos.Validator(database_banner=database_banner)
            period = str(self.period_id.name)
            
            try:
                # Obtener las homologaciones
                res = validador.get_homologations_for_period(period=period)
            except Exception as e:
                raise UserError(f"Error al obtener homologaciones para el periodo {period}: {str(e)}")
            
            
            subjects_odoo_empty = []
            subjects_banner_empty = []
            data = []

            for cont, item in enumerate(res, start=1):
                try:
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
                except Exception as e:
                    raise UserError(f"Error al obtener homologaciones para el sujeto {item['REGLA']}: {str(e)}")
                
                if not homologaciones_odoo:
                    subjects_odoo_empty.append([item['REGLA'], item['PERIODO'], item['AREA']])
                if not homologaciones_banner:
                    subjects_banner_empty.append([item['REGLA'], item['PERIODO'], item['AREA']])

                if homologaciones_banner and homologaciones_odoo:
                    try:
                        data_compare_to = self.compare_to(homologaciones_odoo=homologaciones_odoo, homologaciones_banner=homologaciones_banner)
                        data.extend(data_compare_to)
                    except Exception as e:
                        raise UserError(f"Error al comparar homologaciones: {str(e)}")

            try:
                # Generar el archivo Excel
                output = BytesIO()
                workbook = xlsxwriter.Workbook(output, {'in_memory': True})  
                sheet = workbook.add_worksheet("Reporte")
                header_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
                format1 = workbook.add_format({'font_size': 13, 'align': 'vcenter', 'bold': True})
                
                headers = [
                    "Periodo", "Area", "Regla", "Conector", "Sigla", "Prueba", 
                    "Test Puntaje Mínimo", "Test Puntaje Máximo", 
                    "Regla Puntaje Mínimo", "Regla Atributo", "Errores"
                ]
                
                for col, header in enumerate(headers):
                    sheet.write(0, col, header, header_format)
                    
                for i, row in enumerate(data, start=1):
                    sheet.write(i, 0, row.get('PERIODO', "Sin Definir"), format1)
                    sheet.write(i, 1, row.get('AREA', "Sin Definir"), format1)
                    sheet.write(i, 2, row.get('REGLA', "Sin Definir"), format1)
                    sheet.write(i, 3, row.get('CONECTOR', "Sin Definir"), format1)
                    sheet.write(i, 4, row.get('SIGLA', "Sin Definir"), format1)
                    sheet.write(i, 5, row.get('PRUEBA', "Sin Definir"), format1)
                    sheet.write(i, 6, row.get('TEST_PUNTAJE_MINIMO', "Sin Definir"), format1)
                    sheet.write(i, 7, row.get('TEST_PUNTAJE_MAXIMO', "Sin Definir"), format1)
                    sheet.write(i, 8, row.get('REGLA_PUNTAJE_MINIMO', "Sin Definir"), format1)
                    sheet.write(i, 9, row.get('REGLA_ATRIBUTO', "Sin Definir"), format1)
                    sheet.write(i, 10, row.get('ERRORES', "Sin Definir"), format1)
                
                workbook.close()
                output.seek(0)
                
                # Codificar en base64
                encoded_excel = base64.b64encode(output.read())
                print("Encoded Excel:", encoded_excel)
                
                self.write({
                    'file': encoded_excel,
                    'file_name': f"Homologacion_{self.period_id.name}.xlsx"
                })
                
                output.close()
            except Exception as e:
                raise UserError(f"Error al generar el archivo Excel: {str(e)}")
            
            return {
                'type': 'ir.actions.act_url',
                'url': f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{encoded_excel.decode()}',
                'target': 'self',
                'download': self.period_id.name,
            }
        
        except Exception as e:
            # Captura cualquier otro error inesperado
            raise UserError(f"Error inesperado: {str(e)}")




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
