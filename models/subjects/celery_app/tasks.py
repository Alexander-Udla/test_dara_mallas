from . import celery_app
from odoo import api, SUPERUSER_ID
import io
import base64
import pandas as pd
import datetime
from . import metodos_homologation as metodos
import logging
from celery import shared_task
import odoo

_logger = logging.getLogger(__name__)

@celery_app.app.task(name='dara_mallas.models.subjects.celery_app.tasks.procesar_homologaciones')
def procesar_homologaciones(database_banner, period_id_name):
   # Nombre de la base de datos
    db_name = 'dara_mallas'

    # Crear un entorno con la base de datos y realizar operaciones
    with api.Environment.manage():
        cr = odoo.sql_db.db_connect(db_name).cursor()
        
        env = api.Environment(cr, SUPERUSER_ID, {})
            # Realiza operaciones con 'env'
        

    # Buscar un registro del modelo
    homologacion = env['dara_mallas.data_homologations'].search([], limit=1)
    # Simula tu validador
    validador = metodos.Validator(database_banner=database_banner)
    period = str(period_id_name)

    # Inicializa listas y datos
    res = validador.get_homologations_for_period(period=period)
    subjects_odoo_empty = []
    subjects_banner_empty = []
    data = []
    cont = 1

    # Procesar homologaciones
    for item in res:
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
        # Verificar datos faltantes
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
            data_compare_to = homologacion.compare_to(homologaciones_odoo, homologaciones_banner)
            data.extend(data_compare_to)

        cont += 1

    # Crear archivo CSV
    output = io.BytesIO()
    resultado = pd.DataFrame(data)
    fecha = datetime.datetime.now().strftime("%d%m%Y")
    resultado.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)

    # Codificar en base64 para Odoo
    archivo_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
    nombre_archivo = f"homologaciones-{fecha}-{period}.csv"

    _logger.info(f"Archivo generado: {nombre_archivo}")
    return {'file': archivo_base64, 'file_name': nombre_archivo}
