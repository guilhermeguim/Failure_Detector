from snap7.types import *
import os

def find_area(start_list, total_size_list, start_byte):
        for i in range(len(start_list)):
                start = start_list[i]
                size = total_size_list[i]
                if start_byte >= start and start_byte < (start+size):
                        return start, size

def calcula_bit(string_address,start,size):
        
        if string_address == 'null':
                bit_to_del = []
                return bit_to_del
        
        if string_address[len(string_address)-1] == ',':
                string_address = string_address[:-1]
                
        string_address = string_address.replace(' ','') 
        address_list = string_address.split(',')
        
        bit_to_del = []

        for address in address_list:
                address_divided = address.split('.')
                to_del = ((start + size-1-int(address_divided[0]))*8) + 7 - int(address_divided[1]) 
                bit_to_del.append(to_del)
                        
        return bit_to_del

def calcula_bit_wc(wc_address,wc_external, wc_position):
        
        bit_pos = ((wc_external - wc_address)*8)+wc_position
                        
        return bit_pos

def to_list(string_address):
        
        if string_address == 'null':
                bit_to_del = []
                return bit_to_del
        
        if string_address[len(string_address)-1] == ',':
                string_address = string_address[:-1]
                
        string_address = string_address.replace(' ','') 
        address_list = string_address.split(',')
        
        listed = []
        
        for address in address_list:
                if str(address).upper() == 'MEMORY':
                        listed.append(Areas.MK)
                elif str(address).upper() == 'INPUT':
                        listed.append(Areas.PE)
                else:
                        listed.append(int(address))
                
        return listed

def get_curr_path():
    curr_path = os.path.dirname (os.path.abspath (__file__))
    curr_path = curr_path.replace('\\', '/')  # Substitui as barras invertidas por barras normais
    curr_path = curr_path + '/'
    return curr_path

if __name__ == '__main__':
        print(get_curr_path())