from src.helpers.logging import get_logger

logger = get_logger('Alura')


class BaseModule(object):

    def __init__(self, alura, *args, **kwargs):
        self.alura = alura

    def register_error(self, url, path):
        self.alura.errors.append({
            'url': url,
            'path': path
        })

        if len(self.alura.errors):
            lines = [f'python main.py -o "{e["path"]}" -v {e["url"]}\n' for e in self.alura.errors]
            open('errors.txt', 'w').writelines(lines)
