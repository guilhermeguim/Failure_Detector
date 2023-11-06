from printer import print_log
import sqlite3


def compare(hex_word, pattern  ,SIZE, WHERE_TO_READ_PLC, ADDRESS, bit_error_list,t_num, df, last_state, dt_string, alarm_bit, db_name,curr_path):
    
    conn = sqlite3.connect(db_name)
    
    if alarm_bit == 1:
        classe = 1
    else:
        classe = 3
    
    bit_status = []
    
    for i in range(SIZE*8):
        bit_status.append('FAILURE')
    
    
    binary_value = bin(int(hex_word, 16))[2:].zfill(SIZE*8)
    binary_pattern = bin(int(pattern, 16))[2:].zfill(SIZE*8)
    
    for bit in range(len(binary_pattern)):
        if binary_value[bit] == binary_pattern[bit]:
            bit_status[bit] = "WORKING"
        else:
            pass
        
    print_log("\n\n--------FAILURE--------\n",t_num,curr_path)
    print_log(str(hex_word)+"<--FOUND\n",t_num,curr_path)
    print_log(str(binary_value)+'\n',t_num,curr_path)
    print_log(str(pattern)+"<--EXPECTED\n",t_num,curr_path)
    print_log(str(binary_pattern)+'\n',t_num,curr_path)
    print_log('-----------------------------------------',t_num,curr_path)
    
    placer = 8

    for i in range(len(bit_status)):
        if placer == 0:
            placer = 8
            SIZE = SIZE-1
        placer = placer - 1
        if bit_status[i] == 'FAILURE':
            if WHERE_TO_READ_PLC == 'OUTPUT':
                d_type = 'Q'
                address = str(ADDRESS+SIZE-1) + '.' + str(placer)
                failure_address = d_type + address
                failure = failure_address +': '+bit_status[i]
                device = df._get_value(failure_address, 'name')
                device = str(device)
                device = device.replace("'","")
                device = device.replace('"','')
                print_log('\n' + str(failure) + ' (' + str(device) + ')',t_num,curr_path)
                bit_error_list.append(failure)
                conn.execute("INSERT INTO FAILURE_HIST (D_TYPE,ADDRESS,CLASS,DESCRIPTION,DATE_TIME,LAST_STATE,EXPECTED_STATE,FOUND_STATE) \
                        VALUES ('{0}', {1}, {2}, '{3}', '{4}', '{5}','{6}','{7}')"
                        .format(d_type,address,classe,device,dt_string,last_state,pattern,hex_word)) 
                
            else:
                d_type = 'I'
                address = str(ADDRESS+SIZE-1) + '.' + str(placer)
                failure_address = d_type + address
                failure = failure_address +': '+bit_status[i]
                device = df._get_value(failure_address, 'name')
                device = str(device)
                device = device.replace("'","")
                device = device.replace('"','')
                print_log('\n' + str(failure) + ' (' + str(device) + ')',t_num,curr_path)
                bit_error_list.append(failure)
                conn.execute("INSERT INTO FAILURE_HIST (D_TYPE,ADDRESS,CLASS,DESCRIPTION,DATE_TIME,LAST_STATE,EXPECTED_STATE,FOUND_STATE) \
                        VALUES ('{0}', {1}, {2}, '{3}', '{4}', '{5}','{6}','{7}')"
                        .format(d_type,address,classe,device,dt_string,last_state,pattern,hex_word))
    
    conn.commit()
    conn.close()
    
    return bit_error_list

def also_compare(hex_word, pattern ,SIZE, WHERE_TO_READ_PLC, ADDRESS, bit_error_list,t_num, df, last_state, dt_string, alarm_bit,db_name,curr_path):
    
    conn = sqlite3.connect(db_name)
    
    if alarm_bit == 1:
        classe = 2
    else:
        classe = 4
    
    bit_status = []
    
    for i in range(SIZE*8):
        bit_status.append('FAILURE')
        
    binary_value = bin(int(hex_word, 16))[2:].zfill(SIZE*8)
    binary_pattern = bin(int(pattern, 16))[2:].zfill(SIZE*8)
    
    for bit in range(len(binary_pattern)):
        if binary_value[bit] == binary_pattern[bit]:
            bit_status[bit] = "WORKING"
        else:
            pass

    print_log('\n' + str(pattern) + "<--EXPECTED\n",t_num,curr_path)
    print_log(str(binary_pattern),t_num,curr_path)
    
    placer = 8

    for i in range(len(bit_status)):
        if placer == 0:
            placer = 8
            SIZE = SIZE-1
        placer = placer - 1
        if bit_status[i] == 'FAILURE':
            if WHERE_TO_READ_PLC == 'OUTPUT':
                d_type = 'Q'
                address = str(ADDRESS+SIZE-1) + '.' + str(placer)
                failure_address = d_type + address
                failure = failure_address +': '+bit_status[i]
                if failure in bit_error_list:
                    pass
                else:
                    device = df._get_value(failure_address, 'name')
                    device = str(device)
                    device = device.replace("'","")
                    device = device.replace('"','')
                    print_log('\n' + str(failure) + ' (' + str(device) + ')',t_num,curr_path)
                    bit_error_list.append(failure)
                    conn.execute("INSERT INTO FAILURE_HIST (D_TYPE,ADDRESS,CLASS,DESCRIPTION,DATE_TIME,LAST_STATE,EXPECTED_STATE,FOUND_STATE) \
                        VALUES ('{0}', {1}, {2}, '{3}', '{4}', '{5}','{6}','{7}')"
                        .format(d_type,address,classe,device,dt_string,last_state,pattern,hex_word)) 
            else:
                d_type = 'I'
                address = str(ADDRESS+SIZE-1) + '.' + str(placer)
                failure_address = d_type + address
                failure = failure_address +': '+bit_status[i]
                if failure in bit_error_list:
                    pass
                else:
                    device = df._get_value(failure_address, 'name')
                    device = str(device)
                    device = device.replace("'","")
                    device = device.replace('"','')
                    print_log('\n' + str(failure) + ' (' + str(device) + ')',t_num,curr_path)
                    bit_error_list.append(failure)
                    conn.execute("INSERT INTO FAILURE_HIST (D_TYPE,ADDRESS,CLASS,DESCRIPTION,DATE_TIME,LAST_STATE,EXPECTED_STATE,FOUND_STATE) \
                                VALUES ('{0}', {1}, {2}, '{3}', '{4}', '{5}','{6}','{7}')"
                                .format(d_type,address,classe,device,dt_string,last_state,pattern,hex_word))   
    
    conn.commit()
    conn.close()
    return bit_error_list