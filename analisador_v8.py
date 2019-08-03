# coding=latin-1
import csv
from datetime import date
import numpy as np
import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import math
import os
import pandas as pd

#hj = date.today()
#dataFormatada = hj.strftime('%d/%m/%Y')



#variaveis
ArqDadosPag = open("pagamentos.csv","r")
DataPag = "01/01/2020"
Valor = []
Plano = []
ClienteID = []
MesesPagos = []
data = {}
#listas
meses =['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
retiraAspas = '"'
retiraCifrao= 'R$ '
retiravirgula= ','
tmp = 'texto'
#listas
dia = []
mes = []
ano = []
#reader = csv.reader(ArquivoDadosPagamentos, delimiter=',', quoting=csv.QUOTE_NONE)
#Ler arquivo csv
LerCsv = csv.reader(ArqDadosPag)
#adicionar o cabeçalho no arquivo
csvRow=[] #memoria do meu novo conjunto de dados
for row in LerCsv:
# print LerCsv.line_num
 if LerCsv.line_num == 1:
  continue
 ClienteID.append(row[0])
#Limpando data de pagamento
# print row[1]
 diaTmp,mesTmp,anoTmp = row[1].split('/')
 dia.append(int(diaTmp))
 mes.append(int(mesTmp))
 ano.append(int(anoTmp))
 msano = []
 for i in range(0,len(row[2])):
# Limpando dados/formato pagamento
  row[2] = row[2].replace(retiraAspas,"")
  row[2] = row[2].replace(retiraCifrao,"")
  row[2] = row[2].replace(",",".")
 Valor.append(float(row[2]))
# Limpando plano
# print row[3]
 PlanoNomeTmp, MesesPagosTmp = row[3].split('/')
 Plano.append(str(PlanoNomeTmp))
 MesesPagos.append(int(MesesPagosTmp))
IDinicio= int(min(ClienteID))
IDFim=int(max(ClienteID))

df1 = pd.DataFrame({'idx': ClienteID,'Dia': dia, 'Mes':mes, 'Ano':ano, 'Plano':Plano, 'mesespagos':MesesPagos,'R$':Valor})
tmp = 0
contador = 0
mmini = []
#menor data
mesinicio = 13
AnoInicio = int(min(ano))
eh_inicio =  df1['Ano']== AnoInicio
df1_inicio = df1[eh_inicio]
#menor mes
mtmp = df1_inicio['Mes']
MesInicio = min(mtmp)
#print MesInicio, anoinicio
AnoFim = 2019
MesFim = 8
#print MesFim, AnoFim
matrix = [[]]
COLUNAS = []
COLUNAS.append('IDCL')
#criando planilha
for kano in range(AnoInicio,AnoInicio+1):
 for kmes in range(MesInicio,13):
  texton = (str(meses[kmes-1])+'/'+str(kano))
  COLUNAS.append(texton)
#  print texton 
for kano in range(AnoInicio+1,AnoFim):
 for kmes in range(1,13):
  texton = (str(meses[kmes-1])+'/'+str(kano))
  COLUNAS.append(texton)
#  print texton
for kano in range(AnoFim,AnoFim+1):
 for kmes in range(1,MesFim+1):
  texton = (str(meses[kmes-1])+'/'+str(kano))
  COLUNAS.append(texton)
#  print texton
#print COLUNAS
#Metricas
MRR = pd.DataFrame(columns=COLUNAS)
NewMRR = pd.DataFrame(columns=COLUNAS)
dfnulo = pd.DataFrame(columns=COLUNAS)
ExpasionMRR = pd.DataFrame(columns=COLUNAS)
ContractionMRR = pd.DataFrame(columns=COLUNAS)
CancelledMRR = pd.DataFrame(columns=COLUNAS)
ResurrectedMRR = pd.DataFrame(columns=COLUNAS)
#MRR.set_index('IDX', inplace=True)
#print MRR
fim = len(ClienteID)
#print df1.loc[0:3] 
#df2 = df1.set_index('idx')
#print df2.head()
#ver linha a linha do data#
qano_fim = 0
qmes_in = 0
qmes_fim = 0
qano_in = 0
def listaFiltro(datafram, valores):
 return datafram.loc[datafram['idx'].isin(valores)]
valorReal = 10000.20
#fixme para ir até 5000
for kk in range(0,5000):
# print kk
 CancelledMRR.loc[kk,'IDCL'] = kk
 ExpasionMRR.loc[kk,'IDCL'] = kk
 ContractionMRR.loc[kk,'IDCL'] = kk
 ResurrectedMRR.loc[kk,'IDCL'] = kk
 MRR.loc[kk,'IDCL'] = kk
 NewMRR.loc[kk,'IDCL'] = kk
 tmpk = str(kk)
 lista = [tmpk]
 df2 = pd.DataFrame(listaFiltro(df1, lista))
# df2.to_csv('data/ID%i.csv' % kk)
 lista_rows =  df2.index
# print df2
 qano_fim = 0
 qmes_in = 0
 qmes_fim = 0
 qano_in = 0
 ncols=[]
 aMRR = 2200
 mMRR = 12
 for k in lista_rows:
  numMes = df2.loc[k,'mesespagos']
  knumMes= int(numMes)
  valorReal = (float(df2.loc[k,'R$'])/float(numMes))
#quando foi pago
  qdia_in = df2.loc[k,'Dia']
  qmes_in = df2.loc[k,'Mes']
  qano_in = df2.loc[k,'Ano']
  qmes_fim = (qmes_in + knumMes)
##Achar primeiro pagamento do Cliente 
  if (qmes_fim > 12):
   somaano = (qmes_fim /12)
   resto = (qmes_fim % 12)
   qmes_fim = resto
#   print resto,somaano
   qano_fim = (qano_in + somaano)
  else:
   qano_fim = qano_in
  while ((qano_in <= qano_fim)and(qmes_in <= qmes_fim)):
#   print k,qmes_in,qano_in
#   print df2.loc[[k],['Dia','Mes','Ano']], qano_fim, qmes_fim, qano_in, qmes_in  
   jv = qmes_in
   texton = (str(meses[jv-1])+'/'+str(qano_in))
   if ((qmes_in < mMRR)and(qano_in < aMRR)):
	mMRR = qmes_in
	aMRR = qano_in
	vnewMRR = valorReal
   MRR.loc[kk,texton] = valorReal
   qmes_in = (qmes_in+1)
#    print kk, k, texton
   if (qmes_in > 12):
    qmes_in = 1
    qano_in = (qano_in + 1)
###Fazendo a MRR, o de cima###  
##Abaixo Fazendo a NewMRR###
 texton = (str(meses[mMRR-1])+'/'+str(aMRR))
 NewMRR.loc[kk,texton] = vnewMRR
 kont = -1
 for kkk in COLUNAS:
  kont = kont +1	 
  if (kkk == 'IDCL'):
   continue
  else:
   xis = MRR.loc[kk, kkk]
   xis_ant = MRR.loc[kk, COLUNAS[kont-1]]
   nxis = xis - xis_ant
#############################################
#Metricas
   if (math.isnan(xis) is True):
    if (math.isnan(xis_ant) is True):
     continue
    else:
     CancelledMRR.loc[kk,kkk] = xis_ant
   else:
    if (nxis > 0.0):
     if (math.isnan(xis_ant) is True):
      ResurrectedMRR.loc[kk,kkk] = nxis
     else:
      ExpasionMRR.loc[kk,kkk] = nxis
    elif (nxis < 0.0):
	 ContractionMRR.loc[kk,kkk] = nxis*(-1.0)
    else:
     continue
#vou usar
#df[(df["Seminário"] > 8.0) & (df["Prova"] > 3)]
MRR.to_csv('MRR.csv')
NewMRR.to_csv('NewMRR.csv')
ExpasionMRR.to_csv('ExpasionMRR.csv')
ContractionMRR.to_csv('ContractionMRR.csv')
CancelledMRR.to_csv('CancelledMRR.csv')
ResurrectedMRR.to_csv('ResurrectedMRR.csv')
print MRR.describe
