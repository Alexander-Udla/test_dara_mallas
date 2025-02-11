from odoo import fields, models
from ..repository.suplementario_repository import suplemetarioRepository
from odoo.exceptions import UserError
import base64
import io
import pandas as pd

class SuplementarioValidador(models.TransientModel):
    _name = "dara_mallas.validador_suplementario"
    _description = "Validador suplementario de siglas"

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    resultado = fields.Char(string = "resultado")
    resultado_odoo = fields.Html(string = "resultado_odoo")
    excel_file = fields.Binary(string="Archivo Excel", readonly=True)
    excel_filename = fields.Char(string="Nombre del archivo")

    def execute(self):

        if not self.period_id:
            raise UserError("Debe seleccionar un período antes de ejecutar la consulta.")

        repository = suplemetarioRepository(self.env)
        result = repository.get_information_banner(self.period_id.name)        

        diferencias_lista = []

        for item in result:
            codigo = item[0] 
            result_odoo = repository.get_information_odoo(codigo)

            if result_odoo:
                clean_result_odoo = tuple(val.strip() if isinstance(val, str) else val for val in result_odoo[0])
            else:
                clean_result_odoo = ("Sin datos",) * len(item)

            diferencia = {
                "Código": codigo,
                "Periodo": clean_result_odoo[1] if item[1] != clean_result_odoo[1] else "",
                "Ponderación": clean_result_odoo[2] if item[2] != clean_result_odoo[2] else "",
                "Coordinador": clean_result_odoo[3] if item[3] != clean_result_odoo[3] else "",
                "Programa": clean_result_odoo[4] if item[4] != clean_result_odoo[4] else "",
            }


            if any(value for key, value in diferencia.items() if key != "Código"):
                diferencias_lista.append(diferencia)

        if diferencias_lista:
            df = pd.DataFrame(diferencias_lista)
            df = df.loc[:, (df != "").any(axis=0)]
        else:
            df = pd.DataFrame(columns=["Código", "Periodo", "Ponderación", "Coordinador", "Programa"])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Diferencias", index=False)

        output.seek(0)  # Regresar al inicio del archivo para lectura

        # Convertir a Base64
        file_data = base64.b64encode(output.read())

        # Nombre del archivo con fecha actual
        fecha = fields.Datetime.now().strftime("%d%m%Y")
        filename = f"Validador_{fecha}.xlsx"
    
        # Guardar en el modelo para la descarga
        self.write({
            "excel_file": file_data,
            "excel_filename": filename,
            "resultado_odoo": "Archivo generado correctamente." if diferencias_lista else "No se encontraron diferencias."
        })