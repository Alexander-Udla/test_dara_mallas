'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models,api

class subject_prerequisite_line(models.Model):
    _name="dara_mallas.prerequisite_line"

    period_id=fields.Many2one("dara_mallas.period",'Periodo')
    subject_id=fields.Many2one('dara_mallas.subject','Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    subject_prerequisite_ids = fields.One2many("dara_mallas.prerequisite",inverse_name="prerequisite_line_id",string="Prerrequisitos")
    prerequisites_check = fields.Text(string="Comment")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    
    def copy(self,default=None):
        new_subject_prerequisite_line=super(subject_prerequisite_line,self).copy(default=default)
        prerequisites = []
        for item in self.subject_prerequisite_ids:
            pre = {
                'prerequisite_subject_id':item.prerequisite_subject_id.id,
                'condition':item.condition,
                'conector':item.conector,
                'or_conector':item.or_conector,
                'lparen':item.lparen,
                'test_code':item.test_code,
                'test_score':item.test_score,
                'grade_id':item.grade_id.id,
                'score_id':item.score_id.id,
                'rparen':item.rparen,
                'seq':item.seq,
                'prerequsite_type':item.prerequsite_type,
                'prerequisite_line_id':new_subject_prerequisite_line.id,
            }
            new_prerequisite = self.env['dara_mallas.prerequisite'].create(pre)
            prerequisites.append(new_prerequisite.id)
        new_subject_prerequisite_line.subject_prerequisite_ids=[(6,0,prerequisites)]
        return new_subject_prerequisite_line

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result
    
    @api.onchange('subject_prerequisite_ids') 
    def onchange_prerequisites_check_ids(self):
        #self.asisted_hours=self.practicing_hours+self.application_hours+self.community_service_hours+self.lab_application_hours       
        self.check_prerequisites()

    def check_prerequisites(self):
        cadena = []
        #df_resultados = pd.DataFrame(columns=['subject_code','prerequisites'])
        seqRes = True
        #ordena el secuencial y verifica si existen suplicados
        for iterint in range(len(self.subject_prerequisite_ids)+1): 
            i=0
            for prerequisite in self.subject_prerequisite_ids:
                if prerequisite['seq'] == iterint:
                    if prerequisite['conector']:
                        if prerequisite['conector']=='O':
                            conector='||'
                        if prerequisite['conector']=='Y':
                            conector ='&&'
                        cadena.append(conector)
                    if prerequisite['lparen']:
                        cadena.append(prerequisite['lparen'])
                    if prerequisite['test_code']:
                        cadena.append(prerequisite['test_code'])
                    if prerequisite['prerequisite_subject_code']:
                        cadena.append(prerequisite['prerequisite_subject_code'])
                    if prerequisite['rparen']:
                        cadena.append(prerequisite['rparen'])
                    i+=1
            if i >1:
                seqRes = False
            
        if len(self.subject_prerequisite_ids)==0:
            self.prerequisites_check = ""

        if seqRes: 
            #df_resultados = df_resultados.append({'subject_code':self.code, 'prerequisites':' '.join(elem for elem in cadena)}, ignore_index=True)
            paren_number=0
            cadena2=[]
            cadena21=[]
            for item in cadena:
               
                if item =='(':
                    paren_number+=1
                if item==')':
                    paren_number -=1
                if item not in ('(',')'):
                    cadena2.append(item)
                cadena21.append(item)
            
            if paren_number ==0:
                contador=0
                contador2 = 0
                res = True
                for item in cadena21:
                   
                    if contador2+1 == len(cadena21):
                        break
                    if len(item)>2 and cadena21[contador2+1] in (('(')) or item == ')' and cadena21[contador2+1] in (('(')) or item == ')' and len(cadena21[contador2+1])>2 or  len(item) >2 and len(cadena21[contador2+1])>2 :
                        res = False
                        break
                    else:
                        res = True
                    contador2+=1
                
                for item in cadena2:
                        
                    if cadena2.index(item,contador,len(cadena2))%2 ==0 and item in ('||','&&') or cadena2[len(cadena2)-1] in ('||','&&') or res == False:
                        text = "ERROR EN PREREQUISITOS, NO ESTAN BIEN DEFINIDOS LOS OPERADORES"
                        self.hours_validation = text
                        self.prerequisites_check = text
                        break
                    else:
                        cadena3 = ""
                        for item in cadena21:
                            cadena3+=" "+item
                            
                        self.prerequisites_check = str(cadena3)
                        self.hours_validation = ""
                    contador+=1
            else:
                text = "ERROR PREREQUISITOS no concuerdan el número de parentesis en la estructura"
                self.hours_validation = text
                self.prerequisites_check = text
                
        else:
            text = "ERROR EN LA SECUENCIA"
            self.hours_validation = text
            self.prerequisites_check = text


class subject_prerequisite(models.Model):
    _name="dara_mallas.prerequisite"
    _order="seq" 

    
    prerequisite_subject_id=fields.Many2one("dara_mallas.subject")
    prerequisite_subject_code=fields.Char("Sigla",related="prerequisite_subject_id.code")
    condition=fields.Char("Condiciones")
    conector=fields.Selection([('Y','Y'),('O','O')],"Conector")
    or_conector=fields.Boolean("O")
    lparen=fields.Char("(")
    test_code=fields.Char("Codigo Examen")
    test_score=fields.Float("Puntaje Examen")
    grade_id=fields.Many2one("dara_mallas.grade")
    score_id=fields.Many2one('dara_mallas.rule_score', string="Calificacion")
    rparen=fields.Char(")")
    seq = fields.Integer("Seq")
    prerequsite_type=fields.Selection([('malla','Malla'),('homologacion','Homologacion')],"Tipo",default='malla')

    prerequisite_line_id=fields.Many2one("dara_mallas.prerequisite_line")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def name_get(self):
        result = []
        for rec in self:
            if rec.prerequisite_subject_id:
                result.append((rec.id,'%s - %s' % (str(rec.prerequisite_subject_id.code),str(rec.prerequisite_subject_id.name))))
            elif rec.test_code:
                result.append((rec.id,'%s' % (str(rec.test_code))))
            else:
                pass
        return result

    