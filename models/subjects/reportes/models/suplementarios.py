from odoo import fields, models, api
from ..repository.suplementario_repository import suplemetarioRepository
from odoo.exceptions import UserError

class SuplementarioValidador(models.TransientModel):
    _name = "dara_mallas.validador_suplementario"
    _description = "Validador suplementario de siglas"

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    resultado = fields.Char(string = "resultado")
    resultado_odoo = fields.Char(string = "resultado_odoo")

    def execute(self):
        print("VALOR SELECCIONADO " , self.period_id.name)
        if not self.period_id:
            raise UserError("Debe seleccionar un período antes de ejecutar la consulta.")

        repository = suplemetarioRepository(self.env)
        result = repository.get_information_banner(self.period_id.name)
        print("===========RESULTADO ", result)

        coincidencias = []

        for item in result:
            codigo = item[0]  # Suponiendo que el código está en la primera columna
            result_odoo = repository.get_information_odoo(codigo)
            print("=======CODIGO",codigo, "================ENCONTRADO ", result_odoo)


        self.write({
            "resultado": str(result),
            "resultado_odoo": str(result_odoo),
        })
