import subprocess
import os
from odoo import models, api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class MainHomologacion(models.Model):
    _name = 'dara_mallas.main_homologacion'

    @api.model
    def action_execute_code(self,*args, **kwargs):
        # Ruta completa a la carpeta del proyecto
        ruta_proyecto = '/home/odoo/Descargas/Validador/'
        #ruta_proyecto = '/home/odoo/Descargas/'

        # Ruta del script a ejecutar
        #ruta_script = os.path.join(ruta_proyecto, 'pruebas.py')
        ruta_script = os.path.join(ruta_proyecto, 'main.py')
        print("Ruta completa ", ruta_script)

        # Verificar si el archivo existe
        if not os.path.exists(ruta_script):
            _logger.warning("************************VALIDACION FINALIZADA********************************")
            raise UserError("El script no se encuentra en la ubicación especificada.")

        # Ejecutar el script con Python
        
        try:
            _logger.warning("*****txt***********EXIST***********")
            # Usar Popen y redirigir salidas para evitar bloqueos
            process = subprocess.Popen(
                ["python3", ruta_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True  # Liberar recursos del proceso padre
            )
            # Opcional: Si no necesitas la salida, puedes omitir stdout/stderr
            _logger.info("Script ejecutado en segundo plano (PID: %s)", process.pid)
        except Exception as e:
            _logger.error("Error al iniciar el proceso: %s", str(e))
            raise UserError("Error al iniciar el script externo.")
    
        return True

