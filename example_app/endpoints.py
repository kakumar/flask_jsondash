"""A separate Flask app that serves fake endpoints for demo purposes."""

# -*- coding: utf-8 -*-

import json
import locale
import os
from datetime import timedelta as td
from datetime import datetime as dt
from random import randrange as rr
from random import choice, random
import time

from flask import (
    Flask,
    abort,
    request,
    render_template,
)
from flask.ext.cors import CORS
from flask.ext.cors import cross_origin

app = Flask('endpoints_test')
CORS(app)
app.config['SECRET_KEY'] = 'NOTSECURELOL'
app.debug = True

STRESS_MAX_POINTS = 300

locale.setlocale(locale.LC_ALL, '')

cwd = os.getcwd()


def recursive_d3_data(current=0, max_iters=12, data=None):
    """Generate d3js data for stress testing.
    Format is suitable in treemap, circlepack and dendrogram testing.
    """
    if current >= max_iters:
        return data
    if data is None:
        data = dict(name='foo', size=rr(10, 10000), children=[])
    data = dict(name='foo', size=rr(10, 10000),
                children=[data, data])
    return recursive_d3_data(
        current=current + 1,
        max_iters=max_iters,
        data=data)


def dates_list(max_dates=10):
    """Generate a timeseries dates list."""
    now = dt.now()
    return [str(now + td(days=i * 10))[0:10] for i in range(max_dates)]


def rr_list(max_range=10):
    """Generate a list of random integers."""
    return [rr(0, 100) for i in range(max_range)]


@cross_origin()
@app.route('/combination')
def combination():
    """Fake endpoint."""
    data = {
        'columns': [
            ['data1', 30, 20, 50, 40, 60, 50],
            ['data2', 200, 130, 90, 240, 130, 220],
            ['data3', 300, 200, 160, 400, 250, 250],
            ['data4', 200, 130, 90, 240, 130, 220],
            ['data5', 130, 120, 150, 140, 160, 150],
            ['data6', 90, 70, 20, 50, 60, 120],
        ],
        'type': 'bar',
        'types': {
            'data3': 'spline',
            'data4': 'line',
            'data6': 'area',
        },
        'groups': [
            ['data1', 'data2'],
        ]
    }
    return json.dumps(dict(data=data))


@cross_origin()
@app.route('/stacked-bar')
def stackedbar():
    """Fake endpoint."""
    return json.dumps({
        'data': {
            'columns': [
                ['data1', -30, 200, 200, 400, -150, 250],
                ['data2', 130, 100, -100, 200, -150, 50],
                ['data3', -230, 200, 200, -300, 250, 250]
            ],
            'type': 'bar',
            'groups': [
                ['data1', 'data2']
            ]
        },
        'grid': {
            'y': {
                'lines': [{'value': 0}]
            }
        }
    })


@cross_origin()
@app.route('/plotly')
def plotly():
    """Fake endpoint."""
    chart_type = request.args.get('chart', 'line')
    filename = '{}/examples/plotly/{}.json'.format(cwd, chart_type)
    with open(filename, 'r') as chartjson:
        return chartjson.read()
    return json.dumps({})


@cross_origin
@app.route('/plotly-dynamic')
def plotly_dynamic():
    """Fake endpoint."""
    filename = '{}/examples/plotly/bar_line_dynamic.json'.format(cwd)
    with open(filename, 'r') as chartjson:
        return chartjson.read()
    return json.dumps({})


@cross_origin()
@app.route('/timeline')
def timeline():
    """Fake endpoint."""
    with open('{}/examples/timeline3.json'.format(cwd), 'r') as timelinejson:
        return timelinejson.read()
    return json.dumps({})


@app.route('/dtable', methods=['GET'])
def dtable():
    """Fake endpoint."""
    if 'stress' in request.args:
        return json.dumps([
            dict(
                foo=rr(1, 1000),
                bar=rr(1, 1000),
                baz=rr(1, 1000),
                quux=rr(1, 1000)) for _ in range(STRESS_MAX_POINTS)
        ])
    fname = 'dtable-override' if 'override' in request.args else 'dtable'
    with open('{}/examples/{}.json'.format(os.getcwd(), fname), 'r') as djson:
        return djson.read()
    return json.dumps({})


@cross_origin()
@app.route('/timeseries')
def timeseries():
    """Fake endpoint."""
    return json.dumps({
        "dates": dates_list(),
        "line1": rr_list(max_range=10),
        "line2": rr_list(max_range=10),
        "line3": rr_list(max_range=10),
    })


@cross_origin()
@app.route('/custom')
def custompage():
    """Fake endpoint."""
    kwargs = dict(number=rr(1, 1000))
    return render_template('examples/custom.html', **kwargs)


@cross_origin()
@app.route('/gauge')
def gauge():
    """Fake endpoint."""
    return json.dumps({'data': rr(1, 100)})


@cross_origin()
@app.route('/area-custom')
def area_custom():
    """Fake endpoint."""
    return json.dumps({
        "data": {
            "columns": [
                ["data1", 300, 350, 300, 0, 0, 0],
                ["data2", 130, 100, 140, 200, 150, 50]
            ],
            "types": {
                "data1": "area",
                "data2": "area-spline"
            }
        }
    })


@cross_origin()
@app.route('/scatter')
def scatter():
    """Fake endpoint."""
    if 'override' in request.args:
        with open('{}/examples/overrides.json'.format(cwd), 'r') as jsonfile:
            return jsonfile.read()
    return json.dumps({
        "bar1": [1, 2, 30, 12, 100],
        "bar2": rr_list(max_range=40),
        "bar3": rr_list(max_range=40),
        "bar4": [-10, 1, 5, 4, 10, 20],
    })


@cross_origin()
@app.route('/pie')
def pie():
    """Fake endpoint."""
    letters = list('abcde')
    if 'stress' in request.args:
        letters = range(STRESS_MAX_POINTS)
    return json.dumps({'data {}'.format(name): rr(1, 100) for name in letters})


@cross_origin()
@app.route('/custom-inputs')
def custom_inputs():
    """Fake endpoint."""
    _range = int(request.args.get('range', 5))
    entries = int(request.args.get('entries', 3))
    starting = int(request.args.get('starting_num', 0))
    prefix = request.args.get('prefix', 'item')
    if 'override' in request.args:
        show_axes = request.args.get('show_axes', False)
        show_axes = show_axes == 'on'
        data = dict(
            data=dict(
                columns=[
                    ['{} {}'.format(prefix, i)] + rr_list(max_range=entries)
                    for i in range(starting, _range)
                ],
            )
        )
        if show_axes:
            data.update(axis=dict(
                x=dict(label='This is the X axis'),
                y=dict(label='This is the Y axis')))
        return json.dumps(data)
    return json.dumps({
        i: rr_list(max_range=_range) for i in range(starting, entries)
    })


@cross_origin()
@app.route('/bar')
def barchart():
    """Fake endpoint."""
    if 'stress' in request.args:
        return json.dumps({
            'bar-{}'.format(k): rr_list(max_range=STRESS_MAX_POINTS)
            for k in range(STRESS_MAX_POINTS)
        })
    return json.dumps({
        "bar1": [1, 2, 30, 12, 100],
        "bar2": rr_list(max_range=5),
        "bar3": rr_list(max_range=5),
    })


@cross_origin()
@app.route('/line')
def linechart():
    """Fake endpoint."""
    if 'stress' in request.args:
        return json.dumps({
            'bar-{}'.format(k): rr_list(max_range=STRESS_MAX_POINTS)
            for k in range(STRESS_MAX_POINTS)
        })
    return json.dumps({
        "line1": [1, 4, 3, 10, 12, 14, 18, 10],
        "line2": [1, 2, 10, 20, 30, 6, 10, 12, 18, 2],
        "line3": rr_list(),
    })


@cross_origin()
@app.route('/singlenum')
def singlenum():
    """Fake endpoint."""
    _min, _max = 10, 10000
    if 'sales' in request.args:
        val = locale.currency(float(rr(_min, _max)), grouping=True)
    else:
        val = rr(_min, _max)
    if 'negative' in request.args:
        val = '-{}'.format(val)
    return json.dumps(val)


@cross_origin()
@app.route('/deadend')
def test_die():
    """Fake endpoint that ends in a random 50x error."""
    # Simulate slow connection
    time.sleep(random())
    abort(choice([500, 501, 502, 503, 504]))


@cross_origin()
@app.route('/venn')
def test_venn():
    """Fake endpoint."""
    data = [
        {'sets': ['A'], 'size': rr(10, 100)},
        {'sets': ['B'], 'size': rr(10, 100)},
        {'sets': ['C'], 'size': rr(10, 100)},
        {'sets': ['A', 'B'], 'size': rr(10, 100)},
        {'sets': ['A', 'B', 'C'], 'size': rr(10, 100)},
    ]
    return json.dumps(data)


@cross_origin()
@app.route('/sparklines', methods=['GET'])
def sparklines():
    """Fake endpoint."""
    if any([
        'pie' in request.args,
        'discrete' in request.args,
    ]):
        return json.dumps([rr(1, 100) for _ in range(10)])
    return json.dumps([[i, rr(i, 100)] for i in range(10)])


@cross_origin()
@app.route('/circlepack', methods=['GET'])
def circlepack():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return json.dumps(recursive_d3_data())
    with open('{}/examples/flare.json'.format(cwd), 'r') as djson:
        return djson.read()
    return json.dumps({})


@cross_origin()
@app.route('/treemap', methods=['GET'])
def treemap():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return json.dumps(recursive_d3_data())
    with open('{}/examples/flare.json'.format(cwd), 'r') as djson:
        return djson.read()
    return json.dumps({})


@cross_origin()
@app.route('/map', methods=['GET'])
def datamap():
    """Fake endpoint."""
    return render_template('examples/map.html')


@cross_origin()
@app.route('/dendrogram', methods=['GET'])
def dendro():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return json.dumps(recursive_d3_data())
    filename = 'flare-simple' if 'simple' in request.args else 'flare'
    with open('{}/examples/{}.json'.format(cwd, filename), 'r') as djson:
        return djson.read()
    return json.dumps({})


@cross_origin()
@app.route('/voronoi', methods=['GET'])
def voronoi():
    """Fake endpoint."""
    w, h = request.args.get('width', 800), request.args.get('height', 800)
    max_points = int(request.args.get('points', 100))
    if 'stress' in request.args:
        max_points = 500
    return json.dumps([[rr(1, h), rr(1, w)] for _ in range(max_points)])


@cross_origin()
@app.route('/digraph', methods=['GET'])
def graphdata():
    """Fake endpoint."""
    if 'simple' in request.args:
        graphdata = """
        digraph {
            a -> b;
            a -> c;
            b -> c;
            b -> a;
            b -> b;
        }
        """
        return json.dumps(dict(graph=graphdata))
    nodes = list('abcdefghijkl')
    node_data = '\n'.join([
        '{0} -> {1};'.format(choice(nodes), choice(nodes))
        for _ in range(10)
    ])
    graphdata = """digraph {lb} {nodes} {rb}""".format(
        lb='{', rb='}', nodes=node_data)
    return json.dumps(dict(
        graph=graphdata,
    ))


if __name__ == '__main__':
    app.run(debug=True, port=5004)
