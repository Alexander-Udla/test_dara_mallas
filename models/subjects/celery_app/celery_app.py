from celery import Celery
from celery.schedules import crontab
import sys
sys.path.append('/odoo/odoo-server/odoo/addons')
app = Celery('odoo', broker='redis://localhost:6379/0')
app.conf.update(
    #result_backend='redis://localhost:6379/0',
    result_backend='db+postgresql://postgres:jde.2020@localhost/dara_mallas',
    #include=['tasks']
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
)
app.autodiscover_tasks(['dara_mallas.models.subjects.celery_app.celery_app'])
