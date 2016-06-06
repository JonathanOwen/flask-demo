"""
import numpy as np
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
"""
import numpy as np
import pandas as pd
import requests
import simplejson as json
from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.embed import components 

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('select_stock.html')
    else:
        app.vars['stock'] = request.form['ticker_symbol']
        return redirect('/graph')

@app.route('/graph')
def graph():
    stock = app.vars['stock']
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    session.close()

    stock_json = raw_data.json()
    try:
        stock_df = pd.DataFrame(stock_json['data'], columns=stock_json['column_names'])
    except:
        return redirect('/no_stock')
    stock_df.set_index(pd.to_datetime(stock_df["Date"]), inplace=True)

    p = figure(tools='pan,box_zoom,reset,save', title='ticker symbol: %s' % stock,
           x_axis_label='date', x_axis_type='datetime')
    x = stock_df.index
    y = stock_df['Close']
    p.line(x, y, line_color = 'blue')

    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

@app.route('/no_stock', methods=['GET','POST'])
def no_stock():
    if request.method == 'GET':
        return render_template('no_stock.html')
    else:
        return redirect('/index')

if __name__ == '__main__':
    app.run(port=33507)

