import pandas as pd
from collections import Counter

def detect(dataset,DETECT_FILTER,t_num):

    minimal = DETECT_FILTER #valor em porcentagem

    ##PREPARAÇÃO DOS DADOS EM DATAFRAME
    #print(t_num,'started detection')
    df = pd.read_excel(dataset, header=None,dtype=str) #faz a leitura do arquivo excel definido e o converte para um Pandas Dataframe
    df = df.reset_index(drop=True) #Limpa qualquer tipo de index que venha como sujeira da planilha
    
    n_columns = df.shape[1] #conta quantidade de colunas
    n_rows = df.shape[0] #conta quantidade de linhas

    df = df.fillna('to_clear') #substitui os valores nulos do DF com valor 0
    #print(t_num,'filled')
    
    #Durante a importação do arquivo, algumas células vem com tipos de dados diferentes, então faremos a normalização
    #para que todos os dados sejam tratados como sring
    
    
    # for i in range(n_columns):
    #     for j in range(n_rows): #percorre todas as células do dataframe
    #         if t_num == 180.0:
    #             print('i:',i,'| j:',j)
    #         #as celulas que foram lidas como float, quando convertidas para string,
    #         #irão herdar a virgula ou ponto, então iremos converter esses dados para int e depois para string
    #         if type(df[i][j]) == np.float64 or type(df[i][j]) == float: #se encotrada uma celula do tipo float
    #             df.at[j,i] = str(int(df[i][j])) #converte para int para tirar a virgula e depois para string

    #print(t_num,'pattern done')
    df = df.astype(str) #converte toda a tabela para string

    ##CONTAGEM DAS SEQUENCIAS

    df_array = df.to_numpy() #converte as linhas do dataframe para um array com todas as sequencias lidas

    counter = Counter(map(tuple, df_array)) #a função Counter irá contar quantas vezes cada sequencia aparece no dataframe
    #print(counter)
    #Retorno:
    '''Counter({('20005501','2fd75501','2bd95501','2bd55501','3a055501','20255501','30275501','20255501','20005501','20005401','0'): 11,
            ('20005501','2fd75501','2bd95501','2bd55501','3a055501','2a055501','20255501','30275501','20255501','20005501','0'): 13})'''

    #print(t_num,'counted')
    
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
        
    #print(t_num,'to list')

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
        
    #print(t_num,'removed minimum')

    #Remove os elementos 0 que ficam no final de cada sequencia
    clean_detected = []


    for i in detected:
        if 'to_clear' in i:
            i = [x for x in i if x != 'to_clear']
            clean_detected.append(i)
        else:
            clean_detected.append(i)

    #print(t_num,'clear')
    
    # for i in clean_detected:
    #     print(t_num,':',i)
    
    return clean_detected

def detect_all(dataset,DETECT_FILTER,t_num):

    minimal = DETECT_FILTER #valor em porcentagem

    ##PREPARAÇÃO DOS DADOS EM DATAFRAME
    #print(t_num,'started detection')
    df = pd.read_excel(dataset, header=None,dtype=str) #faz a leitura do arquivo excel definido e o converte para um Pandas Dataframe
    df = df.reset_index(drop=True) #Limpa qualquer tipo de index que venha como sujeira da planilha
    
    n_columns = df.shape[1] #conta quantidade de colunas
    n_rows = df.shape[0] #conta quantidade de linhas

    df = df.fillna('to_clear') #substitui os valores nulos do DF com valor 0
    #print(t_num,'filled')
    
    #Durante a importação do arquivo, algumas células vem com tipos de dados diferentes, então faremos a normalização
    #para que todos os dados sejam tratados como sring
    
    
    # for i in range(n_columns):
    #     for j in range(n_rows): #percorre todas as células do dataframe
    #         if t_num == 180.0:
    #             print('i:',i,'| j:',j)
    #         #as celulas que foram lidas como float, quando convertidas para string,
    #         #irão herdar a virgula ou ponto, então iremos converter esses dados para int e depois para string
    #         if type(df[i][j]) == np.float64 or type(df[i][j]) == float: #se encotrada uma celula do tipo float
    #             df.at[j,i] = str(int(df[i][j])) #converte para int para tirar a virgula e depois para string

    #print(t_num,'pattern done')
    df = df.astype(str) #converte toda a tabela para string

    ##CONTAGEM DAS SEQUENCIAS

    df_array = df.to_numpy() #converte as linhas do dataframe para um array com todas as sequencias lidas

    detected = []

    for i in df_array:
        detected.append(i)
    
    #Remove os elementos 0 que ficam no final de cada sequencia
    clean_detected = []


    for i in detected:
        if 'to_clear' in i:
            i = [x for x in i if x != 'to_clear']
            clean_detected.append(i)
        else:
            clean_detected.append(i)

    #print(t_num,'clear')
    
    # for i in clean_detected:
    #     print(t_num,':',i)
    
    return clean_detected

# sequencias = detect('C:/Users/37107014/Desktop/Q30_Engine_Failure_Detector-Validation_PC/get_data/training/coleta_in1_0thread.xlsx',0,1)

# for sequencia in sequencias:
#     print(sequencia)
