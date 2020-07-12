import os


def folder(f):
    if not os.path.isdir(f):
        os.makedirs(f)

    return f


def file(f):
    if os.path.isfile(f):
        os.remove(f)

    return f
