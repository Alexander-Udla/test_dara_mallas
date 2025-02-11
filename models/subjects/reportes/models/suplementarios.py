from odoo import fields, models, api
from ..repository.suplementario_repository import suplemetarioRepository
from odoo.exceptions import UserError

class SuplementarioValidador(models.TransientModel):
    _name = "dara_mallas.validador_suplementario"
    _description = "Validador suplementario de siglas"

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    resultado = fields.Char(string = "resultado")
    resultado_odoo = fields.Html(string = "resultado_odoo")

    def execute(self):

        if not self.period_id:
            raise UserError("Debe seleccionar un período antes de ejecutar la consulta.")

        repository = suplemetarioRepository(self.env)
        result = repository.get_information_banner(self.period_id.name)

        diferencias_texto = []

        for item in result:
            codigo = item[0] 
            result_odoo = repository.get_information_odoo(codigo)

            if result_odoo:
                clean_result_odoo = tuple(val.strip() if isinstance(val, str) else val for val in result_odoo[0])
            else:
                clean_result_odoo = ("Sin datos",) * len(item)

            # Comparar campo por campo y guardar solo las diferencias
            diferencias_campos = []

            if item[1] != clean_result_odoo[1]:  # Comparación del periodo
                diferencias_campos.append(f"    - Periodo: Banner → {item[1]}, Odoo → {clean_result_odoo[1]}")

            if item[2] != clean_result_odoo[2]:  # Comparación de ponderación
                diferencias_campos.append(f"    - Ponderación: Banner → {item[2]}, Odoo → {clean_result_odoo[2]}")

            if item[3] != clean_result_odoo[3]:  # Comparación de coordinador
                diferencias_campos.append(f"    - Coordinador: Banner → {item[3]}, Odoo → {clean_result_odoo[3]}")

            if item[4] != clean_result_odoo[4]:  # Comparación de programa
                diferencias_campos.append(f"    - Programa: Banner → {item[4]}, Odoo → {clean_result_odoo[4]}")

            # Si hay diferencias, agregarlas a la lista
            if diferencias_campos:
                diferencias_texto.append(f"Código: {codigo}\n" + "\n".join(diferencias_campos) + "\n")

        diferencias_final = "<br/>".join(diferencias_texto) if diferencias_texto else "No se encontraron diferencias."

        print("DESPUES ", diferencias_final)
        # Guardar el resultado en el campo resultado_odoo
        self.write({
            "resultado_odoo": diferencias_final
        })