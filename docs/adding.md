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
```python
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
```text
+--------------+----------+---------------+--------------+--------------+
| date         |arc       |flats          |bias          |color         |
+--------------+----------+---------------+--------------+--------------+
|                                   ...                                 |
+--------------+----------+---------------+--------------+--------------+
| 11-12-2018   |56        | 50            |133           | red          |
+--------------+----------+---------------+--------------+--------------+
| 12-12-2018   |46        | 70            |100           | green        |
+--------------+----------+---------------+--------------+--------------+
|                                   ...                                 |
+--------------+----------+---------------+--------------+--------------+
| 30-12-2018   |33        | 72            |120           |  blue        |
+--------------+----------+---------------+--------------+--------------+
| 31-12-2018   |33        | 72            |120           |  uv          |
+--------------+----------+---------------+--------------+--------------+
|                                   ...                                 |
+--------------+----------+---------------+--------------+--------------+
```
And on each we need to plot date over value.
then `sdq/queries/bvit.py`:
```python
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

```python
from bokeh.plotting import figure
from flask import g
from sdq.util import bokeh_plot_grid
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
File `sdq/content/bvit/bias.py` and `sdq/content/bvit/flats.py`

```text
.
.
.
content = bokeh_plot_grid(2,
             plot('bias/flats', 'red'),
             plot('bias/flats', 'green'),
             plot('bias/flats', 'blue'),
             plot('bias/flats', 'uv'),
             plot('bias/flats', 'xray')
             )

description = 'Bias/Flats waves for BVIT on different colors'
.
.
.

```

Step two Adding BVIT to menu
----------------------------
Each secodary/side menu is described by a list of tuples containing the title to use in the menu, the slug to use in the URL and the
module for the page content.
You can create a new one or add it to th existing one.
To add one:
On file `sdq\menus.py` add a secondary menu before using it like
```python
...
_hrs_menu = (
       ('Diagnostic', 'diagnostics', hrs_blue),
    ('Arc Wave', 'arc', hrs_blue),
    ('Bias Levels', 'bias', hrs_blue),
    ('Flats', 'flats', hrs_blue),
    ('Order', 'order', hrs_blue),
    ('Velocity Standards', 'velocity', hrs_blue),
)
# ++++++ADD+++++++
_bvit_menu = (
    ('Arcs', 'arcs', 'sdq.content.bvit.arcs'),
    ('Bias', 'bias', 'sdq.content.bvit.bias'),
    ('Flats', 'flats', 'sdq.content.bvit.flats'),
)
# ++++++ADD+++++++

# primary menu
#
# Each list item is a tuple of the title to use in the menu, the slug for the URL and the secondary menu

...
```
Primary/top menu list item is a tuple of the title to use in the menu, the slug for the URL and the secondary menu

lastly add BVIT to primary/top menu like
```python
...
# primary menu
#
# Each list item is a tuple of the title to use in the menu, the slug for the URL and the secondary menu

_primary_menu = (
    ('Telescope', 'telescope', _telescope_menu),
    ('Salticam', 'salticam', _salticam_menu),
    ('RSS', 'rss', _rss_menu),
    ('HRS', hrs_blue, _hrs_menu),
    # ++++++ADD+++++++
    ('BVIT', 'bvit', _bvit_menu)
    # ++++++ADD+++++++
)
...
```
