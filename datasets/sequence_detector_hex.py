import pandas as pd
import numpy as np
from collections import Counter
from os import listdir
from os.path import isfile, join

def detect(dataset):

    minimal = 1 #valor em porcentagem

    ##PREPARAÇÃO DOS DADOS EM DATAFRAME

    df = pd.read_excel(dataset, header=None,dtype=str) #faz a leitura do arquivo excel definido e o converte para um Pandas Dataframe
    df = df.reset_index(drop=True) #Limpa qualquer tipo de index que venha como sujeira da planilha

    df = df.fillna('to_clear')
        
    df = df.iloc[1:-1]
    
    df = df.reset_index(drop=True)
    
    col_list = df.columns.to_list()
    
    df = df.sort_values(by=col_list) 
    
    n_columns = df.shape[1] #conta quantidade de colunas
    n_rows = df.shape[0] #conta quantidade de linhas
    
    #Durante a importação do arquivo, algumas células vem com tipos de dados diferentes, então faremos a normalização
    #para que todos os dados sejam tratados como sring
    # for i in range(n_columns):
    #     for j in range(n_rows): #percorre todas as células do dataframe
    #             #as celulas que foram lidas como float, quando convertidas para string,
    #             #irão herdar a virgula ou ponto, então iremos converter esses dados para int e depois para string
    #             if type(df[i][j]) == np.float64 or type(df[i][j]) == float: #se encotrada uma celula do tipo float
    #                 df.at[j,i] = str(int(df[i][j])) #converte para int para tirar a virgula e depois para string

    df = df.astype(str) #converte toda a tabela para string

    ##CONTAGEM DAS SEQUENCIAS

    df_array = df.to_numpy() #converte as linhas do dataframe para um array com todas as sequencias lidas

    counter = Counter(map(tuple, df_array)) #a função Counter irá contar quantas vezes cada sequencia aparece no dataframe
    #print(counter)
    #Retorno:
    '''Counter({('20005501','2fd75501','2bd95501','2bd55501','3a055501','20255501','30275501','20255501','20005501','20005401','0'): 11,
            ('20005501','2fd75501','2bd95501','2bd55501','3a055501','2a055501','20255501','30275501','20255501','20005501','0'): 13})'''

    #cria as listas de operação
    detected_tuple = []
    counts = []
    temp = []
    detected = []

    for unique_list in counter: #para cada sequencia contada
            detected_tuple.append(unique_list) #alimenta lista com as sequencias
            counts.append(counter[unique_list]) #alimenta lista com a quantidade de vezes que ocorre a sequencia

    #as sequencias lidas estão como tuplas, então será percorrido cada elemento e realimentado em outra lista
    #para que fique no formato de lista
    for i in detected_tuple:
        for j in i:
            temp.append(j)
        detected.append(temp)
        temp = []

    #remove as sequencias que aparecem menos vezes do que a porcentagem estabelecida em 'minimal',
    #serão tratadas como erro.
    to_remove = []
    
    if (n_rows/100)*minimal >= 1:
        minimal_value = (n_rows/100)*minimal
    else:
        minimal_value = 1
        
    minimal_value = 0
    
    for i in range(len(counts)):
        if counts[i] <= minimal_value:
            to_remove.append(i)
    for i in reversed(to_remove):
        del detected[i]
        del counts[i]

    #Remove os elementos 0 que ficam no final de cada sequencia
    clean_detected = []

    for i in detected:
        if 'to_clear' in i:
            i = [x for x in i if x != 'to_clear']
            clean_detected.append(i)
        else:
            clean_detected.append(i)
            
            

    return clean_detected, counts, n_rows

mypath = 'C:/Users/37107014/Desktop/Q30_Engine_Failure_Detector-Validation_PC/get_data/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

file_object = open('contagem.txt', 'a')

for file in onlyfiles:
    if file[-1] != 'y' and file[-1] != 'r':
        path_read = 'C:/Users/37107014/Desktop/Q30_Engine_Failure_Detector-Validation_PC/get_data/' + file
        print(path_read)
        file_object.write(path_read)
        file_object.write('\n')
        sequencias, contagens, n_rows = detect(path_read)


        for i in range(len(sequencias)):
            file_object.write(str(sequencias[i])+': '+str(contagens[i]))
            file_object.write('\n')
            
        tx = 1-(len(sequencias) / n_rows)
        tx = round(tx,3)
        file_object.write('SQ =  '+ str(tx)+'/'+str(len(sequencias))+'/'+str(n_rows))
        file_object.write('\n')
        # file_object.write('SEQUENCIAS:'+str(n_rows))
        # file_object.write('\n')
        # file_object.write('QTD:'+str(len(sequencias)))
        # file_object.write('\n')
        file_object.write('-------------------------------------------------------')
        file_object.write('\n')
        
        
file_object.close()