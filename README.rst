=============================
Data Quality Proof of Concept
=============================

Installation
------------

See the :ref:`installation instructions <installation>` instructions if you want to develop code for the site on your own machine.

Adding a new page
-----------------

Adding a new page to the data quality site is a two-step process.

1. Create the menu item.
2. Create a Python module with the actual page content.

We'll explain these steps by means of a simple example, creating a page for monitoring one of SALT's most important components - the coffee machine.

Open the file :file:`sdq/menus.py`. It defines a variable called ``_primary_menu``. Its entries are used to generate the main menu. As the coffee machine is not part of any instrument, it is reasonable to assume that its status page should fall under 'Telescope', and there is indeed a menu item for this.

.. code-block:: python

  _primary_menu = (
      ('Telescope', 'telescope', _telescope_menu),
      ...
  )

The third entry in the tuple, ``_telescope_menu`` is the secondary menu shown when the 'Telescope' item is selected from the main menu. It looks as follows.

.. code-block:: python

  _telescope_menu = (
      ('Weather', 'weather', 'sdq.content.telescope.weather'),
      ('Seeing', 'seeing', 'sdq.content.telescope.seeing')
  )

Let's add our own entry.

.. code-block:: python

  _telescope_menu = (
      ('Weather', 'weather', 'sdq.content.telescope.weather'),
      ('Seeing', 'seeing', 'sdq.content.telescope.seeing'),
      ('Coffee Machine', 'coffee', 'sdq.content.telescope.coffee')
  )

If you now open the site in your browser and select `Telescope` from the main menu, 
you should see the `Coffee Machine` option in the secondary menu. But if you click on it, you will be greeted by an error co plaining about a missing module.

To fix that, create a file :file:`sdq/content/telescope/coffee.py`. The file path is determined by the third item in the tuple we've added to the secondary menu (``'sdq.content.telescope.coffee'``, that is); all dots were replaced by slashes and ``.py`` was appended.

The module for our page content defines an (optional) title, the content and a description. These are made available in form of variables ``title``, ``content`` and ``description`` in the module. So we add the following to our (empty) :file:`coffee.py` file.

.. code-block:: python
  
  title = 'Coffee Machine Uptime'

  content = '<h2>The coffee machine is working!</h2>'

  description = 'Availability of the coffee machine. The availability of the machine itself as well as the supply of coffee beans are measured.'

If you don't provide a title, the text of the menu item will be used instead.

Save the file and go to ``/dq/telescope/content/coffee`` in your browser. Voilà, you see your shiny new page for ensuring quality control for the coffee machine.
