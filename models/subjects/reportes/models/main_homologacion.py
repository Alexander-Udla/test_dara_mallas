import subprocess
import os
from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError # type: ignore
import shutil

import logging
_logger = logging.getLogger(__name__)


class MainHomologacion(models.Model):
    _name = 'dara_mallas.main_homologacion'
    _description =("Validador homologaciòn y prerequisitos.")

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    type = fields.Selection(selection=[("1", "Homologaciòn"), ("2", "Prerequisito")], string="Seleccione validador:")
    data_base = fields.Selection(selection=[("banner_test", "Banner-Pruebas"), 
                                            ("banner", "Banner-Producciòn"),
                                            ("banner_devl", "Banner-Devl"),
                                            ("banner_migr", "Banner-Migr")], 
                                            string="Base de datos:")

    file_links = fields.Html(string="Archivos Generados", compute="_compute_file_links")
    state = fields.Char(string="Estado", compute="_compute_status")

    
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
                ["python3", ruta_script, str(self.type), str(self.period_id.name), str(self.data_base)],
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
    
    """
    def _compute_file_links(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for record in self:
            if not record.type:
                record.file_links = "<p>Seleccione un validador.</p>"
                continue

            # Definir la ruta correcta según el tipo de validador
            if record.type == "1":
                print("=======ENVIAR HOMOLOGACIÒN")
                csv_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/homologaciones/source/"
            elif record.type == "2":
                print("=======ENVIAR PREREQUISITO")
                csv_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/prerequisitos/source/"
            else:
                print("=======SIN SELECCION")
                record.file_links = "<p>Tipo de validador desconocido.</p>"
                continue

            if not os.path.exists(csv_directory):
                record.file_links = "<p>No hay archivos disponibles.</p>"
                continue

            # Generar enlaces de descarga desde static/csv/source/
            files = [
                f'<a href="{base_url}/dara_mallas/static/csv/source/{file}" target="_blank">{file}</a>'
                for file in os.listdir(csv_directory) if file.endswith('.csv')
            ]

            record.file_links = "<br/>".join(files) if files else "<p>No hay archivos disponibles.</p>"
"""
    def _compute_file_links(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for record in self:
            if not record.type:
                record.file_links = "<p>Seleccione un validador.</p>"
                continue

            # Rutas de los archivos generados
            if record.type == "1":
                source_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/homologaciones/source/"
            elif record.type == "2":
                source_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/prerequisitos/source/"
            else:
                record.file_links = "<p>Tipo de validador desconocido.</p>"
                continue

            static_directory = "/odoo/custom/addons/dara_mallas/static/csv/source/"

            if not os.path.exists(static_directory):
                os.makedirs(static_directory)  # Crear si no existe

            if not os.path.exists(source_directory):
                record.file_links = "<p>No hay archivos disponibles.</p>"
                continue

            files = []
            for file in os.listdir(source_directory):
                if file.endswith('.xlsx'):
                    source_file = os.path.join(source_directory, file)
                    target_file = os.path.join(static_directory, file)

                    # Copiar solo si el archivo ha cambiado
                    if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                        shutil.copy2(source_file, target_file)

                    # Generar enlaces de descarga
                    file_url = f"{base_url}/dara_mallas/static/csv/source/{file}"
                    files.append(f'<a href="{file_url}" target="_blank">{file}</a>')

            record.file_links = "<br/>".join(files) if files else "<p>No hay archivos disponibles.</p>"


    
    def update_file_links(self):
        self._compute_file_links()

    def _compute_status(self):
        """Revisar el estado del procesamiento."""
        for record in self:
            if not record.period_id:
                record.state = "Desconocido"
                continue

            # Ruta del estado
            status_file = f"/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/status/status_{record.period_id.name}.txt"

            if not os.path.exists(status_file):
                record.state = "Pendiente"
            else:
                with open(status_file, "r") as f:
                    record.state = f.read().strip()

    def update_status(self):
        """Actualiza el estado del archivo y muestra una notificación."""
        for record in self:
            record._compute_status()
        
        message = f"Estado actualizado: {self.state}"  
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

