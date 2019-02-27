Adding a plot
=============

We will go through a made up example of adding a instrument BVIT to the data quality plot.

Step one Preparation
--------------------
scripts
-------
we need to add directory `bvit/` to the `sdq/content/` dir. this mean we will have `sdq/content/bvit/`.

In the root of `bvit` we can now add the plots that we want.
Assuming we need to add `arcs`, `flats` and `bias` for `bvit` we will have to create three python scrips for each
each script should contain variables
```
    title = 'Plot title'  #  Must have
    content = 'Plot html and javaScript'  #  Must have
    description = 'Plot description'  #  Optional

```
`content` will be explained later.

At the end we will have `sdq/content/bvit/arcs.py`, `sdq/content/bvit/bias.py` and `sdq/content/bvit/flats.py`
each containing above variables.

data
----
For code organisation, all query will be stored in `sdq/queries/`
we acn add `bvit.py` in `sdq/queries/` the we have `sdq/queries/bvit.py`
with an assumption that we have table `bvit` in `sdb` looking like
```
+--------------+----------+---------------+--------------+--------------+
| date         |arc       |flats          |bias          |color         |
+--------------+----------+---------------+--------------+--------------+
| 11-12-2018   |56        | 50            |133           | red          |
+--------------+----------+---------------+--------------+--------------+
| 12-12-2018   |46        | 70            |100           | green        |
+--------------+----------+---------------+--------------+--------------+
|                                   ...                                 |
+--------------+----------+---------------+--------------+--------------+
| 31-12-2018   |33        | 72            |120           |  blue        |
+--------------+----------+---------------+--------------+--------------+
```
And on each we need to plot date over value.
then `sdq/queries/bvit.py`:
```
import pandas as pd
from bokeh.plotting import ColumnDataSource

from sdq.sdb_connection import sdb_connect


def bvit_query(start_date, end_date, column, color):
    #  query to get data
    sql = "SELECT Date, {column} FROM bvit  WHERE date BETWEEN '{start_date}' AND '{end_date}' AND color={color}" \
        .format(start_date=start_date, end_date=end_date, column=column)

    #  use pandas read_sql read run query in sdb  and store results in a data frame
    df = pd.read_sql(sql, sdb_connect())

    # create bokeh ColumnDataSource form pandas data frame
    source = ColumnDataSource(df)

    # return results
    return source
```
Creating content
----------------

File `sdq/content/bvit/arcs.py` should look like:

```
from sdq.queries.bvit import bvit_query


def plot(column, color):
    source = bvit_query(str(g.dates['start_date']), str(g.dates['end_date']), column, color)

    p = figure(plot_height=150, plot_width=200, x_axis_label='Date', y_axis_label='Value', x_axis_type='datetime')

    p.scatter(source=source, x='date', y=column, fill_alpha=0.2, size=10)

    return p

title = 'BVIT Arc Waves'

content = bokeh_plot_grid(2,
             plot('arcs', 'red'),
             plot('arcs', 'green'),
             plot('arcs', 'blue'),
             plot('arcs', 'uv'),
             plot('arcs', 'xray')
             )

description = 'Arc waves for BVIT on different colors'
```

side/secondary menu
-------------------
Each menu is described by a list of tuples containing the title to use in the menu, the slug to use in the URL and the
module for the page content.
You can create a new one or add it to th existing one.
To add one:
On file `sdq\menus.py` add a secondary menu before using it
```python
    ...
    _hrs_menu = (
        ('Diagnostic', 'diagnostics', 'sdq.content.hrs.diagnostics'),
        ('Arc Wave', 'arc', 'sdq.content.hrs.arc'),
        ('Bias Levels', 'bias', 'sdq.content.hrs.bias'),
        ('Flats', 'flats', 'sdq.content.hrs.flats'),
        ('Order', 'order', 'sdq.content.hrs.order'),
        ('Velocity Standards', 'velocity', 'sdq.content.hrs.velocity'),
    )
    # ++++++ADD+++++++
    _new_menu = (
        ('Menu 1', 'menu1', 'sdq.content.menu.menu_1'),
        ('Menu 2', 'menu2', 'sdq.content.menu.menu_2'),
        ('Menu 3', 'menu3', 'sdq.content.menu.menu_3'),

    )
    # ++++++ADD+++++++

    # primary menu
    #
    # Each list item is a tuple of the title to use in the menu, the slug for the URL and the secondary menu

    ...
```


top/primary menu
------------