"""
import sys
sys.path.append('/odoo/odoo-server/odoo/addons')  # Agrega la ruta a los addons de Odoo


from celery import Celery # type: ignore

celery_app = Celery('odoo', broker='amqp://guest:guest@localhost//')  # RabbitMQ está corriendo localmente
celery_app.conf.update(
    result_backend='rpc://',  # Esto almacena los resultados de la tarea (puedes cambiarlo si prefieres otro backend)
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


# Asegúrate de que Celery descubra las tareas de los módulos adecuados
#celery_app.autodiscover_tasks(['odoo.addons.dara_mallas.models.subjects.reportes.categorias.tasks'])
"""

from celery import Celery # type: ignore
from celery.schedules import crontab # type: ignore
import sys
sys.path.append('/odoo/odoo-server/odoo/addons')
app = Celery('odoo', broker='redis://localhost:6379/0')
app.conf.update(
    #result_backend='redis://localhost:6379/0',
    result_backend='db+postgresql://postgres:root123@localhost/mallas',
    #include=['tasks']
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
)
app.autodiscover_tasks(['dara_mallas.models.subjects.reportes.database.celeryconfig'])