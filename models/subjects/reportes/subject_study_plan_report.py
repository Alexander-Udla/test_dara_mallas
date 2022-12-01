'''
Created on Apr 4, 2019

@author: fbaez
'''

from odoo import tools
from odoo import api, fields, models




class prerrequisites_report(models.Model):
    _name="dara_mallas.subject_study_plan_report"
    
   
    _description = "Mallas por asignatura"
    _auto = False
    _order = "program_name"

    

    subject= fields.Char('Sigla')
    study_plan_id=fields.Many2one('dara_mallas.study_plan')
    program_name = fields.Char("Program",related='study_plan_id.program_id.name')
    #===========================================================================
    # study_plan_class_id=fields.Many2one('dara_mallas.study_plan_class')
    #===========================================================================
    def _select(self,subject_id):
        cadena = "("
        for count,item in enumerate(subject_id,start=0):
            if count == len(subject_id)-1:
                cadena +="'"+item.code+"'"
            else:
                cadena +="'"+item.code+"',"
        cadena += ")"
        select_str = """
            select min(s.id) as id 
                    , concat(s.code,' ',s.name) as subject
                    , sp.id as study_plan_id
                    , pr.name as program_name
                    --,splc.id as study_plan_class_id
                from dara_mallas_study_plan_line spl
                left join dara_mallas_study_plan sp on spl.study_plan_id =sp.id
                left join dara_mallas_area_homologation ah on spl.area_homologation_id = ah.id
				left join dara_mallas_subject_inherit_area sia ON  ah.id = sia.area_homologation_id
                left join dara_mallas_subject_inherit si on sia.subject_inherit_id = si.id
                left join dara_mallas_subject s on si.subject_id = s.id
                left join dara_mallas_program pr on pr.id=sp.program_id
                --left join dara_mallas_period p on p.id=sp.period_id
                --eft join dara_mallas_study_plan_class splc on splc.id=sp.study_plan_class_id
                where s.code in """+cadena+"""
                group by s.id ,sp.id ,pr.name
                order by 3 desc
        """ 
        return select_str
    


    
    def cargar(self,subject_id):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s           
            )""" % (self._table, self._select(subject_id)))
    
   

class subjectMallasDeSigla(models.TransientModel): 
    _name="dara_mallas.subject_mallas_sigla"
    subject_id=fields.Many2many("dara_mallas.subject_pivot",default=lambda self:self.env.context.get('subject_id',False),string="Asignaturas")
    #subject_id=fields.Char("dara_mallas.subject")
    @api.onchange('subject_id')
    def get_data(self):
        self.env['dara_mallas.subject_pivot'].get_data_subject()

    
    def generate_malla_sigla(self):
        self.env['dara_mallas.subject_study_plan_report'].cargar(self.subject_id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dara_mallas.subject_study_plan_report',
            'view_mode': 'pivot',
            'view_type': 'pivot',
            'target': 'current',
            'name': 'Mallas de sigla',
            'domain': [],
            'context': {
                        'subject_id':self.subject_id
                        },
        }

class subject_pivot(models.Model):
    _name="dara_mallas.subject_pivot"
    

    name = fields.Char("Nombre Asignatura")
    code = fields.Char("Codigo")

    def _select(self):
        select_str = """
            select s.code as code
                    ,s.name as name
                    from dara_mallas_subject s
            where s.code not in (select p.code from dara_mallas_subject_pivot p )
                
        """ 
        return select_str

    
    def get_data_subject(self):
        self.env.cr.execute("""INSERT INTO %s(code,name)
            %s 
          

            """ % (self._table, self._select()))
