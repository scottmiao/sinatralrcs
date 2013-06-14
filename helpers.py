from flask import request

# helper for sytling the current page


def is_current(path='/'):
    return 'current' if request.path == path or request.path == path + '/' \
        else ''


def set_title(title=''):
    return "Songs By Sinatra" if title == '' else title
