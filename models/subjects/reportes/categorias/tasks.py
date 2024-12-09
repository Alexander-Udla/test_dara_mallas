from celery import shared_task
import odoo
from odoo.api import Environment
from math import ceil
import psycopg2  # type: ignore
import xlsxwriter
import base64
from io import BytesIO
from num2words import num2words
from odoo import registry


@shared_task
def generate_report_async(record_id):
    with odoo.api.Environment.manage():
        registry_instance = registry('mallas')
        with registry_instance.cursor() as cr:
            env = Environment(cr, odoo.SUPERUSER_ID, {})
            record = env["dara_mallas.data_homologations"].browse(record_id)
            if not record.exists():
                return

            def numero_a_texto(numero):
                return num2words(numero, lang='es').capitalize()

            # Generar datos para el Excel
            data = [{'numero': i, 'texto': numero_a_texto(i)} for i in range(1, 1001)]  # Cambia el rango según tus necesidades

            # Dividir los datos en lotes de 100
            batch_size = 100
            total_batches = ceil(len(data) / batch_size)

            for batch_number in range(total_batches):
                batch_data = data[batch_number * batch_size:(batch_number + 1) * batch_size]

                # Crear el archivo Excel en un buffer
                output = BytesIO()
                workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                worksheet = workbook.add_worksheet(f"Lote {batch_number + 1}")

                # Escribir encabezados
                worksheet.write(0, 0, 'Número')
                worksheet.write(0, 1, 'Texto')

                # Escribir datos
                row = 1
                for record_data in batch_data:
                    worksheet.write(row, 0, record_data['numero'])
                    worksheet.write(row, 1, record_data['texto'])
                    row += 1

                workbook.close()

                # Codificar el archivo en Base64
                excel_data = base64.b64encode(output.getvalue())
                output.close()

                # Crear un nuevo registro relacionado
                env["dara_mallas.data_homologations"].create({
                    'file': excel_data,
                    'file_name': f'numeros_y_texto_lote_{batch_number + 1}.xlsx',
                    'parent_id': record.id,
                })

    return f"Reporte generado exitosamente para el registro {record_id}"
