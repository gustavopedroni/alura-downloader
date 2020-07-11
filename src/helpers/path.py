import os


def folder(f):
    if not os.path.isdir(f):
        os.mkdir(os.path.join(os.path.abspath('./'), f))

    return f


def file(f):
    if os.path.isfile(f):
        os.remove(f)

    return f
