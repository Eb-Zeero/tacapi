from sdq.data import data_t
from sdq.diagnostic_table import diagnostic_table_week


def plot():
    return diagnostic_table_week(data_t())

content = plot()

description = 'RSS Diagnostics.'
