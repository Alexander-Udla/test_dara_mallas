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
    
    def __init__(self):
        pass
      
        
    #conexion con base de datos en formato json
    def query(self,sql='',option='',parq=[],one=False,dataframe=False,insert=False):
        if option == 'dara_mallas_dev':
            conexion = psycopg2.connect("dbname=dara_mallas_test user=welintong password=jde.2020")
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