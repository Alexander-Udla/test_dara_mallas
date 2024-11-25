# -*- coding: utf-8 -*-


import os
import sys
import pandas as pd
#import re



CONNECTORS = []
try:
    import psycopg2
    CONNECTORS.append(('postgres', 'POSTGRES'))
except:
    print('PSYCOPG2 libraries not available. Please install.')

try:
    import cx_Oracle
    CONNECTORS.append(('cx_Oracle', 'Oracle'))
except:
    print('CX_ORACLE libraries not available. Please install.')
class BaseExternalDbsource:
    host=''
    port=0
    password=''
    service_name=''
    user=''
    
    def __init__(self, source=None,service_name=None):

                        
        #self.name = ""
        self.source=source
        self.use_sid=False
        self.connector = 'postgresql'
        
        if self.source=='devl':
            self.host='sntsora02.udla-ec.int'
            self.port=1521
            self.user='INT_MALLAS'
            self.service_name = 'DEVL'
            self.password = 'SJA3Da/T*M}Z\j['
            self.connector = "cx_Oracle"
        elif self.source=='test':
            self.host='sntsora02.udla-ec.int'
            self.port=1521
            self.user='INT_MALLAS'
            self.service_name = 'TEST'
            self.password = 'SJA3Da/T*M}Z\j['
            self.connector = "cx_Oracle"        
        elif self.source=='migr':
            self.host='sntsora02.udla-ec.int'
            self.port=1521
            self.user='INT_MALLAS'
            self.service_name = 'MIGR'
            self.password = 'SJA3Da/T*M}Z\j['
            self.connector = "cx_Oracle"
        elif self.source=='prod':
            self.host='snora06.udla-ec.int'
            self.port=1521
            self.user='INT_MALLAS'
            self.service_name = 'PRODSTBY'
            self.password = '8jAbdj4TWRX8@3q*'
            self.connector = "cx_Oracle"
        elif self.source=='mallas_prod':
            self.host='192.168.5.217'
            self.port="5432"
            self.password="Swealhack99"
            self.user='wcabascango'
            self.service_name='udla_mallas'
            self.connector='postgresql'
        elif self.source=='mallas_13':
            self.host='10.190.0.168'
            self.port="5432"
            self.password="Cia2@22*"
            self.user='postgres'
            self.service_name='dara_mallas'
            self.connector='postgresql'
        elif self.source=='mallas_13_dev':
            self.host='localhost'
            self.port="5432"
            self.password="jde.2020"
            self.user='postgres'
            self.service_name='dara_mallas_actual'
            self.connector='postgresql'
        elif self.source=='reports_prod':
            self.host='192.168.4.75'
            self.port="5432"
            self.password="Fabian7598Y3s"
            self.user='fbaez'
            self.service_name=service_name  #dbname 
            self.connector='postgresql'
        elif self.source=='postgres_dev':
            self.host='localhost'
            self.port="5432"
            self.password="Fabian7598Y3s"
            self.user='fbaez'
            self.service_name=service_name #dbname 
            self.connector='postgresql'
        
    
    
    def conn_open(self):
        """The connection is open here."""

        # Try to connect
        if self.connector == 'cx_Oracle':
            os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'
            
            if self.use_sid:
                dsnStr = cx_Oracle.makedsn(self.host, self.port, self.sid)
                conn = cx_Oracle.connect(user=self.user,password=self.password,dsn=dsnStr)
            else:
                #----- print(self.host+' '+str(self.port)+' '+self.service_name)
                dsnStr = cx_Oracle.makedsn(host=self.host, port=self.port, service_name=self.service_name)
                conn = cx_Oracle.connect(user=self.user,password=self.password,dsn=dsnStr)
       
        elif self.connector=='postgresql':
            conn = psycopg2.connect(user = self.user,
                                  password = self.password,
                                  host = self.host,
                                  port = self.port,
                                  database = self.service_name)    
        
        return conn
    def execute_insert(self, sqlquery, sqlparams=None, metadata=False, context=None):
        conn = self.conn_open()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sqlquery, sqlparams)
        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()        
    def execute(self, sqlquery, sqlparams=None, metadata=False, context=None):
        """Executes SQL and returns a list of rows.

            "sqlparams" can be a dict of values, that can be referenced in
            the SQL statement using "%(key)s" or, in the case of Oracle,
            ":key".
            Example:
                sqlquery = "select * from mytable where city = %(city)s and
                            date > %(dt)s"
                params   = {'city': 'Lisbon',
                            'dt': datetime.datetime(2000, 12, 31)}

            If metadata=True, it will instead return a dict containing the
            rows list and the columns list, in the format:
                { 'cols': [ 'col_a', 'col_b', ...]
                , 'rows': [ (a0, b0, ...), (a1, b1, ...), ...] }
        """
        # data = self.browse(cr, uid, ids)
        rows, cols = list(), list()
        
        
        conn = self.conn_open()
        if self.connector in ["sqlite", "mysql", "mssql"]:
                # using sqlalchemy
            cur = conn.execute(sqlquery, sqlparams)
            if metadata:
                cols = cur.keys()
            rows = [r for r in cur]
        else:
            # using other db connectors
            cur = conn.cursor()
            cur.execute(sqlquery, sqlparams)
            if metadata:
                cols = [d[0] for d in cur.description]
            r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        conn.close()
        if metadata:
            return{'cols': cols, 'rows': r}
        else:
            return (r[0] if r else None) if False else r

   
    def connection_test(self):
        """Test of connection."""
               
        for obj in self:
            conn = False
            try:
                conn = self.conn_open()
            except Exception as e:
                sys.stdout.write("Error en la conexión de la base de datos")
            finally:
                try:
                    if conn:
                        conn.close()
                except Exception:
                    # ignored, just a consequence of the previous exception
                    pass
        # TODO: if OK a (wizard) message box should be displayed
        
    def get_dataframe_from_postgres(self,sqlquery,sqlparams):
        conn=self.conn_open()
        df_result = pd.read_sql_query(sql=sqlquery, con=conn, params=sqlparams)
        df_result.columns = map(str.lower, df_result.columns)
        conn.close()
        return df_result
        
    #conexion con base de datos en formato json
    def query(self,sql='',option='',parq=[],one=False,dataframe=False,insert=False):
        if option == 'dara_mallas_dev':
            conexion = psycopg2.connect("dbname=mallas user=alex password=root123")
        if option == 'udla_mallas_dev':
            conexion = psycopg2.connect("dbname=udla_mallas user=welintong password=jde.2020")
        if option == 'silabos_dev':
            conexion = psycopg2.connect("dbname=silabos_dev user=welintong password=jde.2020")
        if option == 'dara_mallas':
            conexion = psycopg2.connect("host=10.190.0.168 dbname=dara_mallas user=postgres password=Cia2@22*")
        if option == 'udla_mallas':
            conexion = psycopg2.connect("host=192.168.5.217 dbname=udla_mallas user=wcabascango password=Swealhack99")
        if option == 'banner':
            dsnStr = cx_Oracle.makedsn(host="ocora02.udla-ec.int", port= "1521", service_name="DBPROD_BA.db.bannerredprod.oraclevcn.com")
            conexion = cx_Oracle.connect( user='INT_MALLAS', password='8jAbdj4TWRX8@3q*', dsn=dsnStr)
        if option == 'banner_test':
            dsnStr = cx_Oracle.makedsn("10.1.2.108", "1521", "TEST")
            conexion = cx_Oracle.connect( user='INT_MALLAS', password='123456', dsn=dsnStr)
        if option == 'banner_devl':
            dsnStr = cx_Oracle.makedsn("sntsora02.udla-ec.int", "1521", "DEVL")
            conexion = cx_Oracle.connect( user='INT_MALLAS', password='SJA3Da/T*M}Z\j[', dsn=dsnStr)
        if option == 'banner_migr':
            dsnStr = cx_Oracle.makedsn("sntsora02.udla-ec.int", "1521", "MIGR")
            conexion = cx_Oracle.connect( user='MIGRACION', password='u_pick_it', dsn=dsnStr)
        if dataframe:
            df_result = pd.read_sql_query(sql=sql, con=conexion, params=parq)
            df_result.columns = map(str.lower, df_result.columns)
            conexion.close()
            return df_result
        else:
            if insert:
                try:
                    cur = conexion.cursor()
                    #cur.execute (sql,parq)
                    cur.execute (sql)
                    conexion.commit()
                    count = cur.rowcount
                    res = str(count)+ " Record inserted successfully into table"
                    if conexion:
                        cur.close()
                        conexion.close()
                        print("PostgreSQL connection is closed")
                    
                    return res
                except Exception as e:
                    print(e)

            else:
                cur = conexion.cursor()
                #cur.execute (sql,parq)
                cur.execute (sql)
                res = [dict((cur.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cur.fetchall()]
                return (res[0] if res else None) if one else res