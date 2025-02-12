
import pandas as pd
from validador.prerequisitos import metodos
from datetime import date
fecha_actual = date.today()

class Validar_Prerequisitos:
    def __init__(self, period: str, base_datos: str) -> None:
        self.metodos = metodos.Validator(base_datos)
        self.df_results=pd.DataFrame(columns=['period','subject_code','status','banner','odoo'])
        #self.periodo = '202310'
        self.fecha = fecha_actual.strftime("%d%m%Y")
        self.period = period
        pass

    def read_xls(self,name):
        file = pd.read_excel('./validador/prerequisitos/source/'+name)
        return file

    def load_or_prerequisitos(self):
        #1.- ejecutar en postgres el archivo insert-pre-hom.txt
        #2.- ejecutar en postgres el archivo delete.txt
        #3.- volver a ejecutar el script
        #4.- ejecutar en postgres el archivo insert.txt

        res = self.read_xls('or_prerequisitesHOM_cargaOdoo.xlsx')
        #filtrar por tipo de homologacion
        #res = res[res['prerequsite_type']=='homologacion']
        res.fillna('',inplace=True)
        sin = []
        #guardar insert y delete en archivo txt
        f = open('./validador/prerequisitos/source/insert-%s.txt'%(self.fecha),'w')
        delete = open('./validador/prerequisitos/source/delete-%s.txt'%(self.fecha),'w')
        #prerequisitos de homologaciones que cambiaron
        preHom = open('./validador/prerequisitos/source/insert-pre-hom-%s.txt'%(self.fecha),'w')
        for i,item_xls in res.iterrows():
            #id_prerequisite = self.metodos.get_id_prerequisito_odoo_head(self.periodo,item_xls['subject_code'])
            id_prerequisite = self.metodos.get_id_prerequisito_odoo_head(item_xls['periodo'],item_xls['subject_code'])
            if id_prerequisite:
                #eliminar detalle de los prerequisitos
                res_delete = self.metodos.delete_detail(id_prerequisite[0]['id'])
                text = """
                insert into dara_mallas_prerequisite(
                condition,
                conector,
                lparen,
                test_code,
                test_score,
                rparen,
                seq,
                prerequsite_type,
                grade_id,
                score_id,
                prerequisite_subject_id,
                prerequisite_line_id) values('%s','%s','%s','%s',%s,'%s',%s,'%s',
                (select g.id from dara_mallas_grade g where g.description = '%s'),
                (select s.id from dara_mallas_rule_score s where s.name = '%s'),
                (select sa.id from dara_mallas_subject sa where sa.code = '%s'),
                '%s'
                );\n
                """%(
                '1',
                item_xls['conector'],
                item_xls['lparen'],
                item_xls['test_code'],
                item_xls['test_score'] if item_xls['test_score'] else 'null' ,
                item_xls['rparen'],
                item_xls['seq'],
                item_xls['prerequsite_type'],
                item_xls['grade'],
                str(item_xls['score']),
                item_xls['prerequisite_subject_code'],
                id_prerequisite[0]['id']
                )
                f.write(text)
                delete.write(res_delete)

            if not id_prerequisite and item_xls['subject_code'] not in sin:
                sin.append(item_xls['subject_code'])
                #escribe en archivo preHom
                cadena = self.insert_or_prerequisitos_homologation(item_xls['periodo'],item_xls['subject_code'])
                preHom.write(cadena)
        f.close()
        delete.close()
        preHom.close()
        df = pd.DataFrame(sin)
        df.to_excel('./validador/prerequisitos/source/siglas-%s.xlsx'%(self.fecha))
    
    
    def insert_or_prerequisitos_homologation(self,periodo,subject_code):
        sql = """
        insert into dara_mallas_prerequisite_line (period_id,subject_id) values
        (
        (select pe.id from dara_mallas_period pe where pe.name = '%s'),
        (select s.id from dara_mallas_subject s where s.code = '%s')
        );\n
        """%(periodo,subject_code)
        return sql
    
    def load_or_prerequisitos_homologation(self):
        res = self.read_xls('siglas-%s.xlsx'%(self.fecha))
        res.fillna('',inplace=True)
        res = list(res[0].values)
        siglas = self.read_xls('prerequisitos_202320_202410_entregaFinal.xlsx')
        SubInh = open('./validador/prerequisitos/source/update-subject-inherit-%s.txt'%(self.fecha),'w')
        for i,item_xls in siglas.iterrows():
            if item_xls['subject_code'] in res:
                id_prerequisite = self.metodos.get_id_prerequisito_odoo_head(item_xls['periodo'],item_xls['subject_code'])
                sql = """
                    update dara_mallas_subject_inherit set prerequisite_line_id = %s
                    where subject_id = (
                    select s.id from dara_mallas_subject s where s.code = '%s'
                    ) ;\n
                """%(id_prerequisite[0]['id'],item_xls['subject_code'])
                SubInh.write(sql)
        SubInh.close()



    def compare_to(self,subject_code,period):
        try:
            #prerequisitos de banner en una linea
            res_banner = self.metodos.get_prerequisitos_banner_detail(subject_code=subject_code,period=period)
            banner_prereq=[]
            for index, row in res_banner.iterrows():
                
                if row['conector']:
                    banner_prereq.append(row['conector'])
                if row['lparen']:
                    banner_prereq.append(row['lparen'])
                if row['test_code']:
                    banner_prereq.append(row['test_code'])
                if row['test_score']:
                    banner_prereq.append(int(row['test_score']))
                    
                if row['prerequisite_subject_code']:
                    banner_prereq.append(row['prerequisite_subject_code'])
                if row['rule_score']:
                    banner_prereq.append(row['rule_score'])
                if row['rparen']:
                    banner_prereq.append(row['rparen'])
            
            #prerequisitos de odoo en una linea
            res_odoo = self.metodos.get_prerequisito_odoo_detail(subject_code=subject_code,period=period)
            res_odoo.fillna('',inplace=True)
            odoo_prereq=[]
            for index, row in res_odoo.iterrows():
                if row['conector']:
                    odoo_prereq.append(row['conector'])
                if row['lparen']:
                    odoo_prereq.append(row['lparen'])
                if row['test_code']:
                    odoo_prereq.append(row['test_code'])
                if row['test_score']:
                    odoo_prereq.append(int(row['test_score']))
                if row['prerequisite_subject_code']:
                    odoo_prereq.append(row['prerequisite_subject_code'])
                if row['rule_score']:
                    odoo_prereq.append(row['rule_score'])
                if row['rparen']:
                    odoo_prereq.append(row['rparen'])

            banner_preq= ' '.join(str(x) for x in banner_prereq)
            odoo_preq = ' '.join (str(x) for x in odoo_prereq)
            if banner_prereq != odoo_prereq:
                self.df_results=self.df_results.append({
                                            'period':period
                                            ,'subject_code':subject_code
                                            ,'status':'Fail'
                                            ,'banner':banner_preq
                                            ,'odoo':odoo_preq},ignore_index=True)
            else:
                self.df_results=self.df_results.append({
                                            'period':period
                                            ,'subject_code':subject_code
                                            ,'status':'OK'
                                            ,'banner':''
                                            ,'odoo':''},ignore_index=True)
        except Exception as e:
            self.df_results=self.df_results.append({
                                            'period':period
                                            ,'subject_code':subject_code
                                            ,'status':'Fail'
                                            ,'banner':e
                                            ,'odoo':''},ignore_index=True)
    
    def execute(self):
        #parametros
        subject_codes = []
        period = self.period
        #period = '202320'
        #df = self.read_xls('or_prerequisites202420_cargaOdoo.xlsx')
        df = self.metodos.get_subject_prerequisito_odoo_per_period(period=period)
        for i, item_subject in df.iterrows():
            print(f"Procesando fila {i + 1} de {len(df)}")
            if item_subject['subject_code'] not in subject_codes:
                self.compare_to(subject_code=item_subject['subject_code'],period=item_subject['period'])
                subject_codes.append(item_subject['subject_code'])
        self.df_results.to_csv('/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/prerequisitos/source/validacion_scapreq-%s-%s.csv'%(self.fecha,period))

        