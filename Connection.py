import cx_Oracle as co
import os
import pandas as pd

currentDir = os.getcwd()
print('Sync Issue Script Creation Running')


df1 = pd.read_csv('dbconfig.csv')
ConfigDict = df1.to_dict()

os.chdir('/instantclient_18_5')
dsn_tns = co.makedsn(ConfigDict['host'][0], ConfigDict['port'][0], service_name=ConfigDict['service'][0])
conn = co.connect(user=ConfigDict['username'][0], password=ConfigDict['password'][0], dsn=dsn_tns)
