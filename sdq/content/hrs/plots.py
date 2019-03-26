from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from flask import g
from sdq.queries.hrs import bias_counts_query, bias_gradient_query


def plot_counts(arm, name):
    source = bias_counts_query(str(g.dates['start_date']), str(g.dates['end_date']), arm)

    p = figure(name=name, plot_height=150, plot_width=200, title='Count vs time', x_axis_type='datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Count'
    p.circle(source=ColumnDataSource(source),
             x='Date', y='bias_med',
             size=15, line_alpha=0.9, fill_alpha=0.8, color=arm)

    # create the coordinates for the errorbars
    err_xs = []
    err_ys = []
    err_min = []
    err_max = []

    for x, y, yerr in zip(source['Date'], source['bias_med'], source['bias_std']):
        err_xs.append((x, x))
        err_ys.append((y - yerr, y + yerr))
        err_min.append(y - yerr)
        err_max.append(y + yerr)
    p.multi_line(err_xs, err_ys, color='black', level="underlay", line_width=1)
    p.dash(y=err_max, x=source['Date'], color='black', level="underlay", line_width=1, size=15)
    p.dash(y=err_min, x=source['Date'], color='black', level="underlay", line_width=1, size=15)

    return p


def plot_gradient(arm, gradient, name):
    source = bias_gradient_query(str(g.dates['start_date']), str(g.dates['end_date']), arm, gradient)

    p = figure(name=name, plot_height=150, plot_width=200, title='Gradient cf{gradient}'.format(gradient=gradient),
               x_axis_type='datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'bias_cf{gradient}'.format(gradient=gradient)
    p.circle(source=ColumnDataSource(source), y='bias_cf{gradient}'.format(gradient=gradient),
             x='Date', size=15, line_alpha=0.9, fill_alpha=0.8, color=arm)
    return p
