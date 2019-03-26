from sdq.content.hrs.plots import plot_counts, plot_gradient
from sdq.util import bokeh_plot_grid

content = bokeh_plot_grid(2,
                          plot_counts('red', 'bias count medians'),
                          plot_gradient('red', 'x', 'bias CFX'),
                          plot_gradient('red', 'y', 'bias CFY')
                          )

description = 'Bias levels for HRS'
