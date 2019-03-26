from bokeh.embed import components
from itertools import zip_longest
from collections import namedtuple
from flask import render_template, g
from datetime import date
from dateutil.relativedelta import relativedelta

PlotHtml = namedtuple('PlotHtml', ('id', 'modal_id', 'grid_div', 'grid_script', 'closeup_div', 'closeup_script'))

plot_id = 1


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def bokeh_plot_grid(columns, *plots):
    # create html content
    html = []
    plot_info = []
    for p in plots:
        modal_plot = p
        plot = p
        info = p.name

        try:

            modal_plot.sizing_mode = 'scale_width'
            p.toolbar.logo = None
            modal_plot.toolbar_location = 'right'
            modal_plot.height = 700
            modal_plot.width = 700
            modal_plot.toolbar_location = 'right'
            modal_grid_html = components(modal_plot)
            plot.sizing_mode = 'scale_width'
            plot.toolbar_location = None
            plot.toolbar.active_drag = None

            grid_html = components(plot)

        finally:
            pass

        global plot_id
        plot_info.append(info)
        html.append(PlotHtml(
            id=plot_id,
            modal_id=str(plot_id) + '-modal',
            grid_div=grid_html[1],
            grid_script=grid_html[0],
            closeup_div=modal_grid_html[1],
            closeup_script=modal_grid_html[0])
        )
        plot_id += 1
    return render_template('plot_grid.html', columns=columns, zipped_data=zip(html, plot_info))


def none_bokeh_plot_grid(columns, *plots):
    # create html content
    html = []
    for plot in plots:
        global plot_id
        html.append(PlotHtml(id=plot_id,
                             modal_id=str(plot_id) + '-modal',
                             grid_div=plot,
                             grid_script='',
                             closeup_div=plot,
                             closeup_script=''))
        plot_id += 1

    x_grouped = list(grouper(columns, html))
    return render_template('none_bokeh_plot_grid.html', columns=columns, plot_html=x_grouped)


def interact_plot_grid(layout):
    script, div = components(layout)

    return render_template('interaction_grid.html', script=script, div=div)


def plasma_colors():
    return ['#0C0786', '#100787', '#130689', '#15068A', '#18068B', '#1B068C', '#1D068D', '#1F058E', '#21058F',
            '#230590', '#250591', '#270592', '#290593', '#2B0594', '#2D0494', '#2F0495', '#310496', '#330497',
            '#340498', '#360498', '#380499', '#3A049A', '#3B039A', '#3D039B', '#3F039C', '#40039C', '#42039D',
            '#44039E', '#45039E', '#47029F', '#49029F', '#4A02A0', '#4C02A1', '#4E02A1', '#4F02A2', '#5101A2',
            '#5201A3', '#5401A3', '#5601A3', '#5701A4', '#5901A4', '#5A00A5', '#5C00A5', '#5E00A5', '#5F00A6',
            '#6100A6', '#6200A6', '#6400A7', '#6500A7', '#6700A7', '#6800A7', '#6A00A7', '#6C00A8', '#6D00A8',
            '#6F00A8', '#7000A8', '#7200A8', '#7300A8', '#7500A8', '#7601A8', '#7801A8', '#7901A8', '#7B02A8',
            '#7C02A7', '#7E03A7', '#7F03A7', '#8104A7', '#8204A7', '#8405A6', '#8506A6', '#8607A6', '#8807A5',
            '#8908A5', '#8B09A4', '#8C0AA4', '#8E0CA4', '#8F0DA3', '#900EA3', '#920FA2', '#9310A1', '#9511A1',
            '#9612A0', '#9713A0', '#99149F', '#9A159E', '#9B179E', '#9D189D', '#9E199C', '#9F1A9B', '#A01B9B',
            '#A21C9A', '#A31D99', '#A41E98', '#A51F97', '#A72197', '#A82296', '#A92395', '#AA2494', '#AC2593',
            '#AD2692', '#AE2791', '#AF2890', '#B02A8F', '#B12B8F', '#B22C8E', '#B42D8D', '#B52E8C', '#B62F8B',
            '#B7308A', '#B83289', '#B93388', '#BA3487', '#BB3586', '#BC3685', '#BD3784', '#BE3883', '#BF3982',
            '#C03B81', '#C13C80', '#C23D80', '#C33E7F', '#C43F7E', '#C5407D', '#C6417C', '#C7427B', '#C8447A',
            '#C94579', '#CA4678', '#CB4777', '#CC4876', '#CD4975', '#CE4A75', '#CF4B74', '#D04D73', '#D14E72',
            '#D14F71', '#D25070', '#D3516F', '#D4526E', '#D5536D', '#D6556D', '#D7566C', '#D7576B', '#D8586A',
            '#D95969', '#DA5A68', '#DB5B67', '#DC5D66', '#DC5E66', '#DD5F65', '#DE6064', '#DF6163', '#DF6262',
            '#E06461', '#E16560', '#E26660', '#E3675F', '#E3685E', '#E46A5D', '#E56B5C', '#E56C5B', '#E66D5A',
            '#E76E5A', '#E87059', '#E87158', '#E97257', '#EA7356', '#EA7455', '#EB7654', '#EC7754', '#EC7853',
            '#ED7952', '#ED7B51', '#EE7C50', '#EF7D4F', '#EF7E4E', '#F0804D', '#F0814D', '#F1824C', '#F2844B',
            '#F2854A', '#F38649', '#F38748', '#F48947', '#F48A47', '#F58B46', '#F58D45', '#F68E44', '#F68F43',
            '#F69142', '#F79241', '#F79341', '#F89540', '#F8963F', '#F8983E', '#F9993D', '#F99A3C', '#FA9C3B',
            '#FA9D3A', '#FA9F3A', '#FAA039', '#FBA238', '#FBA337', '#FBA436', '#FCA635', '#FCA735', '#FCA934',
            '#FCAA33', '#FCAC32', '#FCAD31', '#FDAF31', '#FDB030', '#FDB22F', '#FDB32E', '#FDB52D', '#FDB62D',
            '#FDB82C', '#FDB92B', '#FDBB2B', '#FDBC2A', '#FDBE29', '#FDC029', '#FDC128', '#FDC328', '#FDC427',
            '#FDC626', '#FCC726', '#FCC926', '#FCCB25', '#FCCC25', '#FCCE25', '#FBD024', '#FBD124', '#FBD324',
            '#FAD524', '#FAD624', '#FAD824', '#F9D924', '#F9DB24', '#F8DD24', '#F8DF24', '#F7E024', '#F7E225',
            '#F6E425', '#F6E525', '#F5E726', '#F5E926', '#F4EA26', '#F3EC26', '#F3EE26', '#F2F026', '#F2F126',
            '#F1F326', '#F0F525', '#F0F623', '#EFF821'
            ]


def dates(start_date=None, end_date=None):
    if not start_date or not end_date:
        _dates = {
            'start_date': date.today() - relativedelta(months=+3),
            'end_date': date.today()
        }
    else:
        _dates = {
            'start_date': start_date,
            'end_date': end_date
        }

    if _dates['start_date'] > _dates['end_date']:
        _dates = {
            'start_date': end_date,
            'end_date': start_date
        }
    g.dates = _dates
    return _dates
