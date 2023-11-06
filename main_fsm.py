
from time import sleep
from snap7.util import *
from snap7.types import *
import time
#from gpiozero import CPUTemperature
import sys
from multiprocessing import Process, Manager
from threading import Thread
import pandas as pd

from sequence_detector_hex import detect_all
from score import *
from compare import *
from printer import print_log
from read import read_total, get_reading
from calculate_parameters import find_area, calcula_bit, to_list, calcula_bit_wc, get_curr_path
from alarme import read_alarm
from retraining import routine
import traceback

import requests
from datetime import datetime

import fsm
import os

db_name = None # inicializa a variável db_name como None

curr_path = get_curr_path()

for file in os.listdir(curr_path): # percorre os arquivos do diretório local
    if file.endswith(".db"): # verifica se o arquivo termina com .db
        db_name = file # salva o nome do arquivo na variável db_name
        break # interrompe o loop
    
db_name = curr_path + str(db_name)

print(db_name)

conn = sqlite3.connect(db_name)

dataset2 = pd.read_sql_query('SELECT * FROM GENERAL_PARAMETERS', conn)
parameters2 = dataset2.values.tolist()

IP = str(parameters2[0][13])
RACK = int(parameters2[0][14])
SLOT = int(parameters2[0][15])
TCPPORT = int(parameters2[0][16])

df_path = curr_path + 'I_O_List.xlsx'
df_io = pd.read_excel(df_path)

df_io.columns = ['address','type','name']
#print(df_io)
df_io = df_io.drop(['type'],axis=1)
df_io = df_io.set_index('address')

def register_time():
    file_path = curr_path + 'logs/analisys.log'
    with open(file_path, "w") as f:
        # Obtém a data e hora atual
        agora = datetime.now()
        # Formata a data e hora como uma string
        data_hora = agora.strftime("%Y/%m/%d %H:%M:%S.%f")
        # Escreve a data e hora na primeira linha do arquivo
        f.write(data_hora)

def process_failure(t_num, hex_word, last_state, alarm_bit, next_states, SIZE, ADDRESS,db_name):
    print_log('\n\n#############################',t_num,curr_path)
    
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print_log("\ndate and time = "+ str(dt_string),t_num,curr_path)
    
    print_log('\n' + str(hex_word) + ' <-- FAILURE DETECTED\n' ,t_num,curr_path)
    
    bit_error_list = []
    
    if next_states != {}:
        next_step = get_next(hex_word, next_states, last_state, SIZE,t_num,curr_path)
        bit_error_list = compare(hex_word, next_step[0], SIZE, 'INPUT', ADDRESS, bit_error_list,t_num, df_io, last_state, dt_string, alarm_bit,db_name,curr_path)
    
    print_log('\nRECOMMENDED TO CHECK: ',t_num,curr_path)
    
    if str(last_state) != 'None':
        bit_error_list = also_compare(hex_word, last_state, SIZE,'INPUT', ADDRESS, bit_error_list,t_num, df_io, last_state, dt_string, alarm_bit,db_name,curr_path)
    
    if next_states != {}:
        if len(next_step) > 1:
            for i in range(1, len(next_step)):
                bit_error_list = also_compare(hex_word, next_step[i], SIZE, 'INPUT', ADDRESS, bit_error_list,t_num, df_io, last_state, dt_string, alarm_bit,db_name,curr_path)

def failure_detection(bit_to_del,byte_start,size_word,total_size, t_num, wc_type,wc_position_param,wc_pat,ext_byte,detect_filter, d,region,size_manual,manual_bits, size_alarm, alarm_bits, db_name):
    try:
        
        #print(t_num, 'comecei')
        path_file = curr_path + 'datasets/training/' + t_num + '.xlsx'
        EXCEL = path_file #OK
        detect_filter = int(detect_filter)#percentage to be eliminated on training dataset #OK
        sequences = detect_all(EXCEL,detect_filter,t_num) #OK
        #print(t_num)
        
        initial_list, end_list, all_states = fsm.find_states(sequences)
        
        machine = fsm.FiniteStateMachine(initials = initial_list, finals = end_list, states = all_states, curr_path=curr_path)
        
        fsm.find_transition(sequences, all_states, machine)
        machine.plot_machine(t_num)
        
        input_area = 'input_data' + str(region)
        start_area_str = input_area + '_start'
        start_area = d[start_area_str]

        while(True):
            #print(t_num, 'passei etapa 1')
            if wc_type != 'word':
                wc_position = wc_position_param + 1
        
            SIZE = size_word
            ADDRESS = byte_start
            
            bit_status_list = []
            
            activator = True
            print_new_seq_activator = True

            print('STARTING MONITORING: ',t_num)
            
            #cpu = CPUTemperature()
            first = 0
            #IGNORE FIRST SEQUENCE
            while(activator == True):
                cicle_start = time.time()
                
                hex_word, wc_bit, manual_bit, alarm_bit = get_reading(d,byte_start,size_word,ext_byte,bit_to_del,wc_type,wc_position,total_size,input_area,start_area,size_manual,manual_bits, size_alarm, alarm_bits)
                
                
                if wc_bit == wc_pat:
                    #print(t_num," hex: ",hex_word)
                    if first == 0:
                        #print(t_num,"IGNORING FIRST SEQUENCE")  
                        first = 1
                    pass         
                else:
                    activator = False

            repeat = ''
            locker_next = 0
            end_time = time.time()
            while(True):
                cicle_start = time.time()
                #sleep(0.1)
                #print("--- Waiting %s seconds ---" % (cicle_start - end_time))
                #DATA READING
                hex_word, wc_bit, manual_bit, alarm_bit = get_reading(d,byte_start,size_word,ext_byte,bit_to_del,wc_type,wc_position,total_size,input_area,start_area,size_manual,manual_bits, size_alarm, alarm_bits)
                #se o bit de work complete estiver desativado, ou seja, se estiver rodando uma sequencia
                if wc_bit == wc_pat:
                    if manual_bit == 0 and locker_next == 0:
                        print_new_seq_activator = True
                        #se for a primeira iteração
                        if repeat == '':
                            # # now = datetime.now()
                            # # dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            # # print('STARTING NEW SEQ: ',t_num,' - ', str(dt_string))
                            #altera o valor do repeat para hex_word, assim saberemos se a leitura é igual a anterior
                            repeat = hex_word
                            starting = machine.initialize_pointer(hex_word,t_num)
                            if starting == False:
                                now = datetime.now()
                                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                                print('FALHA ENCONTRADA1',' - ', str(dt_string))
                                last_state = machine.get_last_state()
                                next_states = machine.get_next_states()
                                alarm_score = 0
                                sleep(15)
                                hex_word2, wc_bit2, manual_bit2, alarm_bit2 = get_reading(d,byte_start,size_word,ext_byte,bit_to_del,wc_type,wc_position,total_size,input_area,start_area,size_manual,manual_bits, size_alarm, alarm_bits)
                                alarm_sum = alarm_bit + alarm_bit2
                                if alarm_sum > 0:
                                    alarm_score = 1
                                else:
                                    alarm_score = 0
                                process_failure(t_num, hex_word, last_state, alarm_score, next_states, SIZE, ADDRESS, db_name)
                                print_log('\nway: ' + str(machine.get_way()), t_num, curr_path)
                                activator = True
                                break
                            
                            else:
                                pass
                            #print(t_num,"--- Scan2 %s seconds ---" % (time.time() - cicle_start))
                            #print(hex_word, '<-- WORKING1',t_num)
                        #Se a leitura atual é igual a anterior
                        elif repeat == hex_word:
                            # now = datetime.now()
                            # dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            # print(hex_word, '<-- WORKING2',t_num,' - ', str(dt_string))
                            #print('repeating\n')
                            pass
                            
                        else:
                            repeat = hex_word
                            change = machine.change_state(hex_word,t_num)
                            # # now = datetime.now()
                            # # dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            # # print(hex_word, '<-- CHANGE',t_num,' - ', str(dt_string))
                            if change == False:
                                now = datetime.now()
                                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                                print('FALHA ENCONTRADA2',' - ', str(dt_string))
                                last_state = machine.get_last_state()
                                next_states = machine.get_next_states()
                                alarm_score = 0
                                sleep(15)
                                hex_word2, wc_bit2, manual_bit2, alarm_bit2 = get_reading(d,byte_start,size_word,ext_byte,bit_to_del,wc_type,wc_position,total_size,input_area,start_area,size_manual,manual_bits, size_alarm, alarm_bits)
                                alarm_sum = alarm_bit + alarm_bit2
                                if alarm_sum > 0:
                                    alarm_score = 1
                                else:
                                    alarm_score = 0
                                process_failure(t_num, hex_word, last_state, alarm_score, next_states, SIZE, ADDRESS,db_name)
                                print_log('\nway: ' + str(machine.get_way()), t_num, curr_path)
                                activator = True
                                break
                            #print(t_num,"--- Scan2 %s seconds ---" % (time.time() - cicle_start))
                    else:
                        locker_next = 1
                        # counter = 0
                        # repeat = ''
                        #do not analyse
                        #block next seq to be analysed
                        pass
                else:
                    locker_next = 0
                    #print(t_num,'WAITING')
                    machine.reset_state()
                    repeat = ''
                    if print_new_seq_activator == True:
                        # print('\n-------------------------')
                        # # now = datetime.now()
                        # # dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        # # print(t_num,' WAITING FOR A NEW SEQUENCE',' - ', str(dt_string))
                        # print('\n-------------------------')
                        print_new_seq_activator = False
                end_time = time.time()
                #print(t_num,"--- Scan2 %s seconds ---" % (end_time - cicle_start))
    except:

        errors = sys.exc_info()
        import traceback
        traceback.print_exc()
        for e in errors: 
            print(str(e)) 
            #input('\nPress key to exit.') 
            exit()

def cycle_main(db_name, name_list):
    
    manager = Manager()
    shared_dict = manager.dict()
    
    conn = sqlite3.connect(db_name)
    
    dataset1 = pd.read_sql_query('SELECT * FROM GENERAL_PARAMETERS', conn)
    parameters1 = dataset1.values.tolist()
    
    print(parameters1)

    wc_address = int(parameters1[0][1])
    wc_size = int(parameters1[0][2])
    try:
            wc_alternative_address = int(parameters1[0][3])
            wc_alternative_size = int(parameters1[0][4])
    except:
            wc_alternative_address = parameters1[0][3]
            wc_alternative_size = parameters1[0][4]
    manual_types = to_list(parameters1[0][5])
    manual_addresses = to_list(parameters1[0][6])
    manual_bits = to_list(parameters1[0][7])
    alarm_types = to_list(parameters1[0][8])
    alarm_addresses = to_list(parameters1[0][9])
    alarm_bits = to_list(parameters1[0][10])
    
    start_list =  to_list(parameters1[0][11])
    total_size_list = to_list(parameters1[0][12])
    
    size_manual = len(manual_addresses)
    size_alarm = len(alarm_addresses)
    
    t_main = Process(target=read_total, 
                            args=(IP, RACK, SLOT, TCPPORT, 
                            shared_dict,
                            wc_address,
                            wc_size,
                            wc_alternative_address,
                            wc_alternative_size,
                            manual_types,
                            manual_addresses,
                            alarm_types,
                            alarm_addresses,
                            start_list, 
                            total_size_list))

    t_alarme = Process(target=read_alarm,
                            args=(shared_dict,size_manual,manual_bits, size_alarm, alarm_bits,curr_path))
    
    names = name_list
    names_str = "','".join(names)
    query = "SELECT * FROM PARAMETERS WHERE ANALISYS_NAME IN ('{}');".format(names_str)
    
    dataset = pd.read_sql_query(query, conn)
    parameters = dataset.values.tolist()
    
    process_list = []
    
    t_main.start()
    sleep(3)
    t_alarme.start()
    
    for parameter in parameters:
        print(parameter)
        t = parameter[4]
        start_byte = parameter[2]
        size_word = parameter[3]
        silent_bit = calcula_bit(parameter[1], start_byte, size_word)
        region, total_size = find_area(start_list, total_size_list,start_byte)
        thread_name = parameter[4]
        wc_type = parameter[5]
        wc_position = parameter[6]
        wc_pat = parameter[7]
        wc_ext_byte = parameter[8]
        detect_filter = parameter[9]
        
        if wc_type == 'input':
            wc_position_calculated = wc_position
        elif wc_type == 'memory':
            wc_position_calculated = calcula_bit_wc(wc_address, wc_ext_byte, wc_position)
        elif wc_type == 'memory_alternative':
            wc_position_calculated = calcula_bit_wc(wc_alternative_address, wc_ext_byte, wc_position)
        
        proc = Process(target=failure_detection, 
        args = (
                silent_bit,
                start_byte,
                size_word,
                total_size,
                thread_name,
                wc_type,
                wc_position_calculated,
                wc_pat,
                wc_ext_byte,
                detect_filter,
                shared_dict,
                region,
                size_manual ,manual_bits,
                size_alarm, alarm_bits,
                db_name))
        
        proc.start()
        process_list.append(proc)
    
    training_routine = Process(target=routine, args=(shared_dict,db_name,))
    training_routine.start()
    process_list.append(training_routine)
    
    
    
    for p in process_list:
        p.join()
    
    
def start_main():
    sleep(5)
    conn = sqlite3.connect(db_name)
    
    dataset = pd.read_sql_query('SELECT * FROM PARAMETERS', conn)
    parameters = dataset.values.tolist()
    
    c = conn.cursor()

    # Execute a SELECT statement to retrieve all values from a column of a table
    c.execute('SELECT ANALISYS_NAME FROM PARAMETERS')

    # Fetch all rows and store the values in a list
    column_values = [row[0] for row in c.fetchall()]

    # Close the cursor and connection objects
    c.close()
    conn.close()

    # Print the list of column values
    print(column_values)

    size_columns = len(column_values)
    
    cycle_main(db_name, column_values[0:size_columns])
    
def keep_alive():
    while True:
        sleep(0.5)
        register_time()
    
if __name__ == '__main__':
    t_alive = Thread(target=keep_alive)
    t_alive.start()
    start_main()
