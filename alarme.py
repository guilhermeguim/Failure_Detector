from snap7.util import *
from snap7.types import *
from read import get_reading_alarm_manual
from calculate_parameters import get_curr_path
#from gpiozero import CPUTemperature


def read_alarm(d,size_manual,manual_bits, size_alarm, alarm_bits,curr_path):#DATA READING

    first1 = 1
    first2 = 1 
    
    while True:
        
        manual_bit, alarm_bit = get_reading_alarm_manual(d,size_manual,manual_bits, size_alarm, alarm_bits)

        if manual_bit == 1:
            #print('entrei manual')
            if first2 == 1:
                tipo = 'manual start'
                now = datetime.now()
                tempo =  str(now.strftime("%Y/%m/%d %H:%M:%S"))
                
                string_log = str(tipo) + ': ' + str(tempo) + '\n'
                print(string_log)
                
                string_file = curr_path + 'logs/alarm.log'
                file_object = open(string_file, 'a')
                file_object.write(string_log)
                file_object.close()
            first2 = 0
        if manual_bit == 0:
            #print('sai manual')
            if first2 == 0:
                tipo = 'manual end'
                now = datetime.now()
                tempo =  str(now.strftime("%Y/%m/%d %H:%M:%S"))
                
                string_log = str(tipo) + ': ' + str(tempo) + '\n'
                print(string_log)
                
                string_file = curr_path + 'logs/alarm.log'
                file_object = open(string_file, 'a')
                file_object.write(string_log)
                file_object.close()
                
            first2 = 1
        ######################################################
        
        
        if alarm_bit == 1:
            if first1 == 1:
                tipo = 'alarm start'
                now = datetime.now()
                tempo =  str(now.strftime("%Y/%m/%d %H:%M:%S"))
                
                string_log = str(tipo) + ': ' + str(tempo) + '\n'
                print(string_log)
                
                string_file = curr_path + 'logs/alarm.log'
                file_object = open(string_file, 'a')
                file_object.write(string_log)
                file_object.close()
            first1 = 0
        if alarm_bit == 0:
            if first1 == 0:
                tipo = 'alarm end'
                now = datetime.now()
                tempo =  str(now.strftime("%Y/%m/%d %H:%M:%S"))
                
                string_log = str(tipo) + ': ' + str(tempo) + '\n'
                print(string_log)
                
                string_file = curr_path + 'logs/alarm.log'
                file_object = open(string_file, 'a')
                file_object.write(string_log)
                file_object.close()
                
            first1 = 1
