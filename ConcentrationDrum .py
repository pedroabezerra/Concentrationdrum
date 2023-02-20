#!/usr/bin/env python
# coding: utf-8

# In[256]:


import os
import glob
import numpy as np
import pandas as pd


# In[257]:


NF = 50 #number of files
NP = 57300 #number of particles


# In[258]:


contador1 = list()
contador2 = list()
contador = list()
concentracao1 = list()
concentracao2 = list()
Tipo = np.zeros((NP,NF))
posicaoX = np.zeros((NP,NF))
posicaoY = np.zeros((NP,NF))


# In[259]:


#construção das repartições no tambor
nd_x = 5
nd_y = 5

max_x = 0.075
min_x = -0.075
max_y = 0.075
min_y = -0.075
esp_x = (max_x - min_x)/nd_x
esp_y = (max_y - min_y)/nd_y


# In[260]:


#leitura dos dados

home = os.path.expanduser("~")
path = f"E:/PIBIC/efeito da dimensao do tambor - densidade/70/dados_rot"
all_files = glob.glob(path + "/*.csv")
Dados = pd.concat((pd.read_csv(f) for f in all_files))
Dados_filter = Dados.filter(items=['type','Points:0','Points:1'])
display(Dados_filter)


# In[261]:


#construção do ponteiro para localização
cd1 = Dados_filter
cd1['Points:0'] = Dados_filter['Points:0'].div(esp_x).round(0)+3
cd1['Points:1'] = Dados_filter['Points:1'].div(esp_y).round(0)+3
posicao = -5+cd1['Points:0']+5*cd1['Points:1']
cd1 = cd1.assign(posicao = posicao.values)
print(cd1)


# In[262]:


#contagem de particulas repetidas em cada posição
count = cd1.groupby(['type', 'posicao']).size().reset_index(name='count')
count2 = pd.DataFrame(count)
dftype1 = count2[(count2.type == 1)]
dftype2 = count2[(count2.type == 2)]
dftype1.reset_index(inplace = True, drop = True)
dftype2.reset_index(inplace = True, drop = True)

#Dataframe de zeros para preenchimento
count3 = pd.DataFrame(0, columns=['type','posicao','count'],index=range(25))
count4 = pd.DataFrame(0, columns=['type','posicao','count'],index=range(25))
posicao1 = list(range(1, 26, 1))
posicao2 = list(range(1, 26, 1))
count3['posicao'] = posicao1
count4['posicao'] = posicao2

count3 = pd.concat([dftype1, count3], axis=0).sort_values(by='posicao', axis=0,ascending=True, kind='stable').drop_duplicates('posicao')
count4 = pd.concat([dftype2, count4], axis=0).sort_values(by='posicao', axis=0,ascending=True, kind='stable').drop_duplicates('posicao')

#display(count2)
#display(count3)
#display(count4)

#display(dftype1)
#display(dftype2)
#display(dftypetotal)


# In[263]:


#cálculo da concentração por tipo de partícula

total_count_df = pd.merge(count3, count4, on='posicao',how='left')
total_count = total_count_df['count_x'].add(total_count_df['count_y'], fill_value=0)
total_count_df['total_count']= total_count
total_count_df['concentracao_1']= total_count_df['count_x'] / total_count_df['total_count']
total_count_df['concentracao_2']= total_count_df['count_y'] / total_count_df['total_count']
total_count_df = total_count_df.replace(np.nan,0)
display(total_count_df)


# In[ ]:




