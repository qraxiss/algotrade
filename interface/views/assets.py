"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    assets.auto_build = True
    assets.debug = False
    less_bundle = Bundle(
        filters="cssmin",
        output="dist/css/styles.css",
    )
    assets.register("less_all", less_bundle)
    if app.config["FLASK_ENV"] == "development":
        less_bundle.build()
    return assets