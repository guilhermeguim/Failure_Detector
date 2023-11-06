import os
import sqlite3
from datetime import datetime, timedelta, date
import pandas as pd
from flask import request

def get_path():
    db_name = None # inicializa a variável db_name como None

    curr_path = get_curr_path()
    
    print(os.listdir(curr_path))

    for file in os.listdir(curr_path): # percorre os arquivos do diretório local
        if file.endswith(".db"): # verifica se o arquivo termina com .db
            db_name = file # salva o nome do arquivo na variável db_name
            break # interrompe o loop
    db_path = curr_path + str(db_name)

    print(db_path)
    
    log_path = curr_path + 'logs/alarm.log'
    
    return db_path, log_path
    
def get_data_hist(class_value):
    # Connect to the database
    db_path, log_path = get_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Get all rows from the table
    
    last_24_hours = datetime.now() - timedelta(hours=24)

    # Escreve uma consulta SQL para selecionar dados da última 24 horas
    if class_value is None:
        class_value = 1

    sql = f'''SELECT ID, D_TYPE, ADDRESS, CLASS, DESCRIPTION, DATE_TIME
            FROM FAILURE_HIST
            WHERE DATE_TIME >= ? AND CLASS = ?
            ORDER BY ID DESC'''
            
    if class_value == 5:
        sql = f'''SELECT ID, D_TYPE, ADDRESS, CLASS, DESCRIPTION, DATE_TIME
            FROM FAILURE_HIST
            WHERE DATE_TIME >= ?
            ORDER BY ID DESC'''
            
            
    if class_value == 5:
        cur.execute(sql, (last_24_hours,))
    else:
        cur.execute(sql, (last_24_hours,class_value,))
        
    
    data = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()
    
    return data

def get_manual_alarm():
    db_path, log_path = get_path()
    class_value = request.args.get('class_value', default=None, type=str)  # Get the selected CLASS value from the request parameters
    
    # Lê o conteúdo do arquivo de texto
    with open(log_path, 'r') as file:
        lines = file.read().splitlines()
    
    # Cria uma lista vazia para armazenar os dados
    dados = []

    # Itera sobre as linhas e extrai as informações
    for line in lines:
        # Separa a linha no primeiro ':'
        partes = line.split(':', 1)
        
        if len(partes) == 2:
            informacao = partes[0].strip()
            restante = partes[1].strip()
            
            # Separa a parte restante em data e horário
            data, horario = restante.split(' ', 1)
            
            # Adiciona os dados à lista
            dados.append([informacao, data, horario])

    # Cria o dataframe com as colunas nomeadas
    df = pd.DataFrame(dados, columns=['Type', 'Date', 'Time'])
    
    # Converter a coluna 'Date' para o tipo de dados datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Obter a data atual
    data_atual = datetime.now()

    # Calcular a data de início dos últimos 15 dias
    data_inicio = data_atual - timedelta(days=15)

    # Filtrar o DataFrame para ter apenas dados dos últimos 15 dias
    df_filtrado = df[(df['Date'] >= data_inicio) & (df['Date'] <= data_atual)]
    
    # Filtrar o dataframe df_filtrado
    today_df = df_filtrado[df_filtrado['Date'] == class_value].copy()
            
    # Converter a coluna 'Date' de volta para string
    df_filtrado['Date'] = df_filtrado['Date'].dt.strftime('%Y-%m-%d')
    today_df['Date'] = today_df['Date'].dt.strftime('%Y-%m-%d')
        
    # Converter DataFrame para um dicionário
    df_tuples = [tuple(x) for x in df_filtrado.to_records(index=False)]
    today_df_tuples = [tuple(x) for x in today_df.to_records(index=False)]
    df_tuples.reverse()
    today_df_tuples.reverse()
    
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    
    # Obter uma lista com cada valor único da coluna 'Data'
    date_values = df_filtrado['Date'].unique().tolist()
    date_values.reverse()
    
    return df_tuples, today_df_tuples, date_string, date_values

def clean_directory():
        curr_path = get_curr_path()
        # Define o caminho da pasta
        pasta = curr_path + 'datasets'

        # Lista todos os arquivos .xlsx na pasta
        arquivos = os.listdir(pasta)

        # Percorre cada arquivo e verifica se é .xlsx
        for arquivo in arquivos:
        # Se for .xlsx, o apaga
                if arquivo.endswith('.xlsx'):
                        os.remove(os.path.join(pasta, arquivo))
                        #print(f'Arquivo {arquivo} apagado.')

def get_directory_size_xlsx():
    curr_path = get_curr_path()
    path = curr_path +'datasets'
    files = os.listdir(path)
    count = 0
    for file in files:
        if file.endswith('.xlsx'):
            count += 1
    return count

def get_curr_path():
    curr_path = os.path.dirname (os.path.abspath (__file__))
    curr_path = curr_path.replace('\\', '/')  # Substitui as barras invertidas por barras normais
    curr_path = curr_path.replace('interface', '')
    return curr_path
    
if __name__ == "__main__":
    print(get_curr_path())