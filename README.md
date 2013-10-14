EVEStandings
============

A simple library / cli tool to create a standings overview page for a EVE Online corporation or alliance.

Usage
-----

For CLI command use:

- Install evestandings using `python setup.py install`
- Run the `evestandings` command.

For library use:

- Import `Standings` from `standings`
- Init the `Standings` object with your Key ID and vCode (needs ContactList as the only permission)
- Call `render_template`, `text`, or `html` to produce an output.
- Raw standings can be obtained from a dict by calling `Standings._get_standings()`

About
-----

This tool was originally created by Matalok / Andrew Williams for use by Test Alliance Please Ignore.