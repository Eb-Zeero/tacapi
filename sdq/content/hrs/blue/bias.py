from sdq.content.hrs.plots import plot_counts, plot_gradient
from sdq.util import bokeh_plot_grid

title = 'HRS Bias Levels'

content = bokeh_plot_grid(2,
                          plot_counts('blue', 'bias count medians'),
                          plot_gradient('blue', 'x', 'bias CFX'),
                          plot_gradient('blue', 'y', 'bias CFY')
                          )

description = 'Bias levels for HRS'
