
from get_functions import get_path
from flask import request, render_template
import sqlite3
import os
from get_functions import get_curr_path

def add_parameter():
        db_path, log_path = get_path()
        connection = sqlite3.connect(db_path)
        cur = connection.cursor()
        
        silent = request.values.get("silent")
        if silent == '':
            silent = 'null'
        start = int(request.values.get("start"))
        size = int(request.values.get("size"))
        name = request.values.get("name")
        name0 = name + '_0'
        name1 = name + '_1'
        wctype = request.values.get("type")
        wcpos = int(request.values.get("wcpos"))
        wcbyte = int(request.values.get("wcbyte"))
        
        cur.execute('SELECT id FROM PARAMETERS WHERE ANALISYS_NAME=?', (name0,))
        existing_id0 = cur.fetchone()
        cur.execute('SELECT id FROM PARAMETERS WHERE ANALISYS_NAME=?', (name1,))
        existing_id1 = cur.fetchone()

        if existing_id0 or existing_id1:
            error_message = 'This name is already in use. Try another name'
            
            # Exiba uma mensagem de erro ou redirecione para a página de edição com uma mensagem de erro
            return render_template('add.html', error_message=error_message)

        connection.execute("INSERT INTO PARAMETERS ('SILENT_BIT', 'START_BYTE', 'SIZE_WORD', 'ANALISYS_NAME', 'WORK_COMPLETE_TYPE', 'WORK_COMPLETE_POSITION', 'ANALISYS_PATTERN', 'WORK_COMPLETE_EXTERNAL_BYTE', 'DETECT_FILTER') \
                        VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5}, {6},{7},{8})"
                        .format(silent,start,size,name0,wctype,wcpos,0,wcbyte,0)) 
        connection.execute("INSERT INTO PARAMETERS ('SILENT_BIT', 'START_BYTE', 'SIZE_WORD', 'ANALISYS_NAME', 'WORK_COMPLETE_TYPE', 'WORK_COMPLETE_POSITION', 'ANALISYS_PATTERN', 'WORK_COMPLETE_EXTERNAL_BYTE', 'DETECT_FILTER') \
                        VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5}, {6},{7},{8})"
                        .format(silent,start,size,name1,wctype,wcpos,1,wcbyte,0)) 
        connection.commit()
        connection.close()
        
def edit_parameter(id,name,pattern,db_path):
    
    curr_path = get_curr_path()
    
    dataset_path = curr_path + 'datasets/training/'
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    
    silent = request.values.get("silent")
    if silent == '':
        silent = 'null'
    start = int(request.values.get("start"))
    size = int(request.values.get("size"))
    
    new_name = request.values.get("name")
    
    if pattern == 1 and new_name[-2:] != '_1' and new_name[-2:] != '_0':
        new_name = new_name + '_1'
    elif pattern == 0 and new_name[-2:] != '_0' and new_name[-2:] != '_1':
        new_name = new_name + '_0'
        
    wctype = request.values.get("type")
    wcpos = int(request.values.get("wcpos"))
    wcbyte = int(request.values.get("wcbyte"))
    
    cur.execute('SELECT id FROM PARAMETERS WHERE ANALISYS_NAME=?', (new_name,))
    existing_id = cur.fetchone()

    if existing_id and existing_id[0] != id:
        error_message = 'This name is already in use. Try another name'
        
        cur.execute('SELECT * FROM PARAMETERS WHERE id=?', (id,))
        record = cur.fetchone()
        connection.close()
        
        # Exiba uma mensagem de erro ou redirecione para a página de edição com uma mensagem de erro
        return render_template('editing.html', error_message=error_message, record=record, id=id, name=new_name)

    consulta =  '''
                UPDATE PARAMETERS
                SET SILENT_BIT= ?,
                START_BYTE = ?,
                SIZE_WORD = ?,
                ANALISYS_NAME = ?,
                WORK_COMPLETE_TYPE = ?,
                WORK_COMPLETE_POSITION = ?,
                ANALISYS_PATTERN = ?,
                WORK_COMPLETE_EXTERNAL_BYTE = ?,
                DETECT_FILTER = ? 
                WHERE ID = ?
                '''
    
    connection.execute(consulta,(silent,start,size,new_name,wctype,wcpos,pattern,wcbyte,0,id,))
    
    connection.commit()

    cur = connection.cursor()
    cur.execute('SELECT * FROM PARAMETERS')
    data = cur.fetchall()
    connection.close()
    
    namecheck = name + '.xlsx'
    new = new_name + '.xlsx'
    
    # Lista todos os arquivos no diretório dataset_path
    for file_name in os.listdir(dataset_path):
        
        # Verifica se o nome do arquivo corresponde ao nome recebido
        if file_name == namecheck:
            print('é igual')
            # Constrói o caminho completo do arquivo antigo
            old_file_path = os.path.join(dataset_path, file_name)
            # Constrói o caminho completo do novo arquivo com o novo nome
            new_file_path = os.path.join(dataset_path, new)
            # Renomeia o arquivo antigo com o novo nome
            os.rename(old_file_path, new_file_path)


    return render_template("edit.html", data=data)

def edit_general_parameters(db_path):
    curr_path = get_curr_path()
    dataset_path = curr_path + 'datasets/training/'
    
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    
    wcaddress = int(request.values.get("wcaddress"))
    wcsize = int(request.values.get("wcsize"))
    altwcaddress = int(request.values.get("altwcaddress"))
    altwcsize = int(request.values.get("altwcsize"))
    manualbytes = request.values.get("manualbytes")
    manualbits = request.values.get("manualbits")
    manualtypes = request.values.get("manualtypes")
    alarmbytes = request.values.get("alarmbytes")
    alarmbits = request.values.get("alarmbits")
    alarmtypes = request.values.get("alarmtypes")
    blockbytes = request.values.get("blockbytes")
    blocksize = request.values.get("blocksize")
    plcip = request.values.get("plcip")
    plcrack = request.values.get("plcrack")
    plcslot = request.values.get("plcslot")
    plctcp = request.values.get("plctcp")

    consulta =  '''
                UPDATE GENERAL_PARAMETERS
                SET WC_ADDRESS= ?,
                WC_SIZE = ?,
                WC_ALTERNATIVE_ADDRESS = ?,
                WC_ALTERNATIVE_SIZE = ?,
                MANUAL_TYPES = ?,
                MANUAL_ADDRESSES = ?,
                MANUAL_BITS = ?,
                ALARM_TYPES = ?,
                ALARM_ADDRESSES = ?,
                ALARM_BITS = ?,
                START_LIST = ?,
                TOTAL_SIZE_LIST = ?,
                IP = ?,
                RACK = ?,
                SLOT = ?,
                TCPPORT = ?
                WHERE ID = ?;
                '''
    
    connection.execute(consulta,(wcaddress,wcsize,altwcaddress,altwcsize,manualtypes,manualbytes,manualbits,alarmtypes,alarmbytes,alarmbits,blockbytes,blocksize,plcip,plcrack,plcslot,plctcp,1))
    
    connection.commit()
    connection.close()