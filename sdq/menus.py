from sdq.errors import NotFoundException


# secondary menus
#
# Each menu is described by a list of tuples containing the title to use in the menu, the slug to use in the URL
# and the module for the page content.

_telescope_menu = (
    ('Weather', 'weather', 'sdq.content.telescope.weather'),
    ('Interact', 'interact', 'sdq.content.telescope.interact'),
    ('Seeing', 'seeing', 'sdq.content.telescope.seeing'),
    ('Coffee', 'coffee', 'sdq.content.telescope.coffee')

)


_salticam_menu = (
    ('Diagnostic', 'diagnostics', 'sdq.content.salticam.diagnostics'),
    ('Bias Levels', 'bias', 'sdq.content.salticam.bias'),
    ('Throughput', 'throughput', 'sdq.content.salticam.throughput')
)

_rss_menu = (
    ('Diagnostic', 'diagnostics', 'sdq.content.rss.diagnostics'),
    ('Bias Levels', 'bias', 'sdq.content.rss.bias'),
    ('Throughput', 'throughput', 'sdq.content.rss.throughput'),
    ('Straylight', 'straylight', 'sdq.content.rss.straylight')
)
_hrs_menu = (
    ('Diagnostic', 'diagnostics', 'sdq.content.hrs.diagnostics'),
    ('Arc Wave', 'arc', 'sdq.content.hrs.arc'),
    ('Bias Levels', 'bias', 'sdq.content.hrs.bias'),
    ('Flats', 'flats', 'sdq.content.hrs.flats'),
    ('Order', 'order', 'sdq.content.hrs.order'),
    ('Velocity Standards', 'velocity', 'sdq.content.hrs.velocity'),
)

# primary menu
#
# Each list item is a tuple of the title to use in the menu, the slug for the URL and the secondary menu

_primary_menu = (
    ('Telescope', 'telescope', _telescope_menu),
    ('Salticam', 'salticam', _salticam_menu),
    ('RSS', 'rss', _rss_menu),
    ('HRS', 'hrs', _hrs_menu),
)


def primary_menu():
    return _primary_menu


def primary_menu_item(url):
    slugs = url.split('/')
    if len(slugs) == 0 or not slugs[0]:
        return _primary_menu[0]
    slug = slugs[0]

    menu_item = next(filter(lambda item: item[1] == slug, _primary_menu), None)

    if menu_item is None:
        raise NotFoundException('The requested primary menu item does not exist')

    return menu_item


def secondary_menu(url):
    return primary_menu_item(url)[2]


def secondary_menu_item(url):
    menu = secondary_menu(url)

    slugs = url.split('/')
    if len(slugs) < 2 or not slugs[1]:
        return menu[0]
    slug = slugs[1]

    menu_item = next(filter(lambda item: item[1] == slug, menu), None)

    if menu_item is None:
        raise NotFoundException('The requested secondary menu item does not exist')

    return menu_item
