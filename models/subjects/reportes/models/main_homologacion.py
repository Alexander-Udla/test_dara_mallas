import subprocess
import os
from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError # type: ignore

import logging
_logger = logging.getLogger(__name__)


class MainHomologacion(models.Model):
    _name = 'dara_mallas.main_homologacion'
    _description =("Validador homologaciòn y prerequisitos.")

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    type = fields.Selection(selection=[("1", "Homologaciòn"), ("2", "Prerequisito")], string="Seleccione validador")
    file_links = fields.Html(string="Archivos Generados", compute="_compute_file_links")
    
    def action_execute_code(self):
        if self.period_id:
            period = self.env['dara_mallas.period'].browse(self.period_id.id)
            if period.exists():
                _logger.info("ID de period_id: %s", period.id)
                _logger.info("Nombre de period_id: %s", period.name)
            else:
                raise UserError("El periodo seleccionado no existe.")
        else:
            raise UserError("Debe seleccionar un periodo para ejecutar el script.")

            

        # Ruta completa a la carpeta del proyecto
        ruta_proyecto = '/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador'
        ruta_script = os.path.join(ruta_proyecto, 'main.py')

        # Verificar si el archivo existe
        if not os.path.exists(ruta_script):
            raise UserError("El script no se encuentra en la ubicación especificada.")

        # Ejecutar el script con Python
        try:
            process = subprocess.Popen(
                ["python3", ruta_script, str(self.type), str(self.period_id.name)],
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
    
    
    def _compute_file_links(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not self.type:
            raise UserError("Seleccione un validador")
        else:
            if self.type == "1":
                csv_directory = '/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/homologaciones/source/'
            else:                
                csv_directory = '/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/prerequisitos/source/'
        

        for record in self:
            if not os.path.exists(csv_directory):
                record.file_links = "<p>No hay archivos disponibles.</p>"
                continue

            # Generar enlaces de descarga desde static/csv/
            files = [
                f'<a href="{base_url}/dara_mallas/static/csv/source/{file}" target="_blank">{file}</a>'
                for file in os.listdir(csv_directory) if file.endswith('.csv')
            ]

            record.file_links = "<br/>".join(files) if files else "<p>No hay archivos disponibles.</p>"
    
    def update_file_links(self):
        self._compute_file_links()