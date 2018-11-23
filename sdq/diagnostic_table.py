from sdq.util import grouper


def table_head(dates):
    head = ''
    for day in dates:
        if None not in day:
            head += '<th colspan="{length}">{day1} to {day2}</th>'\
                .format(day1=day[0],
                        day2=day[len(day)-1],
                        length=len(day))
        else:
            dayx = [x for x in day if x is not None]
            head += '<th colspan="{length}">{day1} to {day2}</th>'\
                .format(day1=day[0],
                        day2=dayx[len(dayx)-1],
                        length=len(day))

    return head


def table_body(data):
    body = ''
    for key, row in data.items():
        name=key
        body += '<tr><td>{name}</td>'.format(name=name)
        for s in row:
            try:
                if s['color'] is None or s['color'] not in ['red', 'green', 'orange', 'yellow', 'grey']:
                    body += '<td></td>'
                else:
                     body += '<td><b class="tip" style="background-color: {color}; color: {color};">' \
                             '..' \
                             '<span>name: {name} <br/>date: {date}</span>' \
                             '</b></td>'\
                        .format(color=s['color'], date=s['date'], name=name)
            except TypeError:
                pass
        body += '</tr>'
    return body


def color_code(status):
    if status == 'ok':
        color = 'green'
    elif status == 'fail':
        color = 'red'
    elif status == 'warning':
        color = 'yellow'
    elif status == 'noexec':
        color = 'orange'
    else:
        color = 'grey'
    return color


def table_row(row_data):
    row = '<tr><td>{name}</td>'.format(name=row_data['name'])
    for r in row_data['data']:
        if r['status'] == 'ok':
            row += '<td><p style="background-color: green; color: green;">.</p></td>'
        elif r['status'] == 'fail':
            row += '<td><p style="background-color: red; color: red;">.</p></td>'
        elif r['status'] == 'warning':
            row += '<td><p style="background-color: yellow; color: yellow;">.</p></td>'
        elif r['status'] == 'noexec':
            row += '<td><p style="background-color: orange; color: orange;">.</p></td>'
        else:
            row += '<td><p style="background-color: grey; color: grey;">.</p></td>'
    return row + '</tr>'


def diagnostic_table(data):
    """
        :param data an iterable
        :return html table to display
    """
    table_head = ''
    table_body = ''
    if not isinstance(data, list):
        return '<p style="color: red;">Fail to display this table </p>'

    for index, item in enumerate(data):
        if index == 0:
            for day in item['data']:
                table_head += '<th>{date}</th>'.format(date=day['date'])

        table_body += table_row(item)

    return '''
<div class="container">
  <table  class='table is-striped'>
    <thead>
      <tr>
        <td>Name</td>{head}
      </tr>
    </thead>
    <tbody>{body}</tbody>
    <tfoot>
      <tr>
        <td>Name</td>{head}
      </tr>
    </tfoot>
  </table>
</div>
    '''.format(head=table_head, body=table_body)


def diagnostic_table_week(data):
    if not isinstance(data, list):
        return '<p style="color: red;">Fail to display this table </p>'

    dt = []
    nm = []
    for d in data:
        if d['name'] not in nm:
            nm.append(d['name'])
        for day in d['data']:
            if day['date'] not in dt:
                dt.append(day['date'])

    nm.sort()
    dt.sort()
    dt = [list(elem) for elem in list(grouper(7, dt))]
    final_data = {}

    for name in nm:
        date_copy = []
        for week in dt:
            for d in week:
                date_copy.append({'date': d, 'color': 'white'})
        final_data[name] = date_copy

    for value in data:
        for d in value['data']:
            for f in final_data[value['name']]:
                if d['date'] == f['date']:
                    f['color'] = color_code(d['status'])



    thead = table_head(dt)
    tbody = table_body(final_data)
    plot = '''
<div class="container" style="overflow-x:auto; width: 90%; height: 90%;" >
  <table  class='table is-striped  is-bordered' style="overflow: scroll;">
    <thead>
      <tr>
        <td>Name</td>{head}
      </tr>
    </thead>
    <tbody>{body}</tbody>
    <tfoot>
      <tr>
        <td>Name</td>{head}
      </tr>
    </tfoot>
  </table>
</div>
    '''.format(head=thead, body=tbody)
    return plot
