from sdq.diagnostic_table import diagnostic_table


def plot():
    data = [
      {'name': 'name-1', 'data': [{'date': 'day1', 'status': 'ok'}, {'date': 'day2', 'status': 'noexec'}, {'date': 'day3', 'status': 'ok'}, {'date': 'day4', 'status': 'ok'}]},
      {'name': 'name-2', 'data': [{'date': 'day1', 'status': 'fail'}, {'date': 'day2', 'status': 'ok'}, {'date': 'day3', 'status': 'noexec'}, {'date': 'day4', 'status': 'ok'}]},
      {'name': 'name-3', 'data': [{'date': 'day1', 'status': 'noexec'}, {'date': 'day2', 'status': 'fail'}, {'date': 'day3', 'status': 'noexec'}, {'date': 'day4', 'status': 'noexec'}]},
      {'name': 'name-4', 'data': [{'date': 'day1', 'status': 'ok'}, {'date': 'day2', 'status': 'warning'}, {'date': 'day3', 'status': 'fail'}, {'date': 'day4', 'status': 'ok'}]},
      {'name': 'name-5', 'data': [{'date': 'day1', 'status': 'warning'}, {'date': 'day2', 'status': 'ok'}, {'date': 'day3', 'status': 'ok'}, {'date': 'day4', 'status': 'ok'}]},
      {'name': 'name-6', 'data': [{'date': 'day1', 'status': 'ok'}, {'date': 'day2', 'status': 'ok'}, {'date': 'day3', 'status': 'ok'}, {'date': 'day4', 'status': 'warning'}]}
    ]
    return diagnostic_table(data)

content = plot()

description = 'Salticam Diagnostics.'
