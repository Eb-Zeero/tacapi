from importlib import import_module

from sdq.errors import ContentModuleException
from flask import Flask, render_template
from sdq.menus import primary_menu, primary_menu_item, secondary_menu, secondary_menu_item, dates

app = Flask(__name__)


@app.errorhandler(ContentModuleException)
def content_module_error(e):
    return render_template('500.html', message=str(e))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def generic_error(e):
    return render_template('500.html'), 500


@app.route('/', defaults={'page': ''})
@app.route('/dq', defaults={'page': ''})
@app.route('/dq/<path:page>')
def hello(page):
    # get the module for the content from the selected secondary menu item
    sec_menu_item = secondary_menu_item(page)
    module_name = sec_menu_item[2]
    try:
        content_module = import_module(module_name)
    except ModuleNotFoundError as e:
        error = 'The module {module_name} does not exist. \
Please refer to the documentation on adding pages to this website.'\
            .format(module_name=module_name)
        raise ContentModuleException(error)

    # get the title
    if hasattr(content_module, 'title'):
        title = content_module.title
    else:
        title = sec_menu_item[0]

    # get the content
    if hasattr(content_module, 'content'):
        content = content_module.content
    else:
        content = None

    # get the description
    if hasattr(content_module, 'description'):
        description = content_module.description
    else:
        description = None

    if not content or not description:
        error = 'The content or the description is missing in the module {module_name}. \
Please refer to the documentation on adding pages to this website.'\
        .format(module_name=module_name)
        raise ContentModuleException(error)

    return render_template('data_quality.html',
                           primary_menu=primary_menu(),
                           dates=dates(),
                           primary_menu_item=primary_menu_item(page),
                           secondary_menu=secondary_menu(page),
                           secondary_menu_item=secondary_menu_item(page),
                           title=title,
                           content=content,
                           description=description)
