#import numpy as np
import pandas as pd
import requests
import simplejson as json
from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.embed import components 

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index')
def graph():
    stock = 'AAPL'

    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    session.close()

    stock_json = raw_data.json()
    stock_df = pd.DataFrame(stock_json['data'], columns=stock_json['column_names'])
    stock_df.set_index(pd.to_datetime(stock_df["Date"]), inplace=True)

    p = figure(tools='pan,box_zoom,reset,save', title='ticker symbol: %s' % stock,
           x_axis_label='date', x_axis_type='datetime')
    x = stock_df.index
    y = stock_df['Close']
    p.line(x, y, line_color = 'blue')

    script, div = components(p)
    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)

