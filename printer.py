def print_log(string_log, t_num, curr_path):
    print(string_log)
    
    string_file = curr_path + 'logs/' + str(t_num)+ '.log'
    file_object = open(string_file, 'a')
    file_object.write(string_log)
    file_object.close()