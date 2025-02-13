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
    
    def _compute_file_links(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for record in self:
            if not record.type:
                record.file_links = "<p>Seleccione un validador.</p>"
                continue

            # Definir la ruta correcta según el tipo de validador
            """"""
            if record.type == "1":
                source_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/homologacions/source/"
                print("============== HOMOLOGACION ")
                url_directory = f"{base_url}/dara_mallas/static/csv/source/"
                
            elif record.type == "2":
                source_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/source/"
                print("============== PREREQUISITO ")
                url_directory = f"{base_url}/dara_mallas/static/csv/source"
            else:
                record.file_links = "<p>Tipo de validador desconocido.</p>"
                continue

            if not os.path.exists(source_directory):
                record.file_links = "<p>No hay archivos disponibles.</p>"
                continue
            """"""
            # Generar enlaces de descarga directamente
            files = [
                f'<a href="{url_directory}{file}" target="_blank">{file}</a>'
                for file in os.listdir(source_directory) if file.endswith('.xlsx') or file.endswith('.csv')
            ]

            record.file_links = "<br/>".join(files) if files else "<p>No hay archivos disponibles.</p>"
    
    """   

    def _compute_file_links(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for record in self:
            if not record.type:
                record.file_links = "<p>Seleccione un validador.</p>"
                continue

            # Directorio de origen donde se generan los archivos
            source_directory = "/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/source/"

            # Directorio donde Odoo sirve archivos estáticos
            static_directory = "/odoo/custom/addons/dara_mallas/static/csv/source/"
            url_directory = f"{base_url}/web/static/dara_mallas/csv/source/"

            # Asegurar que la carpeta estática exista
            if not os.path.exists(static_directory):
                os.makedirs(static_directory)

            # Mover archivos desde el directorio fuente al directorio estático
            moved_files = []
            for file in os.listdir(source_directory):
                if file.endswith('.xlsx') or file.endswith('.csv'):
                    source_path = os.path.join(source_directory, file)
                    destination_path = os.path.join(static_directory, file)

                    try:
                        shutil.move(source_path, destination_path)
                        moved_files.append(file)
                    except Exception as e:
                        _logger.error(f"Error al mover {file}: {str(e)}")

            # Generar enlaces de descarga
            files = [
                f'<a href="{url_directory}{file}" target="_blank">{file}</a>'
                for file in os.listdir(static_directory) if file.endswith('.xlsx') or file.endswith('.csv')
            ]

            record.file_links = "<br/>".join(files) if files else "<p>No hay archivos disponibles.</p>"
    """


    def update_file_links(self):
        for record in self:
            record._compute_file_links()
            record.write({})  # Forzar actualización


    def _compute_status(self):
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
        for record in self:
            record._compute_status()
        
        message = f"Estado actualizado: {self.state}"  
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

