import sqlite3
from datetime import datetime, timedelta, date
import pandas as pd
import plotly.graph_objs as go
from get_functions import get_manual_alarm, get_path

def get_figs():
    db_path, log_path = get_path()
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Calculate the date 15 days ago
    date_15_days_ago = datetime.now() - timedelta(days=15)

    # Format the date as string in SQLite format (YYYY-MM-DD)
    date_15_days_ago_str = date_15_days_ago.strftime('%Y-%m-%d')

    # Execute the SQL query with the parameter for date
    query = '''SELECT ID, ADDRESS, CLASS, DESCRIPTION, DATE_TIME
                FROM FAILURE_HIST
                WHERE DATE_TIME >= ?
                ORDER BY ID DESC'''
    data = pd.read_sql_query(query, conn, params=(date_15_days_ago_str,))

    # Calcular a data e hora atual
    current_datetime = datetime.now()
    # Calcular a data e hora de 24 horas atrás
    datetime_24_hours_ago = current_datetime - timedelta(hours=24)
    # Converter as datas para strings no formato SQLite (YYYY-MM-DD HH:MM:SS)
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    datetime_24_hours_ago_str = datetime_24_hours_ago.strftime('%Y-%m-%d %H:%M:%S')

    # Convert the 'DATE_TIME' column to datetime
    data['DATE_TIME'] = pd.to_datetime(data['DATE_TIME'])  

    last_day_data = data.query("DATE_TIME >= @datetime_24_hours_ago_str and DATE_TIME <= @current_datetime_str")

    #################################################################
    ################# FIG1 - FAILURE COUNT BY CLASS #################
    #################################################################
    # Convert the 'CLASS' column to string
    last_day_data['CLASS'] = last_day_data ['CLASS'].astype(str)

    # Count the occurrences of each class
    class_counts = last_day_data['CLASS'].value_counts()
    class_counts_sorted = class_counts.sort_index()


    if '1' not in class_counts_sorted.index:
        nova_linha = pd.Series([0], index=['1'])
        class_counts_sorted = class_counts_sorted.append(nova_linha)
    if '2' not in class_counts_sorted.index:
        nova_linha = pd.Series([0], index=['2'])
        class_counts_sorted = class_counts_sorted.append(nova_linha)
    if '3' not in class_counts_sorted.index:
        nova_linha = pd.Series([0], index=['3'])
        class_counts_sorted = class_counts_sorted.append(nova_linha)
    if '4' not in class_counts_sorted.index:
        nova_linha = pd.Series([0], index=['4'])
        class_counts_sorted = class_counts_sorted.append(nova_linha)

    print(class_counts_sorted.index)

    # Define custom colors for each class in hexadecimal format
    colors = ['#053266', '#3589a9', '#6eb8c5','#acd1c6']

    # Create a bar chart with the class counts
    fig1 = go.Figure(data=[go.Bar(x=class_counts_sorted.index, y=class_counts_sorted.values, marker=dict(color=colors))])

    # Set the chart title and axis labels
    fig1.update_layout(
                        width=700, height=370,
                        margin=dict(l=50, r=50, t=50, b=50),  # Define the left, right, top, and bottom margins
                        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
                        paper_bgcolor='#e0e5ec',
                        xaxis_title='Class', 
                        yaxis_title='Count',
                        font=dict(size=18),
                        )

    # Add text annotations for the sum above each bar
    fig1.update_traces(text=class_counts_sorted.values, textposition='auto', textfont=dict(size=18))

    #################################################################
    ################# FIG2 - FAILURE COUNT BY DESCRIPTION #################
    #################################################################
    # Convert the 'CLASS' column to string
    last_day_data['DESCRIPTION'] = last_day_data['DESCRIPTION'].astype(str)

    # Count the occurrences of each class
    description_counts = last_day_data.groupby(['DESCRIPTION', 'CLASS']).size().unstack().fillna(0)

    if '1' not in description_counts.columns:
        description_counts['1'] = 0
    if '2' not in description_counts.columns:
        description_counts['2'] = 0
    if '3' not in description_counts.columns:
        description_counts['3'] = 0
    if '4' not in description_counts.columns:
        description_counts['4'] = 0
    # Define custom colors for each class in hexadecimal format

    colors = ['#053266', '#3589a9', '#6eb8c5','#acd1c6']

    # Create a bar chart with the class counts
    fig2 = go.Figure(data=[
                            go.Bar(x=description_counts.index, 
                                    y=description_counts['1'].values, 
                                    name='CLASS 1',
                                    marker_color=colors[0]
                                    #marker=dict(color=colors)
                                    ),
                            go.Bar(x=description_counts.index, 
                                    y=description_counts['2'].values, 
                                    name='CLASS 2',
                                    marker_color=colors[1]
                                    #marker=dict(color=colors)
                                    ),
                            go.Bar(x=description_counts.index, 
                                    y=description_counts['3'].values, 
                                    name='CLASS 3',
                                    marker_color=colors[2]
                                    #marker=dict(color=colors)
                                    ),
                            go.Bar(x=description_counts.index, 
                                    y=description_counts['4'].values, 
                                    name='CLASS 4',
                                    marker_color=colors[3]
                                    #marker=dict(color=colors)
                                    ),
                            ]
                    )

    width = 30*len(description_counts)
    if width<700:
        width = 700

    # Set the chart title and axis labels
    fig2.update_layout(
                        barmode='stack',
                        width=width, height=600,
                        margin=dict(l=50, r=50, t=50, b=50),  # Define the left, right, top, and bottom margins
                        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
                        paper_bgcolor='#e0e5ec',
                        xaxis_title='Descriprion', 
                        yaxis_title='Count',
                        font=dict(size=12),
                        legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="left",
                                    x=0
                                )

                        )

    # Add text annotations for the sum above each bar
    fig2.update_traces(text=description_counts.values, textposition='auto', textfont=dict(size=18))

    # Convert the Plotly figure to JSON
    graph_json2 = fig2.to_json()

    #################################################################
    ################# FIG3 - FAILURE COUNT BY DESCRIPTION #################
    #################################################################

    data['DATE_TIME'] = pd.to_datetime(data['DATE_TIME']).dt.floor('D')

    # Agrupe os dados por data e classe e conte a quantidade de falhas
    daily_counts = data.groupby(['DATE_TIME', 'CLASS']).size().unstack().fillna(0)

    # Selecione apenas as colunas das classes
    class_columns = daily_counts.columns

    # Crie um gráfico de linhas separadas para cada classe
    fig3 = go.Figure()
    for class_name in daily_counts.columns:
        fig3.add_trace(go.Scatter(
            x=daily_counts.index,
            y=daily_counts[class_name],
            mode='markers+lines',
            name='CLASS ' + str(class_name),
            
        ))
        
        # Adicionar anotações de valores
        for i, count in enumerate(daily_counts[class_name]):
            fig3.add_annotation(
                x=daily_counts.index[i],
                y=count,
                text=int(count),
                showarrow=False,
                arrowhead=1,
                yshift=10
                
            )
            

    # Configure o layout do gráfico
    fig3.update_layout(
        width=700, height=410,
        margin=dict(l=50, r=50, t=50, b=50),  # Define the left, right, top, and bottom margins
        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
        paper_bgcolor='#e0e5ec',
        xaxis_title='Date', 
        yaxis_title='Count',
        font=dict(size=12),
        legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0
                )

        
        )   

    # Defina as cores das linhas
    colors = ['#053266', '#3589a9', '#6eb8c5','#acd1c6']  # Exemplo de cores vermelho, verde e azul
    for i, trace in enumerate(fig3.data):
        trace.marker.color = colors[i % len(colors)]
        trace.line.color = colors[i % len(colors)]

    #################################################################
    ################# FIG4 - FAILURE COUNT BY DESCRIPTION #################
    #################################################################

    data['DATE_TIME'] = pd.to_datetime(data['DATE_TIME']).dt.floor('D')


    daily_counts_old = data.groupby(['DATE_TIME', 'DESCRIPTION']).size().unstack().fillna(0)
    # Agrupe os dados por data e classe e conte a quantidade de falhas
    daily_counts = data.groupby(['DESCRIPTION', 'DATE_TIME', 'CLASS']).size().unstack().fillna(0)

    #daily_counts.to_excel('FAILURE_HIST_G1.xlsx')

    last_day_counts = daily_counts.loc[daily_counts.index.get_level_values('DATE_TIME') == daily_counts.index.get_level_values('DATE_TIME').max()]
    sum_by_description = last_day_counts.sum(axis=1)
    description_with_max_value = sum_by_description.idxmax()[0]

    desc_df = daily_counts.loc[description_with_max_value,:]
    print('############ DESC DF ###########')
    print(desc_df)
    

    leftmost_indices = daily_counts.index.get_level_values(0).unique().tolist()

    description_with_max_value_index = leftmost_indices.index(description_with_max_value)

    # Selecione apenas as colunas das classes
    class_columns = desc_df.columns.values
    class_columns_string = []
    
    print('colunas:', class_columns)
    
    # for column in class_columns:
    #     class_columns_string.append(str(column))
        
    
    # print('colunas2:', class_columns_string)
    
    # desc_df.columns = class_columns_string
        
    # # desc_df = desc_df.rename(columns = {class_columns[0]:class_columns_string[0],
    # #                                     class_columns[1]:class_columns_string[1],
    # #                                     class_columns[2]:class_columns_string[2],
    # #                                     class_columns[3]:class_columns_string[3]})
    
    print('############ DESC DF ###########')
    print(desc_df)
    
    if 1 not in desc_df.columns:
        desc_df[1] = 0.0
    if 2 not in desc_df.columns:
        desc_df[2] = 0.0
    if 3 not in desc_df.columns:
        desc_df[3] = 0.0
    if 4 not in desc_df.columns:
        desc_df[4] = 0.0

    colors = ['#053266', '#3589a9', '#6eb8c5','#acd1c6']
    
    print('############ DESC DF ###########')
    print(desc_df)
    
    print('############ DESC DF ###########')
    print(desc_df[1])
    print('############ DESC DF ###########')
    print(desc_df[2])
    print('############ DESC DF ###########')
    print(desc_df[3])
    print('############ DESC DF ###########')
    print(desc_df[4])
    

    # Crie um gráfico de linhas separadas para cada classe
    fig4 = go.Figure(data=[ go.Bar(x=desc_df.index, y=desc_df[1].values, marker_color=colors[0], visible=True, text=desc_df[1].values, textposition='auto', name='CLASSE 1'),
                            go.Bar(x=desc_df.index, y=desc_df[2].values, marker_color=colors[1], visible=True, text=desc_df[2].values, textposition='auto', name='CLASSE 2'),
                            go.Bar(x=desc_df.index, y=desc_df[3].values, marker_color=colors[2], visible=True, text=desc_df[3].values, textposition='auto', name='CLASSE 3'),
                            go.Bar(x=desc_df.index, y=desc_df[4].values, marker_color=colors[3], visible=True, text=desc_df[4].values, textposition='auto', name='CLASSE 4')])


    fig4.update_layout(
        barmode='stack',
    )

    updatemenu = []
    buttons = []

    # button with one option for each dataframe
    for desc in leftmost_indices:
        print('desc:',desc)
        new_desc_df = daily_counts.loc[desc,:]
        if 1 not in new_desc_df.columns:
            new_desc_df[1] = 0.0
        if 2 not in new_desc_df.columns:
            new_desc_df[2] = 0.0
        if 3 not in new_desc_df.columns:
            new_desc_df[3] = 0.0
        if 4 not in new_desc_df.columns:
            new_desc_df[4] = 0.0
        print(new_desc_df)
        buttons.append(dict(method='restyle',
                            label=desc,
                            visible=True,
                            args=[{'y':[new_desc_df[1].values, new_desc_df[2].values, new_desc_df[3].values, new_desc_df[4].values], 
                                'x':[new_desc_df.index,], 
                                'type':'bar',
                                'text':[new_desc_df[1].values, new_desc_df[2].values, new_desc_df[3].values, new_desc_df[4].values]},
                                ],
                            ),
                    )

    # some adjustments to the updatemenus
    updatemenu = []
    your_menu = dict()
    updatemenu.append(your_menu)

    
    updatemenu[0]['buttons'] = buttons
    updatemenu[0]['direction'] = 'down'
    updatemenu[0]['showactive'] = True
    updatemenu[0]['active'] = description_with_max_value_index
    updatemenu[0]['x'] = 0.4
    updatemenu[0]['y'] = 1.3

    # Configure o layout do gráfico
    fig4.update_layout(
        barmode='stack',
        width=700, height=410,
        margin=dict(l=50, r=50, t=50, b=50),  # Define the left, right, top, and bottom margins
        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
        paper_bgcolor='#e0e5ec',
        xaxis_title='Date', 
        yaxis_title='Count',
        font=dict(size=12),
        showlegend=True, 
        updatemenus=updatemenu,
        legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1,
                    xanchor="left",
                    x=0
                )
        )

    return fig1,fig2,fig3,fig4

def manual_alarm_figs():
    df_tuples, today_df_tuples, date_string, date_values = get_manual_alarm()
    
    df_15days = pd.DataFrame(df_tuples, columns=['Type', 'Date', 'Time'])
    
    df_filtered_alarm = df_15days[df_15days['Type'] == 'alarm start']
    # Contagem acumulada por dia
    df_filtered_alarm['Date'] = pd.to_datetime(df_filtered_alarm['Date'])
    df_filtered_alarm = df_filtered_alarm.groupby('Date').size().reset_index(name='Count')
    
    df_filtered_manual = df_15days[df_15days['Type'] == 'manual start']
    # Contagem acumulada por dia
    df_filtered_manual['Date'] = pd.to_datetime(df_filtered_manual['Date'])
    df_filtered_manual = df_filtered_manual.groupby('Date').size().reset_index(name='Count')
    
    fig1 = go.Figure(data=[go.Bar(x=df_filtered_alarm['Date'], y=df_filtered_alarm['Count'], marker_color='#053266')])
    fig2 = go.Figure(data=[go.Bar(x=df_filtered_manual['Date'], y=df_filtered_manual['Count'], marker_color='#053266')])
    
    fig1.update_layout(
                        width=360, height=170,
                        margin=dict(l=1, r=1, t=1, b=1),  # Define the left, right, top, and bottom margins
                        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
                        paper_bgcolor='#e0e5ec',
                        xaxis_title='Date', 
                        yaxis_title=' Alarm Count',
                        font=dict(size=8),
                        )
    
    fig1.update_traces(text=df_filtered_alarm['Count'], textposition='auto', textfont=dict(size=12))
    
    fig2.update_layout(
                        width=360, height=170,
                        margin=dict(l=1, r=1, t=1, b=1),  # Define the left, right, top, and bottom margins
                        plot_bgcolor='#e0e5ec',  # Change the background color of the plot
                        paper_bgcolor='#e0e5ec',
                        xaxis_title='Date', 
                        yaxis_title=' Manual Count',
                        font=dict(size=8),
                        )
    
    fig2.update_traces(text=df_filtered_manual['Count'], textposition='auto', textfont=dict(size=12))
    
    return fig1,fig2,date_values,date_string,today_df_tuples
