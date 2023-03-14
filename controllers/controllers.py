# -*- coding: utf-8 -*-
from odoo import http
import json

class CreateObjects(http.Controller):
    @http.route('/create/objectos/<string:program_code>/',type='json', auth='public')
    def index(self,program_code,**kw):
        #data = json.loads(http.request.httprequest.data)
        subject = http.request.env['dara_mallas.subject'].search([('code','=',program_code)])
        period = http.request.env['dara_mallas.period'].search([('name','=','202300')])
        weighing = http.request.env['dara_mallas.weighing'].search([('code','=','P70')])
        subject_scadtl = http.request.env['dara_mallas.subject_scadtl'].search([('subject_id','=',subject.id)])
        subject_scadtl_max = subject_scadtl.sorted(key=lambda r: r.period_id.name , reverse=True)[0]

        cheack_subject_scadtl = http.request.env['dara_mallas.subject_scadtl'].search([('subject_id','=',subject.id),('period_id','=',period.id)])
        try:
            if not cheack_subject_scadtl:
                subject_scadtl_new = http.request.env['dara_mallas.subject_scadtl'].create({
                    'subject_id':subject.id,
                    'period_id':period.id,
                    'weighing_id':weighing.id,
                    'coordinador_id':subject_scadtl_max.coordinador_id.id,
                    'program_code_id':subject_scadtl_max.program_code_id.id,

                })

                subject_inherit = http.request.env['dara_mallas.subject_inherit'].search([('subject_id','=',subject.id)])
                for item in subject_inherit:
                    item.write(
                        {
                        'subject_scadtl_id':subject_scadtl_new.id
                        }
                    )

            else:
                subject_inherit = http.request.env['dara_mallas.subject_inherit'].search([('subject_id','=',subject.id)])
                for item in subject_inherit:
                    item.write(
                        {
                        'subject_scadtl_id':subject_scadtl_max.id
                        }
                    )
                print("sigla ya existe")
            data = {
            'res':'ok %s'%(program_code),
            }
            return json.dumps(data)
        except Exception as e:
            data = {
                'res':'fail %s'%(program_code),
                }
            return json.dumps(data)

#     @http.route('/custom/addons/dara_rdas/custom/addons/dara_rdas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom/addons/dara_rdas.listing', {
#             'root': '/custom/addons/dara_rdas/custom/addons/dara_rdas',
#             'objects': http.request.env['custom/addons/dara_rdas.custom/addons/dara_rdas'].search([]),
#         })

#     @http.route('/custom/addons/dara_rdas/custom/addons/dara_rdas/objects/<model("custom/addons/dara_rdas.custom/addons/dara_rdas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom/addons/dara_rdas.object', {
#             'object': obj
#         })
