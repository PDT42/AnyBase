"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the project.
"""
from flask import render_template


def index():
    """Return home page."""
    return render_template("base.html")

