# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import hashlib

from flask import flash, request


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def make_cache_key():
    # get传入的参数
    args_as_sorted_tuple = tuple(
        sorted((pair for pair in request.args.items(multi=True)))
    )
    args_as_bytes = str(args_as_sorted_tuple).encode()
    # post提交的参数
    form_as_sorted_tuple = tuple(
        sorted((pair for pair in request.form.items(multi=True)))
    )
    form_as_bytes = str(args_as_sorted_tuple).encode()

    hashed_args = str(hashlib.md5(args_as_bytes + form_as_bytes).hexdigest())
    cache_key = request.path + hashed_args
    return cache_key
