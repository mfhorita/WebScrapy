import pyodbc
import re
import time
import urllib.request as req

import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Web Scraping
# ------------------------------------------------------------------------------------

bConexao = False
while not bConexao:
    try:
        page = req.urlopen("http://www.anbima.com.br/vna/vna.asp")
        bConexao = True
    except ConnectionError:
        time.sleep(60)
    except Exception as error:
        print(error)
        quit()

soup = BeautifulSoup(page, "html.parser")

NTNB = soup.find_all('div', id='listaNTN-B')
NTNC = soup.find_all('div', id='listaNTN-C')
LFT = soup.find_all('div', id='listaLFT')

regex = {'Data': {
            'NTN-B': re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', NTNB.__str__())[0],
            'NTN-C': re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', NTNC.__str__())[0],
            'LFT': re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', LFT.__str__())[0]},
         'Valor': {
            'NTN-B': re.findall(r'[0-9]{1}\.[0-9]{3}\,[0-9]{6}|[0-9]{2}\.[0-9]{3}\,[0-9]{6}', NTNB.__str__())[0],
            'NTN-C': re.findall(r'[0-9]{1}\.[0-9]{3}\,[0-9]{6}|[0-9]{2}\.[0-9]{3}\,[0-9]{6}', NTNC.__str__())[0],
            'LFT': re.findall(r'[0-9]{1}\.[0-9]{3}\,[0-9]{6}|[0-9]{2}\.[0-9]{3}\,[0-9]{6}', LFT.__str__())[0]}}

result = pd.DataFrame.from_dict(regex)
print(result)
print(type(result))

# with open(r'C:\Users\mfhor\Google Drive\Python\Scrapy\vna.txt', 'w') as f:
#     f.write(result.__str__())

# Conexão ao banco de dados Access e gravação
# ------------------------------------------------------------------------------------

# conn_str = (r'DSN=TestScrapy;DBQ=C:\Users\mfhor\Google Drive\Python\Scrapy\CenAtivos.mdb;')
conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb)};'
            r'DBQ=C:\Users\mfhor\Google Drive\Python\Scrapy\CenAtivos.mdb;')

conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

# Grava valor do LFT
data = datetime.strptime(result.iloc[0, 0], '%d/%m/%Y').date()
cursor.execute("SELECT * FROM [HistIndex] WHERE [DtBase] = #" + data.__str__() + "# AND [DsIndice] = 'LFT';")

if cursor.fetchone() is None:
    print('LFT ' + result.iloc[0, 1]) # Linha, Coluna: Valor LFT
    valor = re.findall(r'[0-9]{1}\.|[0-9]{2}\.', result.iloc[0, 1])[0][:-1] \
            + re.findall(r'[0-9]{3}', result.iloc[0, 1])[0] + '.' \
            + re.findall(r'[0-9]{6}', result.iloc[0, 1])[0]
    insert = "INSERT INTO [HistIndex] VALUES (#" + data.__str__() + "#, 'LFT', " + valor + ");"
    cursor.execute(insert)

# Grava valor do NTN-B
data = datetime.strptime(result.iloc[1, 0], '%d/%m/%Y').date()
cursor.execute("SELECT * FROM [HistIndex] WHERE [DtBase] = #" + data.__str__() + "# AND [DsIndice] = 'NTN-B';")

if cursor.fetchone() is None:
    print('NTN-B ' + result.iloc[1, 1]) # Linha, Coluna: Valor NTN-B
    valor = re.findall(r'[0-9]{1}\.|[0-9]{2}\.', result.iloc[1, 1])[0][:-1] \
            + re.findall(r'[0-9]{3}', result.iloc[1, 1])[0] + '.' \
            + re.findall(r'[0-9]{6}', result.iloc[1, 1])[0]
    insert = "INSERT INTO [HistIndex] VALUES (#" + data.__str__() + "#, 'NTN-B', " + valor + ");"
    cursor.execute(insert)

# Grava valor do NTN-C
data = datetime.strptime(result.iloc[2, 0], '%d/%m/%Y').date()
cursor.execute("SELECT * FROM [HistIndex] WHERE [DtBase] = #" + data.__str__() + "# AND [DsIndice] = 'NTN-C';")

if cursor.fetchone() is None:
    print('NTN-C ' + result.iloc[2, 1]) # Linha, Coluna: Valor NTN-C
    valor = re.findall(r'[0-9]{1}\.|[0-9]{2}\.', result.iloc[2, 1])[0][:-1] \
            + re.findall(r'[0-9]{3}', result.iloc[2, 1])[0] \
            + '.' + re.findall(r'[0-9]{6}', result.iloc[2, 1])[0]
    insert = "INSERT INTO [HistIndex] VALUES (#" + data.__str__() + "#, 'NTN-C', " + valor + ");"
    cursor.execute(insert)

cursor.close()
conn.close()
