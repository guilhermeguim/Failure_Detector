import time
import snap7.client as c
from snap7.util import *
from snap7.types import *

def read_total(IP, RACK, SLOT, TCPPORT, d, wc_address, wc_size, wc_alternative_address, wc_alternative_size,
                manual_types, manual_addresses, alarm_types, alarm_addresses,
                start_list, total_size_list):
        
    print('STARTED READING')
    
        #cria o objeto PLC com os métodos da biblioteca SNAP7
    plc = c.Client()
    #seta o tipo de conexão para S7 Basic connection https://sourceforge.net/p/snap7/discussion/general/thread/ce29071c/
    plc.set_connection_type(0xFD)  
    #conecta o objeto PLC com o PLC real
    plc.connect(IP, RACK, SLOT, TCPPORT)
    #verifica se a conexão foi iniciada
    print(plc.get_connected())
    
    #DATA READING
    for i in range(len(start_list)):
            name_start = 'input_data' + str(start_list[i]) + '_start'
            d[name_start] = start_list[i]

    ##Work Complete
    read_final = time.time()
    while True:
            
            read_start = time.time()
            #print("--- Waiting %s seconds ---" % (read_start - read_final))
            
            d['wc_data'] = plc.read_area(Areas.MK, 0, wc_address, wc_size)
            
            if wc_alternative_address == '':
                    d['wc_data_alt'] = 0 #plc.read_area(Areas.MK, 0, 72, 3)
            else:
                    d['wc_data_alt'] = plc.read_area(Areas.MK, 0, wc_alternative_address, wc_alternative_size)
            ##Output
            # output_data = plc.read_area(Areas.PA, 0, 632, 4)
            ##Input
            name_input = 'input_data100' #+ str(start_list[i])
            name_start =  name_input + '_start'
            
            for i in range(len(start_list)):
                    if i == 0:
                        
                        leitura = plc.read_area(Areas.PE, 0, start_list[i] , total_size_list[i])
                        print('start: ', start_list[i], '--> ', leitura)
                    else:
                        nova_leitura = plc.read_area(Areas.PE, 0, start_list[i] , total_size_list[i])
                        print('start: ', start_list[i], '--> ', nova_leitura)
                        leitura.extend(nova_leitura)

            d[name_input] = leitura
            print('leitura:',leitura)
            for i in range(len(manual_types)):
                    name_manual = 'manual' + str(i)
                    d[name_manual] = plc.read_area(manual_types[i], 0, manual_addresses[i], 1) #I20.2
            for i in range(len(alarm_types)):
                    name_alarm = 'alarm' + str(i)
                    d[name_alarm] = plc.read_area(alarm_types[i], 0, alarm_addresses[i], 1) #M24.5

            read_final = time.time()
            #print("--- Reading %s seconds ---" % (read_final - read_start))

def get_reading(d,byte_start,size_word,ext_byte,bit_to_del,wc_type,wc_position,total_size,input_area,start_area,size_manual,manual_bits, size_alarm, alarm_bits):
        #DATA READING
        input_bit_array_total = bin(int.from_bytes(d[input_area], byteorder='little'))[2:].zfill(8*total_size)
        print('nao sei: ',input_bit_array_total)
        
        if ext_byte == 'null':
                ext_byte = 0
        
        size = len(str(input_bit_array_total))
        start = size-(((byte_start-start_area)+size_word)*8)
        end = start + (size_word*8)
        
        input_bit_array = str(input_bit_array_total)[start : end]

        start_wc = size-(((ext_byte-start_area)+1)*8)
        end_wc = start_wc + (1*8)
        wc_input_bit_array = str(input_bit_array_total)[start_wc : end_wc]
        
        ##Os 40 MSB representarm saídas e 40 LSB as saídas
        binary_word = input_bit_array
        binary_word = str(binary_word)
        wc_input_bit_array = str(wc_input_bit_array)
        
        if len(bit_to_del) != 0:
                for i in bit_to_del:
                        binary_word = binary_word[:i]+'1'+binary_word[i+1:]
        # print(binary_word)

        #Converte a word binaria para hexadecimal para facilitar o armazenamento
        hex_word = hex(int(binary_word,2))[2:]
        print('hex:',hex_word)
        
        # #Contador do tamanho das listas auxiliares
        # size = int(len(list_hex))
        # size_one = int(len(list_one))
        
        #print('Temp=',cpu.temperature,'°')
        
        #Work Complete Memory and Bit convertion
        #print("WORK COMPLETE")
        
        if wc_type == 'memory':
                #print(wc_data)
                #Converte o bitearray lido do plc para um binario
                bit_array = bin(int.from_bytes(d['wc_data'] , byteorder='little'))[2:].zfill(8)
                #print(bit_array)
                #print(bit_array)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                wc_bit = bit_array[len(bit_array)-wc_position]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                wc_bit = int(wc_bit)
                #print(t_num,"WC Bit:", wc_bit)
        
        elif wc_type == 'memory_alternative':
                #print(wc_data_alt)
                #Converte o bitearray lido do plc para um binario
                bit_array = bin(int.from_bytes(d['wc_data_alt'], byteorder='little'))[2:].zfill(8*3)
                #print(bit_array)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                wc_bit = bit_array[len(bit_array)-wc_position]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                wc_bit = int(wc_bit)
                #print("WC Bit:", wc_bit)
        
        elif wc_type == 'input':
                #print('##',wc_input_bit_array)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                wc_bit = wc_input_bit_array[len(wc_input_bit_array)-wc_position]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                wc_bit = int(wc_bit)
                #print("##WC Bit:", wc_bit)
        
        # elif wc_type == 'int':
        #     wc_bit = binary_word_before[len(binary_word_before)-wc_position]
        #     #O bit selecionado vem como string, então convertemos para int para possibilitar operações
        #     wc_bit = int(wc_bit)
        #     print("WC Bit:", wc_bit)

        elif wc_type == 'word':
                if binary_word == wc_position:
                        wc_bit = 0
                else:
                        wc_bit = 1
                #print("WC Bit:", wc_bit)
                
        ####MANUAL BIT
        manual_sum = 0
        for i in range(size_manual):
                manual_string = 'manual' + str(i)
                bit_array_manual = bin(int.from_bytes(d[manual_string], byteorder='little'))[2:].zfill(8)
                #print(bit_array_manual)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                manual_bit_temp = bit_array_manual[len(bit_array_manual)-1-manual_bits[i]]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                manual_bit_temp = int(manual_bit_temp)
                manual_sum = manual_sum + manual_bit_temp
        if manual_sum > 0:
                manual_bit = 1
        else:
                manual_bit = 0

        ####ALARM BIT
        alarm_sum = 0
        for i in range(size_alarm):
                alarm_string = 'alarm' + str(i)
                bit_array_alarm = bin(int.from_bytes(d[alarm_string], byteorder='little')).zfill(8)
                #print(bit_array_manual)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                alarm_bit_temp = bit_array_alarm[len(bit_array_alarm)-1-alarm_bits[i]]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                alarm_bit_temp = int(alarm_bit_temp)
                if i == 0:
                        if alarm_bit_temp == 0:
                                alarm_bit_temp = 1
                        else:
                                alarm_bit_temp = 0
                                
                alarm_sum = alarm_sum + alarm_bit_temp
        if alarm_sum > 0:
                alarm_bit = 1
        else:
                alarm_bit = 0
                
        return hex_word, wc_bit, manual_bit, alarm_bit

def get_reading_alarm_manual(d,size_manual,manual_bits, size_alarm, alarm_bits):
        
        ####MANUAL BIT
        
        # manual_string = 'manual0'# + str(i)
        # bit_array_manual = bin(int.from_bytes(d[manual_string], byteorder='little'))[2:].zfill(8)
        # #print(bit_array_manual)
        # #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
        # manual_bit_temp = bit_array_manual[len(bit_array_manual)-1-manual_bits[0]]
        # ########wc_bit = binary_word[len(binary_word) - 1]
        # #O bit selecionado vem como string, então convertemos para int para possibilitar operações
        # manual_bit = int(manual_bit_temp)
        
        manual_sum = 0
        for i in range(size_manual):
                manual_string = 'manual' + str(i)
                bit_array_manual = bin(int.from_bytes(d[manual_string], byteorder='little'))[2:].zfill(8)
                #print(bit_array_manual)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                manual_bit_temp = bit_array_manual[len(bit_array_manual)-1-manual_bits[i]]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                manual_bit_temp = int(manual_bit_temp)
                manual_sum = manual_sum + manual_bit_temp
                
        # string_file = './logs/alarme_teste2.log'
        # file_object = open(string_file, 'a')
        # now = datetime.now()
        # tempo =  str(now.strftime("%d/%m/%Y %H:%M:%S"))
        # m_string = manual_string + ': '+  str(manual_bit) + '|' + str(tempo)+ '\n'
        # file_object.write(m_string)
        # file_object.close()
                
        if manual_sum > 0:
                manual_bit = 1
        else:
                manual_bit = 0

        ####ALARM BIT
        alarm_sum = 0
        for i in range(size_alarm):
                alarm_string = 'alarm' + str(i)
                bit_array_alarm = bin(int.from_bytes(d[alarm_string], byteorder='little'))[2:].zfill(8)
                #print(bit_array_manual)
                #Seleciona apenas o bit menos significativo do byte lido, representa o endereço de memoria M3885.0
                alarm_bit_temp = bit_array_alarm[len(bit_array_alarm)-1-alarm_bits[i]]
                ########wc_bit = binary_word[len(binary_word) - 1]
                #O bit selecionado vem como string, então convertemos para int para possibilitar operações
                alarm_bit_temp = int(alarm_bit_temp)
                
                # string_file = './logs/alarme_teste2.log'
                # file_object = open(string_file, 'a')
                # now = datetime.now()
                # tempo =  str(now.strftime("%d/%m/%Y %H:%M:%S"))
                # a_string = alarm_string + ': '+  str(alarm_bit_temp) + '|' + str(tempo)+ '\n'
                # file_object.write(a_string)
                # file_object.close()
                
                if i == 0:
                        if alarm_bit_temp == 0:
                                alarm_bit_temp = 1
                        else:
                                alarm_bit_temp = 0
                                
                alarm_sum = alarm_sum + alarm_bit_temp
        if alarm_sum > 0:
                alarm_bit = 1
        else:
                alarm_bit = 0
                
                
        # string_file = './logs/alarme_teste2.log'
        # file_object = open(string_file, 'a')
        # t_string = '#####################\n'
        # file_object.write(t_string)
        # file_object.close()
                
        return manual_bit, alarm_bit