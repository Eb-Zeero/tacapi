from bokeh.plotting import figure
from dq_poc.util import plot_grid
from sdq.queries.hrs import arc_query


def plot(start_date, end_date, obs_mode, arm):
    source = arc_query(start_date, end_date, obs_mode, arm)

    p = figure(plot_height=1500, plot_width=2000, title=arm.upper() + ' ' + obs_mode, x_axis_label='Date',
               y_axis_label='AVG(DeltaX)', x_axis_type='datetime',)
    p.scatter(source=source, x='UTStart', y='avg', color='plasma_colors', fill_alpha=0.2, size=10)

    return p


title = 'HRS Arc Waves'

content = plot_grid(2,
                    plot('2018-07-01', '2018-08-31', 'HIGH RESOLUTION', 'blue'),
                    plot('2018-07-01', '2018-08-31', 'HIGH RESOLUTION', 'red'),
                    plot('2018-07-01', '2018-08-31', 'MEDIUM RESOLUTION', 'blue'),
                    plot('2018-07-01', '2018-08-31', 'MEDIUM RESOLUTION', 'red'),
                    plot('2018-07-01', '2018-08-31', 'LOW RESOLUTION', 'blue'),
                    plot('2018-07-01', '2018-08-31', 'LOW RESOLUTION', 'red'),

                    )

description = 'Arc waves fro HRS'
