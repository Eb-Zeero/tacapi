from bokeh.plotting import figure
from flask import g
from sdq.util import bokeh_plot_grid
from sdq.queries.hrs import arc_query


def plot(obs_mode, arm):
    source = arc_query(str(g.dates['start_date']), str(g.dates['end_date']), obs_mode, arm)

    p = figure(plot_height=150, plot_width=200, title=arm.upper() + ' ' + obs_mode, x_axis_label='Date',
               y_axis_label='AVG(DeltaX)', x_axis_type='datetime',)
    p.scatter(source=source, x='UTStart', y='avg', color='plasma_colors', fill_alpha=0.2, size=10)

    return p


title = 'HRS Arc Waves'

content = bokeh_plot_grid(2,
                          plot('HIGH RESOLUTION', 'blue'),
                          plot('HIGH RESOLUTION', 'red'),
                          plot('MEDIUM RESOLUTION', 'blue'),
                          plot('MEDIUM RESOLUTION', 'red'),
                          plot('LOW RESOLUTION', 'blue'),
                          plot('LOW RESOLUTION', 'red'),
                          )

description = 'Arc waves fro HRS'
