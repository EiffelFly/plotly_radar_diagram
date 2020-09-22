
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from io import StringIO
import csv
import os
import plotly.io as pio
import plotly

# remove sensitive data
theta = ['a','b','c','d','e','f','g','h','i','j','k']

groupby_customer_mean_result = {}
data_for_plotly = {}

# calculate the data of every company
with open('rhymebus_customer_data_test.csv', encoding="big5", newline='') as target_file:
    target_csv = csv.reader(target_file, delimiter=' ', quotechar='|')
    df = pd.read_csv(
        target_file,
        header=0,
        usecols= ['a','b','c','d','e','f','g','h','i','j']
    )

    #calculate mean 
    groupby_customer_mean = df.groupby('顧客名').mean()
    groupby_customer_mean = groupby_customer_mean.drop('年份',axis=1)

    for index, row in groupby_customer_mean.iterrows():
        row_mean_list = row.astype('int').tolist()
        row_mean_list.append(row_mean_list[0]) # compensate that the line of polar chart can enclose.
        groupby_customer_mean_result.update({f'{index}':row_mean_list})

    # rearrange the data for further usage
    for index, row in df.iterrows():
        area = row['區域']
        customer = row['顧客名']
        year = row['年份']

        row = row.drop(['區域','顧客名','年份'], axis=0)
        row_list = row.astype('int').tolist()
        row_list.append(row_list[0])

        data = {
            'year':year,
            'customer':customer,
            'area':area,
            'data':row_list
        }

        data_for_plotly.update({f'{year}年-{area}-{customer}':data})

# using plotly to draw the radar diagram
for key, value in data_for_plotly.items():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = value['data'],
        theta=theta,
        mode = 'markers+lines',
        marker = dict(color='#000088', size = 10, line = dict(width = 1)),    
    ))

    customer = value['customer']
    year = value['year']

    fig.add_trace(go.Scatterpolar(
        r = groupby_customer_mean_result[f'{customer}'],
        theta=theta,
        mode = 'markers+lines',
        marker = dict(color='#ffa500', size = 10, line = dict(width = 1)),
    ))

    fig.update_layout(
        title = f'{year}年 {customer} 顧客滿意度',
        title_font_size = 30,
        autosize=False,
        width=400,
        height=400,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[5,10],
                showline = True,
                linecolor='#d0d0d0',
                linewidth = 5,
                gridcolor='#d0d0d0',
                layer = "below traces",
                rangemode = 'normal',
                tickmode = 'linear',
                tick0 = 5,
                dtick = 1,
                tickfont = dict(
                    size = 15
                ),

            ),     
            angularaxis = dict(
                gridcolor='#d0d0d0',
                direction = 'clockwise',
                tickfont = dict(
                    size = 25
                )
            ),
        ),
        showlegend=True,
    )

    # plotly orca will usually encounter some environment variable error
    # recommend directly download release zip file and execute the setup.exe
    # https://github.com/plotly/orca
    # then follow the tutorial of Method 4: Standalone binaries

    # this line is especially for windows:
    # after manually install orca in your system and settign up system environment variable 
    # you can get this path on desktop orca shortcut's properity-start in
    plotly.io.orca.config.executable = 'C:\\Users\\Eiffel\\AppData\\Local\\Programs\\orca\\orca.exe'

    fig.write_image(f"images/{year}-{customer}.jpeg", engine='orca', format='jpeg', width=1200 , height=800)

    # config 
    # print(pio.orca.config.plotlyjs)
    # print(pio.orca.config)
    # print(pio.orca.status)
    # path = os.path.dirname(os.path.abspath(__file__))
    # print(path)
