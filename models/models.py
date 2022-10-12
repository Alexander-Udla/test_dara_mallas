# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class dara_mallas(models.Model):
#     _name = 'dara_mallas.dara_mallas'
#     _description = 'dara_mallas.dara_mallas'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
