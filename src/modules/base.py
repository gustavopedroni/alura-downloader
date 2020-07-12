from src.helpers.logging import get_logger

logger = get_logger('Alura')


class BaseModule(object):

    def __init__(self, alura, *args, **kwargs):
        self.alura = alura

    def register_error(self, url):
        self.alura.errors.append(url)
