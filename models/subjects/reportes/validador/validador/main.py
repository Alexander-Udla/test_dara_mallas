import pandas as pd
from validador.homologaciones import metodos
from datetime import date
# Obtener la fecha actual
fecha_actual = date.today()
class Validador_Homologaciones:
    def __init__(self) -> None:
        self.data = []
        #self.period = "202220"
        pass

    def read_csv(self):
        file = pd.read_excel('./validador/homologaciones/source/data.xlsx')
        return file

    def compare_to(self,homologaciones_odoo='',homologaciones_banner=''):
        data_compare = []
        for item_odoo in homologaciones_odoo:
            errores = ""
            exists = False
            conector = False
            for item_banner in homologaciones_banner:
                if item_odoo['PERIODO'] == item_banner['PERIODO'] and item_odoo['AREA'] == item_banner['AREA'] and item_odoo['REGLA'] == item_banner['REGLA']:
                    if item_odoo['SIGLA'] == item_banner['SIGLA'] and not item_odoo['PRUEBA']:
                        exists = True
                        if item_odoo['CONECTOR'] == item_banner['CONECTOR']:
                            conector = True
                            if item_odoo['PRUEBA'] == item_banner['PRUEBA']:
                                errores += ""
                            else:
                                errores += "Error en prueba %s , %s"%(item_odoo['PRUEBA'],item_banner['PRUEBA'])

                            if item_odoo['TEST_PUNTAJE_MINIMO'] == item_banner['TEST_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MINIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MINIMO'],item_banner['TEST_PUNTAJE_MINIMO'])
                            
                            if item_odoo['TEST_PUNTAJE_MAXIMO'] == item_banner['TEST_PUNTAJE_MAXIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MAXIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MAXIMO'],item_banner['TEST_PUNTAJE_MAXIMO'])

                            if item_odoo['REGLA_PUNTAJE_MINIMO'] == item_banner['REGLA_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_PUNTAJE_MINIMO %s , %s"%(item_odoo['REGLA_PUNTAJE_MINIMO'],item_banner['REGLA_PUNTAJE_MINIMO'])
                            
                            if item_odoo['REGLA_ATRIBUTO'] == item_banner['REGLA_ATRIBUTO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_ATRIBUTO %s , %s"%(item_odoo['REGLA_ATRIBUTO'],item_banner['REGLA_ATRIBUTO'])
                        else:
                            next
                    if item_odoo['PRUEBA']:
                        if item_odoo['PRUEBA'] == item_banner['PRUEBA']:
                            exists = True
                            if item_odoo['CONECTOR'] == item_banner['CONECTOR']:
                                conector = True
                                errores += ""
                            else:
                                errores += "Error en conector %s , %s"%(item_odoo['CONECTOR'],item_banner['CONECTOR'])
                            
                            if item_odoo['PRUEBA'] == item_banner['PRUEBA']:
                                errores += ""
                            else:
                                errores += "Error en prueba %s , %s"%(item_odoo['PRUEBA'],item_banner['PRUEBA'])

                            if item_odoo['PRUEBA'][:3]=='ENG':
                                min = item_odoo['TEST_PUNTAJE_MINIMO']
                                maximo = item_odoo['TEST_PUNTAJE_MAXIMO']
                            else:
                                if not item_odoo['PRUEBA'][:3] in ['DAL','DEL','FRA']:
                                    min = '0'+str(item_odoo['TEST_PUNTAJE_MINIMO']) if len(str(item_odoo['TEST_PUNTAJE_MINIMO']))==1 else item_odoo['TEST_PUNTAJE_MINIMO']
                                    maximo = '0'+str(item_odoo['TEST_PUNTAJE_MAXIMO']) if len(str(item_odoo['TEST_PUNTAJE_MAXIMO']))==1 else item_odoo['TEST_PUNTAJE_MAXIMO']
                                else:
                                    min = str(item_odoo['TEST_PUNTAJE_MINIMO'])
                                    maximo = str(item_odoo['TEST_PUNTAJE_MAXIMO'])
                            if str(min) == item_banner['TEST_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MINIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MINIMO'],item_banner['TEST_PUNTAJE_MINIMO'])
                            
                            
                            if str(maximo) == item_banner['TEST_PUNTAJE_MAXIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MAXIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MAXIMO'],item_banner['TEST_PUNTAJE_MAXIMO'])

                            if item_odoo['REGLA_PUNTAJE_MINIMO'] == item_banner['REGLA_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_PUNTAJE_MINIMO %s , %s"%(item_odoo['REGLA_PUNTAJE_MINIMO'],item_banner['REGLA_PUNTAJE_MINIMO'])
                            
                            if item_odoo['REGLA_ATRIBUTO'] == item_banner['REGLA_ATRIBUTO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_ATRIBUTO %s , %s"%(item_odoo['REGLA_ATRIBUTO'],item_banner['REGLA_ATRIBUTO'])

                    if item_odoo['REGLA_ATRIBUTO'] and not exists:
                        if item_odoo['REGLA_ATRIBUTO'] == item_banner['REGLA_ATRIBUTO']:
                            exists = True
                            if item_odoo['CONECTOR'] == item_banner['CONECTOR']:
                                conector = True
                                errores += ""
                            else:
                                errores += "Error en conector %s , %s"%(item_odoo['CONECTOR'],item_banner['CONECTOR'])
                            
                            if item_odoo['PRUEBA'] == item_banner['PRUEBA']:
                                errores += ""
                            else:
                                errores += "Error en prueba %s , %s"%(item_odoo['PRUEBA'],item_banner['PRUEBA'])

                            min = '0'+str(item_odoo['TEST_PUNTAJE_MINIMO']) if len(str(item_odoo['TEST_PUNTAJE_MINIMO']))==1 else item_odoo['TEST_PUNTAJE_MINIMO']
                            if min=='4':
                                print("h")
                            if min == item_banner['TEST_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MINIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MINIMO'],item_banner['TEST_PUNTAJE_MINIMO'])
                            
                            maximo = '0'+str(item_odoo['TEST_PUNTAJE_MAXIMO']) if len(str(item_odoo['TEST_PUNTAJE_MAXIMO']))==1 else item_odoo['TEST_PUNTAJE_MAXIMO']
                            if str(maximo) == item_banner['TEST_PUNTAJE_MAXIMO']:
                                errores += ""
                            else:
                                errores += "Error en TEST_PUNTAJE_MAXIMO %s , %s"%(item_odoo['TEST_PUNTAJE_MAXIMO'],item_banner['TEST_PUNTAJE_MAXIMO'])

                            if item_odoo['REGLA_PUNTAJE_MINIMO'] == item_banner['REGLA_PUNTAJE_MINIMO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_PUNTAJE_MINIMO %s , %s"%(item_odoo['REGLA_PUNTAJE_MINIMO'],item_banner['REGLA_PUNTAJE_MINIMO'])
                            
                            if item_odoo['REGLA_ATRIBUTO'] == item_banner['REGLA_ATRIBUTO']:
                                errores += ""
                            else:
                                errores += "Error en REGLA_ATRIBUTO %s , %s"%(item_odoo['REGLA_ATRIBUTO'],item_banner['REGLA_ATRIBUTO'])
            if not exists:
                errores += "Sigla no existe en Banner %s "%(item_odoo['SIGLA'])
            if not conector and exists:
                errores += "Sigla existe en Banner %s pero el conector es incorrecto %s "%(item_odoo['SIGLA'] if item_odoo['SIGLA'] else item_odoo['PRUEBA'],item_odoo['CONECTOR'])
            data_compare.append(
                {
                    'PERIODO':item_odoo['PERIODO'],
                    'AREA':item_odoo['AREA'],
                    'REGLA': item_odoo['REGLA'],
                    'CONECTOR':item_odoo['CONECTOR'],
                    'SIGLA':item_odoo['SIGLA'],
                    'PRUEBA':item_odoo['PRUEBA'],
                    'TEST_PUNTAJE_MINIMO':item_odoo['TEST_PUNTAJE_MINIMO'],
                    'TEST_PUNTAJE_MAXIMO':item_odoo['TEST_PUNTAJE_MAXIMO'],
                    'REGLA_PUNTAJE_MINIMO':item_odoo['REGLA_PUNTAJE_MINIMO'],
                    'REGLA_ATRIBUTO':item_odoo['REGLA_ATRIBUTO'],
                    'ESTADO': errores if errores else 'OK'
                }
            )        


        #===================================================
        #  VERIFICA SI EN BANNER EXISTE UNA SIGLA ADICIONAL
        #==================================================
        odoo = [item['SIGLA']+str(item['CONECTOR']) if item['SIGLA'] else item['PRUEBA'] for item in homologaciones_odoo]
        filtrada = list(filter(lambda x:(x['SIGLA']+str(x['CONECTOR']) if x['SIGLA'] else x['PRUEBA']) not in odoo, homologaciones_banner))
        if filtrada:
            for item_banner in filtrada:
                data_compare.append(
                    {
                        'PERIODO':item_banner['PERIODO'],
                        'AREA':item_banner['AREA'],
                        'REGLA': item_banner['REGLA'],
                        'CONECTOR':item_banner['CONECTOR'],
                        'SIGLA':item_banner['SIGLA'],
                        'PRUEBA':item_banner['PRUEBA'],
                        'TEST_PUNTAJE_MINIMO':item_banner['TEST_PUNTAJE_MINIMO'],
                        'TEST_PUNTAJE_MAXIMO':item_banner['TEST_PUNTAJE_MAXIMO'],
                        'REGLA_PUNTAJE_MINIMO':item_banner['REGLA_PUNTAJE_MINIMO'],
                        'REGLA_ATRIBUTO':item_banner['REGLA_ATRIBUTO'],
                        'ESTADO': 'En Banner %s no se encontro en odoo'%(item_banner['SIGLA'])
                    }
                )
        self.data.extend(data_compare)


    def execute(self):
        validador = metodos.Validator()
        period = '202520'
        #res = self.read_csv()
        res = validador.get_homologations_for_period(period=period)
        subjects_odoo_empty = []
        subjects_banner_empty = []
        #for i,item in res.iterrows():
        for index, item in zip(range(0,len(res)),res):
            print("%s de %s"%(str(index),len(res)))
            homologaciones_odoo = validador.get_homologations_for_subject_period_area(
                subject_code=item['REGLA'],
                period=item['PERIODO'],
                area=item['AREA'],
                period_val=period
                )
            homologaciones_banner = validador.get_homologations_for_subject_period_area_banner(
                subject_code=item['REGLA'],
                #period=item['PERIODO'],
                period=period,
                area=item['AREA']
            )
            if not homologaciones_odoo:
                subjects_odoo_empty.append([item['REGLA'],
                item['PERIODO'],
                item['AREA']])
            if not homologaciones_banner:
                subjects_banner_empty.append([item['REGLA'],
                item['PERIODO'],
                item['AREA']])
                self.data.append(
                    {
                        'PERIODO':item['PERIODO'],
                        'AREA':item['AREA'],
                        'REGLA': item['REGLA'],
                        'CONECTOR':'',
                        'SIGLA':'',
                        'PRUEBA':'',
                        'TEST_PUNTAJE_MINIMO':'',
                        'TEST_PUNTAJE_MAXIMO':'',
                        'REGLA_PUNTAJE_MINIMO':'',
                        'REGLA_ATRIBUTO':'',
                        'ESTADO': 'En Banner %s no se encontro'%(item['REGLA'])
                    }
                )
            
            if homologaciones_banner and homologaciones_odoo:
                self.compare_to(homologaciones_odoo=homologaciones_odoo,homologaciones_banner=homologaciones_banner)
            else:
                pass
        resultado = pd.DataFrame(self.data)
        fecha = fecha_actual.strftime("%d%m%Y")
        resultado.to_csv('/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/validador/homologaciones/source/homologaciones-%s-%s.csv'%(fecha,period))