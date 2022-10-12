

from odoo import fields, models, api

class uec_credit(models.Model):
    _name="dara_mallas.uec_credit"
    name=fields.Char("UEC Credito")
    credit_hr_ind=fields.Char('SCBCRSE_CREDIT_HR_IND',size=2 )
    credit_hr_low=fields.Float('SCBCRSE_CREDIT_HR_LOW',digits=(7,3))
    credit_hr_high=fields.Float('SCBCRSE_CREDIT_HR_HIGH',digits=(7,3))

    
        
class billed(models.Model):
    _name="dara_mallas.billed"
    
    name=fields.Char("Cobro")
    bill_hr_ind=fields.Char('SCBCRSE_BILL_HR_IND',size=2 )
    bill_hr_low=fields.Float('SCBCRSE_BILL_HR_LOW',digits=(7,3))
    bill_hr_high=fields.Float('SCBCRSE_BILL_HR_HIGH',digits=(7,3))