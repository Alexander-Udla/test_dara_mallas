'''
Created on Apr 12, 2019

@author: fbaez
'''

from odoo import fields,models

class corequisite(models.Model):
    _name="dara_mallas.corequisite"
    
    corequisite_subject_id=fields.Many2one("dara_mallas.subject")
    corequisite_subject_code=fields.Char("Sigla",related="corequisite_subject_id.code")

    corequisite_line_id=fields.Many2one("dara_mallas.corequisite_line")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.corequisite_subject_id.code),str(rec.corequisite_subject_id.name))))
        return result
class corequisite_line(models.Model):
    _name="dara_mallas.corequisite_line"
    
    period_id=fields.Many2one("dara_mallas.period",'Periodo') 
    subject_id=fields.Many2one("dara_mallas.subject",'Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    corequisite_ids=fields.One2many("dara_mallas.corequisite",inverse_name="corequisite_line_id",string="Correquisitos")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def copy(self,default=None):
        new_subject_corequisite_line=super(corequisite_line,self).copy(default=default)
        corequisitos = []
        for item in self.corequisite_ids:
            pre = {
                'corequisite_subject_id':item.corequisite_subject_id.id,
                'corequisite_line_id':new_subject_corequisite_line.id,
            }
            new_corequisite = self.env['dara_mallas.corequisite'].create(pre)
            corequisitos.append(new_corequisite.id)
        new_subject_corequisite_line.corequisite_ids=[(6,0,corequisitos)]
        return new_subject_corequisite_line

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result

