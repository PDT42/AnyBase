"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the project.
"""
from quart import redirect, render_template, url_for


async def index():
    """Return home page_layout."""
    return await render_template("base.html")


async def favicon():
    """Return favicon."""
    return redirect(url_for('static', filename='images/favicon.ico'))
