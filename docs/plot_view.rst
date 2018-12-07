Plot view methods
=================

sdq/util.py has methods that can ve used to display methods are
bokeh_plot_grid
none_bokeh_plot_grid
interact_plot_grid

Method none_/bokeh_plot_grid are only for plots that are not interactive. but on view when you click on one plot a modal
of selected plot will appear, where you can pan, zoom, select section, and save png of the plot. these plots should not
support any callback.
For method interact_plot_grid see section below for details.

Method bokeh_plot_grid
----------------------
In case you have multiple bokeh plots that you need to display you will use bokeh_plot_grid()
arguments are columns and *plots
columns define the number columns you need to have on your view. All the plots are equally spaced.
```
bokeh_plot_grid(columns=2, *plots)
will return
+----------+----------+
|plot-1    |plot-2    |
+----------+----------+
|plot-3    |plot-4    |
+----------+----------+
|plot-5    |plot-6    |
+----------+----------+

```
example code:
```
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

content = bokeh_plot_grid(
            2,
            plot('HIGH RESOLUTION', 'blue'),
            plot('HIGH RESOLUTION', 'red'),
            plot('MEDIUM RESOLUTION', 'blue'),
            plot('MEDIUM RESOLUTION', 'red'),
            plot('LOW RESOLUTION', 'blue'),
            plot('LOW RESOLUTION', 'red'),
          )

description = 'Arc waves fro HRS'
```

Method none_bokeh_plot_grid
---------------------------

In case you have multiple none bokeh plots which need to be in html for display you will use none_bokeh_plot_grid()
arguments are columns and *plots
columns define the number columns you need to have on your view. All the plots are equally spaced.
```
none_bokeh_plot_grid(columns=3, *plots)
will return
+----------+----------+----------+
|plot-1    |plot-2    |plot-3    |
+----------+----------+----------+
|plot-4    |plot-5    |plot-6    |
+----------+----------+----------+
|plot-7    |plot-8    |plot-9    |
+----------+----------+----------+

```

example code:
```
from sdq.util import none_bokeh_plot_grid


def plot(c):

    return '''
    <svg class="plot small" style="height:300px">
        <circle cx="150" cy="150" r="125" style="fill: {c}"/>
    </svg>
    '''.format(c=c)


title = 'Responsive circles'


content = none_bokeh_plot_grid(3, plot('lightgray'), plot('orange'), plot('green'), plot('pink'), plot('blue'), plot('yellow)'))

description = 'Responsive circles'
```

Method interact_plot_grid
-------------------------

These method is only for bokeh plot(s) and/or widgets. You will have to arrange your layout using any of bokeh's layouts
these plots do not have a pop up modal and they can support a call back. arguments to this method is what you need to
display anything that can be be view by bokeh show() can be displayed.

example code:
```
from bokeh.layouts import layout
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file

from sdq.util import interact_plot_grid

output_file("js_on_change.html")

x = [x*0.005 for x in range(0, 200)]
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, color='red')

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = Math.pow(x[i], f)
    }
    source.change.emit();
""")

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
slider.js_on_change('value', callback)

lay = layout([slider], [plot])

content = interact_plot_grid(lay)

description = 'Interact Plot'

```


Other views
-----------

The new data quality website can display anything but I do not encourage anyone to this.
If you have a plot in html and javaScript the plot can be displayed by setting content to be the string of that html + javaScript
