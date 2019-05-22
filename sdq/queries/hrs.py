import pandas as pd

from sdq.sdb_connection import sdb_connect
from sdq.util import plasma_colors
from bokeh.plotting import ColumnDataSource


def arc_query(start_date, end_date, obsmode, arm):
    plasma = plasma_colors()
    if arm.lower() == 'blue':
        arm = 'H%%'
    else:
        arm = 'R%%'
    logic = " and OBSMODE='{obsmode}'  " \
            "   and DeltaX > -99 " \
            "   and FileName like '{arm}' " \
            "   and Object = 1  group by UTStart, HrsOrder" \
        .format(arm=arm, obsmode=obsmode)
    sql = "Select UTStart, HrsOrder, AVG(DeltaX) as avg, CONVERT(UTStart,char) AS Time " \
          "     from DQ_HrsArc join FileData using (FileData_Id) " \
          "     where UTStart > '{start_date}' and UTStart <'{end_date}' {logic}" \
        .format(start_date=start_date, end_date=end_date, logic=logic)

    df = pd.read_sql(sql, sdb_connect())

    color = []
    if len(df) > 0:
        ord_min = df['HrsOrder'].min()
        ord_max = df.HrsOrder.max()
        ord_dif = ord_max - ord_min
        if ord_dif < 1:
            ord_dif = 1
        color = [plasma[int((y - ord_min) * (len(plasma) - 1) / float(ord_dif))] for y in df["HrsOrder"]]

    df['plasma_colors'] = color

    source = ColumnDataSource(df)
    return source


def bias_counts_query(start_date, end_date, arm):

    sql = """
SELECT Date, bias_med, bias_std
FROM DQ_HrsBias
JOIN NightInfo USING(NightInfo_Id)
JOIN DQ_HrsArm USING(DQ_HrsArm_Id)
WHERE Date > '{start_date}'
    AND Date <'{end_date}'
    AND DQ_HrsArm = '{arm}'
""".format(start_date=start_date, end_date=end_date, arm=arm)

    df = pd.read_sql(sql, sdb_connect())
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def bias_gradient_query(start_date, end_date, arm, cf):
    gradient = 'bias_cfx' if cf == 'x' else 'bias_cfy'
    sql = """
SELECT Date, {gradient}
FROM DQ_HrsBias
JOIN NightInfo USING(NightInfo_Id)
JOIN DQ_HrsArm USING(DQ_HrsArm_Id)
WHERE Date > '{start_date}'
    AND Date <'{end_date}'
    AND DQ_HrsArm = '{arm}'
""".format(start_date=start_date, end_date=end_date, arm=arm, gradient=gradient)

    df = pd.read_sql(sql, sdb_connect())
    df['Date'] = pd.to_datetime(df['Date'])
    return df
