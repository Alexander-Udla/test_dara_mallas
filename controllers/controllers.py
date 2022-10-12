# -*- coding: utf-8 -*-
# from odoo import http


# class DaraMallas(http.Controller):
#     @http.route('/dara_mallas/dara_mallas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dara_mallas/dara_mallas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dara_mallas.listing', {
#             'root': '/dara_mallas/dara_mallas',
#             'objects': http.request.env['dara_mallas.dara_mallas'].search([]),
#         })

#     @http.route('/dara_mallas/dara_mallas/objects/<model("dara_mallas.dara_mallas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dara_mallas.object', {
#             'object': obj
#         })
