from odoo import fields, models, api
from ..repository.suplementario_repository import suplemetarioRepository
from odoo.exceptions import UserError

class SuplementarioValidador(models.TransientModel):
    _name = "dara_mallas.validador_suplementario"
    _description = "Validador suplementario de siglas"

    period_id=fields.Many2one("dara_mallas.period", string='Periodo')
    resultado = fields.Char(string = "resultado")

    def execute(self):
        print("VALOR SELECCIONADO " , self.period_id.name)
        if not self.period_id:
            raise UserError("Debe seleccionar un período antes de ejecutar la consulta.")

        repository = suplemetarioRepository(self.env)
        result = repository.get_information_banner(self.period_id.name)
        print("===========RESULTADO ", result)

        self.write({"resultado": result})

