from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import sqlite3
import pandas as pd
import os
import subprocess
import requests
import datetime

from manager import SubprocessManager
from get_functions import get_path, get_data_hist, get_manual_alarm, clean_directory, get_directory_size_xlsx, get_curr_path
from manage_db import add_parameter, edit_parameter, edit_general_parameters
from graphs import get_figs, manual_alarm_figs

from time import sleep
from threading import Thread
from multiprocessing import Process

import webbrowser
import pyautogui

server = Flask(__name__)
server.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(server)


# Create a new SubprocessManager
manager = SubprocessManager()

@server.route("/")
def history():
    #pyautogui.press('f11')
    # Get the Failure History table filtered by class == 1
    data = get_data_hist(1)
    # Render the template with the rows
    return render_template("history.html" ,data=data)

@server.route('/newdata', methods=['GET'])
def newdata():
    class_value = request.args.get('class_value', default=None, type=int)  # Get the selected CLASS value from the request parameters
    data = get_data_hist(class_value)    
    return jsonify(result=data)

@server.route("/add", methods=["GET", "POST"])
def add():
    # SAVE ON FORM SUBMIT
    if request.method == "POST":
        add_parameter()
    # RENDER PAGE
    return render_template("add.html")

@server.route("/edit")
def edit():
    # Connect to the database
    db_path, log_path = get_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM PARAMETERS')
    data = cur.fetchall()
    conn.close()

    return render_template("edit.html", data=data)

@server.route('/editing/<int:id>/<string:name>/<int:pattern>', methods=["GET", "POST"])
def edit_record(id,name,pattern):
    # SAVE ON FORM SUBMIT
    db_path, log_path = get_path()
    if request.method == "POST":
        edit_parameter(id,name,pattern,db_path)
    # RENDER PAGE
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM PARAMETERS WHERE id=?', (id,))
    record = cur.fetchone()
    conn.close()
    return render_template('editing.html', record=record)

@server.route('/delete/<int:id>')
def delete_record(id):
    db_path, log_path = get_path()
    connection = sqlite3.connect(db_path)
    
    delete = '''
            DELETE FROM PARAMETERS
            WHERE ID = ?
            '''
    
    connection.execute(delete,(id,))
        
    connection.commit()
    
    cur = connection.cursor()
    cur.execute('SELECT * FROM PARAMETERS')
    data = cur.fetchall()
    connection.close()
    return render_template("edit.html", data=data)

@server.route("/run")
def run():
    status_analisys = manager.get_process_analisys_status()
    status_training = manager.get_process_training_status()
    print('an: ', status_analisys)
    print('tr: ', status_training)
    trained = manager.get_trained_status()
    return render_template("run.html", status_analisys = status_analisys, status_training = status_training, trained = trained)

@server.route('/run_analisys', methods=['POST'])
def run_analisys():
    if request.method == "POST":
        count = get_directory_size_xlsx()
        if count > 2:
            clean_directory()
        manager.start_analisys()
        status_analisys = manager.get_process_analisys_status()
        status_training = manager.get_process_training_status()
        trained = manager.get_trained_status()
        return render_template("run.html", status_analisys = status_analisys, status_training = status_training, trained = trained)


@server.route('/stop_analisys', methods=['POST'])
def stop_analisys():
    if request.method == "POST":
        manager.stop_analisys()
        status_analisys = manager.get_process_analisys_status()
        status_training = manager.get_process_training_status()
        trained = manager.get_trained_status()
        return render_template("run.html", status_analisys = status_analisys, status_training = status_training, trained = trained)


@server.route('/run_training', methods=['POST'])
def run_training():
    if request.method == "POST":
        time = request.values.get("time")

        manager.start_training(time)
        status_analisys = manager.get_process_analisys_status()
        status_training = manager.get_process_training_status()
        trained = manager.get_trained_status()
        return render_template("run.html", status_analisys = status_analisys, status_training = status_training, trained = trained)


@server.route('/stop_training', methods=['POST'])
def stop_training():
    if request.method == "POST":
        manager.stop_training()
        status_analisys = manager.get_process_analisys_status()
        status_training = manager.get_process_training_status()
        clean_directory()
        trained = manager.get_trained_status()
        return render_template("run.html", status_analisys = status_analisys, status_training = status_training, trained = trained)


@server.route("/general_edit", methods=["GET", "POST"])
def general_edit():
    db_path, log_path = get_path()
    # SAVE ON FORM SUBMIT
    if request.method == "POST":
        edit_general_parameters(db_path)
    # RENDER PAGE
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM GENERAL_PARAMETERS')
    record = cur.fetchone()
    conn.close()
    print(record)
    return render_template('general_edit.html', record=record)

@server.route("/dashboard")
#menção honrosa -> https://stackoverflow.com/questions/59406167/plotly-how-to-filter-a-pandas-dataframe-using-a-dropdown-menu
def dashboard():
    fig1,fig2,fig3,fig4 = get_figs()
    # Convert the Plotly figure to JSON
    graph_json1 = fig1.to_json()
    graph_json2 = fig2.to_json()
    graph_json3 = fig3.to_json()
    graph_json4 = fig4.to_json()
    
    return render_template("dashboard.html", graph_json1=graph_json1, graph_json2=graph_json2, graph_json3=graph_json3, graph_json4=graph_json4)#, graph_json4=graph_json4)

@server.route("/manual_alarm_hist")
def manual_alarm_hist():
    fig1,fig2,date_values,date_string,today_df_tuples = manual_alarm_figs()
        
    graph_json1 = fig1.to_json()
    graph_json2 = fig2.to_json()
        
    return render_template("manual_alarm_hist.html", date_values=date_values, today=date_string, graph_json1=graph_json1, graph_json2=graph_json2)

@server.route('/newdata_manual_alarm', methods=['GET'])
def newdata_manual_alarm():
    fig1,fig2,date_values,date_string,today_df_tuples = manual_alarm_figs()
    
    graph_json1 = fig1.to_json()
    graph_json2 = fig2.to_json()
        
    return jsonify(result=today_df_tuples, graph_json1=graph_json1, graph_json2=graph_json2)


def open_browser():
    subprocess.call(["pkill", "chromium"])
    sleep(5)
    # define the url to open
    url = "http://127.0.0.1:5000"
    if not webbrowser.open_new_tab(url):
        # Se a URL já está aberta, abre uma nova aba com a URL
        webbrowser.open_new(url)
    sleep(2)
    pyautogui.press('f11')
        
def run_main():
    manager.start_analisys()


def checker_status():
    while True:
        try:
            sleep(3)
            # Abre o arquivo.log em modo de leitura
            path = get_curr_path()
            path1 = path + 'logs/analisys.log'
            with open(path1, "r") as f:
                # Lê a primeira linha do arquivo
                linha = f.readline()
                # Converte a string em um objeto datetime
                data_hora_arquivo = datetime.datetime.strptime(linha, "%Y/%m/%d %H:%M:%S.%f")
                # Obtém a data e hora atual
                agora = datetime.datetime.now()
                # Calcula a diferença entre as duas datas e horas em segundos
                diferenca = abs((agora - data_hora_arquivo).total_seconds())
                # Verifica se a diferença está dentro do intervalo de 10 segundos
                if diferenca <= 5:
                    print("A analise está rodando")
                    mensagem1 = 1
                else:
                    print("A analise parou")
                    mensagem1 = 0
            path2 = path + 'logs/training.log'
            with open(path2, "r") as f:
                # Lê a primeira linha do arquivo
                linha = f.readline()
                # Converte a string em um objeto datetime
                data_hora_arquivo = datetime.datetime.strptime(linha, "%Y/%m/%d %H:%M:%S.%f")
                # Obtém a data e hora atual
                agora = datetime.datetime.now()
                # Calcula a diferença entre as duas datas e horas em segundos
                diferenca = abs((agora - data_hora_arquivo).total_seconds())
                # Verifica se a diferença está dentro do intervalo de 10 segundos
                if diferenca <= 5:
                    print("O treinamento está rodando")
                    mensagem2 = 1
                else:
                    print("O treinamento parou")
                    mensagem2 = 0
                
            data = {'analisys_value': mensagem1,
                    'training_value': mensagem2}

            response = requests.post('http://localhost:5000/message', json=data)
            if response.status_code == 200:
                pass
                    #print('Mensagem enviada com sucesso')
            else:
                print('Erro ao enviar mensagem')
        except:
            print('####################')
            print('Falhei na leitura do status')
            print('####################')

@server.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()

    status_an  = data.get('analisys_value')
    status_tr  = data.get('training_value')
    
    last_status_an = manager.get_process_analisys_status()
    last_status_tr = manager.get_process_training_status()
    
    if status_an != last_status_an:

        manager.set_running_analisys(int(status_an))
        data = {
        'status_analisys': manager.get_process_analisys_status(),
        'status_training': manager.get_process_training_status()
        }
        socketio.emit('update_data', data)
        return render_template("run.html", status_analisys = manager.get_process_analisys_status(), status_training = manager.get_process_training_status(), trained = manager.get_trained_status())
        
    if status_tr != last_status_tr:

        manager.set_running_training(int(status_tr))
        data = {
        'status_analisys': manager.get_process_analisys_status(),
        'status_training': manager.get_process_training_status()
        }
        socketio.emit('update_data', data)
        return render_template("run.html", status_analisys = manager.get_process_analisys_status(), status_training = manager.get_process_training_status(), trained = manager.get_trained_status())

    print('Mensagem recebida:',status_an,status_tr)
    
    return 'OK'

if __name__ == "__main__":
    t_check = Thread(target=checker_status)
    t_check.start()
    run_main()
    
    t_screen = Thread(target=open_browser)
    t_screen.start()
    
    socketio.run(server)
    

