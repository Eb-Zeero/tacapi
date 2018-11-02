from bokeh.plotting import figure
from sdq.util import none_bokeh_plot_grid
from sdq.queries.hrs import arc_query


def plot(c):

    return '''
    <svg class="plot small" style="height:300px">
        <circle cx="150" cy="150" r="125" style="fill: {c}"/>
    </svg>
    '''.format(c=c)


title = 'HRS Arc Waves'


content = none_bokeh_plot_grid(3, plot('lightgray'), plot('orange'), plot('green'), plot('pink'), plot('blue'), plot('yellow)'))

description = 'Arc waves fro HRS'
