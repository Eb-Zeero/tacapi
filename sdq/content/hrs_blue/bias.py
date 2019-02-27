from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure
from flask import g
from sdq.queries.hrs import bias_counts_query, bias_gradient_query
from sdq.util import bokeh_plot_grid


def plot_counts(arm):
    source = bias_counts_query(str(g.dates['start_date']), str(g.dates['end_date']), arm)
    print(source)

    p = figure(plot_height=150, plot_width=200, title='Count vs time', x_axis_type='datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Count'
    p.circle(source=ColumnDataSource(source),
             x='Date', y='bias_med',
             size=15, line_alpha=0.9, fill_alpha=0.8, color='blue')

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


def plot_gradient(arm, gradient):
    source = bias_gradient_query(str(g.dates['start_date']), str(g.dates['end_date']), arm, gradient)

    p = figure(plot_height=150, plot_width=200, title='Gradient cf{gradient}'.format(gradient=gradient),
               x_axis_type='datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'bias_cf{gradient}'.format(gradient=gradient)
    p.circle(source=ColumnDataSource(source), y='bias_cf{gradient}'.format(gradient=gradient),
             x='Date', size=15, line_alpha=0.9, fill_alpha=0.8, color='blue')
    return p


title = 'HRS Bias Levels'

content = bokeh_plot_grid(2,
                          plot_counts('blue'),
                          plot_gradient('blue', 'z'),
                          plot_gradient('blue', 'x'),
                          plot_gradient('blue', 'y')
                          )

description = 'Bias levels for HRS'
