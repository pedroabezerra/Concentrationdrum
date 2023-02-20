#!/usr/bin/env python
# coding: utf-8

# In[246]:


import os
import glob
import numpy as np
import pandas as pd


# In[247]:


NF = 50 #number of files
NP = 57300 #number of particles


# In[248]:


contador1 = list()
contador2 = list()
contador = list()
concentracao1 = list()
concentracao2 = list()
Tipo = np.zeros((NP,NF))
posicaoX = np.zeros((NP,NF))
posicaoY = np.zeros((NP,NF))


# In[249]:


#construção das repartições no tambor
nd_x = 5
nd_y = 5

max_x = 0.075
min_x = -0.075
max_y = 0.075
min_y = -0.075
esp_x = (max_x - min_x)/nd_x
esp_y = (max_y - min_y)/nd_y


# In[250]:


#leitura dos dados
#j = 1
#for i in range(0,NF):
    #Dados = pd.read_csv('rot_{}.csv'.format(i))
    #Dados_filter = Dados.filter(items=['type','Points:0','Points:1'])
    #posicaoX[0:i] = Dados_filter['Points:0'].copy()
    
    #posicaoX[0:i] = Dados_filter.loc[:,:2].copy()

    #posicaoX.append(posicaoX[i])
    #posicaoY[i] = Dados.iloc[2].copy()
    #j = j + 1
    
#display(Dados_Filter)
#display(posicaoX)
#display(Dados_Filter.iloc[:,[0,1]])
#display(Dados_Filter.loc['Points:0'])
#display(Dados_Filter.iloc[:,2:3])
#Dados_filter.shape
#display(Dados_Filter.iloc[1])


# In[251]:


#leitura dos dados

home = os.path.expanduser("~")
path = f"E:/PIBIC/efeito da dimensao do tambor - densidade/70/dados_rot"
all_files = glob.glob(path + "/*.csv")
Dados = pd.concat((pd.read_csv(f) for f in all_files))
Dados_filter = Dados.filter(items=['type','Points:0','Points:1'])
display(Dados_filter)


# In[252]:


#construção do ponteiro para localização
cd1 = Dados_filter
cd1['Points:0'] = Dados_filter['Points:0'].div(esp_x).round(0)+3
cd1['Points:1'] = Dados_filter['Points:1'].div(esp_y).round(0)+3
posicao = -5+cd1['Points:0']+5*cd1['Points:1']
cd1 = cd1.assign(posicao = posicao.values)
print(cd1)


# In[253]:


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


# In[254]:


#cálculo da concentração por tipo de partícula

total_count_df = pd.merge(count3, count4, on='posicao',how='left')
total_count = total_count_df['count_x'].add(total_count_df['count_y'], fill_value=0)
total_count_df['total_count']= total_count
total_count_df['concentracao_1']= total_count_df['count_x'] / total_count_df['total_count']
total_count_df['concentracao_2']= total_count_df['count_y'] / total_count_df['total_count']
total_count_df = total_count_df.replace(np.nan,0)
display(total_count_df)


# In[255]:


#cálculo da concentração

#if dftype1.shape[0] >= dftype2.shape[0]:
    #for i in range(0,dftype1.shape[0]):
        #for j in range(0,dftype2.shape[0]):
            #if dftype1.iloc[i]['posicao'] == dftype2.iloc[j]['posicao']:
                #concentracao_1 = dftype1.iloc[i]['count']/(dftype1.iloc[i]['count'] + dftype2.iloc[j]['count'])
                #concentracao1.insert(i, concentracao_1)
                
#else:
    #for i in range(0,dftype2.shape[0]):
       # for j in range(0,dftype1.shape[0]):
            #if dftype2.iloc[i]['posicao'] == dftype1.iloc[j]['posicao']:
                #concentracao_2 = dftype2.iloc[i]['count']/(dftype1.iloc[i]['count'] + dftype2.iloc[j]['count'])
                #concentracao2.insert(i, concentracao_2)
                
#print(dftype1.shape[0])
#print(dftype2.shape[0])


# In[ ]:




