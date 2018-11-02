
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
