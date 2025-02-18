from odoo import fields, models
from ..repository.suplementario_repository import suplemetarioRepository
from odoo.exceptions import UserError
import base64
import io
import pandas as pd

class SuplementarioValidador(models.TransientModel):
    _name = "dara_mallas.validador_suplementario"
    _description = "Validador suplementario de siglas"

    period_id=fields.Many2one("dara_mallas.period", string='Periodo de programación académica banner')
    resultado = fields.Char(string = "resultado")
    resultado_odoo = fields.Html(string = "resultado_odoo")
    excel_file = fields.Binary(string="Archivo Excel", readonly=True)
    excel_filename = fields.Char(string="Nombre del archivo")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )


    def son_ponderaciones_iguales(self, valor1, valor2)
        equivalencias = {
            "P-AR": "Ponderación Aprueba/Reprueba",
            "Ponderación Aprueba/Reprueba": "P-AR"
        }
        return valor1 == valor2 or equivalencias.get(valor1) == valor2

    def execute(self):

        if not self.period_id:
            raise UserError("Debe seleccionar un período antes de ejecutar la consulta.")

        repository = suplemetarioRepository(self.env)
        result = repository.get_information_banner(self.period_id.name)        
        diferencias_lista = []

        #for item in result:
        for idx, item in enumerate(result, start=1): 
            codigo = item[0] 
            result_odoo = repository.get_information_odoo(codigo)
            if result_odoo:
                clean_result_odoo = tuple(val.strip() if isinstance(val, str) else val for val in result_odoo[0])
            else:
                clean_result_odoo = ("Sin datos",) * len(item)

            hay_diferencias = any([
                not self.son_ponderaciones_iguales(item[2], clean_result_odoo[2]),
                item[3] != clean_result_odoo[3],
                item[4] != clean_result_odoo[4]
            ])

            diferencia = {
                "Código": codigo,
                "Periodo Banner": item[1] if item[1] != clean_result_odoo[1] or hay_diferencias else "",
                "Periodo Odoo": clean_result_odoo[1] if item[1] != clean_result_odoo[1] or hay_diferencias else "",
                "Ponderación Banner": item[2] if not self.son_ponderaciones_iguales(item[2], clean_result_odoo[2]) else "",
                "Ponderación Odoo": clean_result_odoo[2] if not self.son_ponderaciones_iguales(item[2], clean_result_odoo[2]) else "",
                "Coordinador Banner": item[3] if item[3] != clean_result_odoo[3] else "",
                "Coordinador Odoo": clean_result_odoo[3] if item[3] != clean_result_odoo[3] else "",
                "Programa Banner": item[4] if item[4] != clean_result_odoo[4] else "",
                "Programa Odoo": clean_result_odoo[4] if item[4] != clean_result_odoo[4] else "",
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
        filename = f"Validador_{self.period_id.name}_{fecha}.xlsx"
    
        # Guardar en el modelo para la descarga
        self.write({
            "excel_file": file_data,
            "excel_filename": filename,
            "resultado_odoo": "Archivo generado correctamente." if diferencias_lista else "No se encontraron diferencias."
        })