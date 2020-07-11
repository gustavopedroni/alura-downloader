

import optparse

from dotenv import load_dotenv
from src.alura import AluraDownloader

load_dotenv()

parser = optparse.OptionParser()
parser.add_option('-u', '--url', help='Command base URL', dest='url', metavar='https://alura.com.br/.../')

(options, args) = parser.parse_args()

if __name__ == '__main__':

    if not options.url:  # if filename is not given
        parser.error('URL not given')

    app = AluraDownloader()
    app.start(**options.__dict__)

