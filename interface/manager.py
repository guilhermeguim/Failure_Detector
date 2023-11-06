import subprocess
import os
import datetime

class SubprocessManager:
    def __init__(self):
        self.process_analisys = None
        self.running_analisys = 0
        self.process_training = None
        self.running_training = 0
        self.curr_path = self.get_curr_path()
        self.trained = self.check_xlsx()
        
        
    def set_running_analisys(self, value):
        self.running_analisys = value
        
    def set_running_training(self, value):
        self.running_training = value
        
    def get_process_training_status(self):
        self.check_xlsx()
        return self.running_training 
    
    def get_trained_status(self):
        self.check_xlsx()
        return self.trained

    def get_process_analisys_status(self):
        self.check_xlsx()
        return self.running_analisys 
    
    def start_analisys(self):
        self.stop_analisys()
        self.check_xlsx()
        if self.trained == 1:
            self.stop_training()
            command = 'lxterminal -e python3 ' +  self.curr_path + 'main_fsm.py'
            self.process_analisys = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            proc_analisys_pid = self.process_analisys.pid
            print('PID: ', proc_analisys_pid)
        else: 
            print("Não está treinado")

    def stop_analisys(self):
        self.check_xlsx()
        if self.process_analisys  is not None:
            command = "pkill -f 'python3 " +  self.curr_path + "main_fsm.py'"
            subprocess.Popen(command, shell=True)
            self.process_analisys  = None
            print("Analise encerrada com sucesso")
        else:
            print("Nenhuma analise em execução")
            

    def start_training(self, time):
        self.check_xlsx()
        self.stop_training()
        self.stop_analisys()
        command = 'lxterminal -e python3 ' +  self.curr_path + 'get_input.py ' + str(time)
        self.process_training = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        proc_training_pid = self.process_training.pid
        print('PID: ', proc_training_pid)


    def stop_training(self):
        self.check_xlsx()
        if self.process_training  is not None:
            command = "pkill -f 'python3 " +  self.curr_path + "get_input.py'"
            subprocess.Popen(command, shell=True)
            self.process_training  = None
            print("Treinamento encerrado com sucesso")
        else:
            print("Nenhum treinamento em execução")
            
    def check_xlsx(self):
        
        directory =  self.curr_path + 'datasets/training'
        # loop through all files in the directory
        for file in os.listdir(directory):
            # check if the file extension is .xlsx
            if file.endswith(".xlsx"):
                # return 1 if found
                self.trained = 1
                return 1
        # return 0 if not found
        self.trained = 0
        return 0 
    
    def get_curr_path(self):
        curr_path = os.path.dirname (os.path.abspath (__file__))
        curr_path = curr_path.replace('\\', '/')  # Substitui as barras invertidas por barras normais
        curr_path = curr_path.replace('interface', '')
        return curr_path
    

