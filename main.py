

import optparse

from dotenv import load_dotenv
from src.alura import AluraDownloader

load_dotenv()

parser = optparse.OptionParser()
parser.add_option('-v', '--video', help='Command video url', dest='video_url', metavar='https://alura.com.br/.../')
parser.add_option('-o', '--output', help='Command base URL', dest='output', metavar='https://alura.com.br/.../')

(options, args) = parser.parse_args()

if __name__ == '__main__':

    app = AluraDownloader(output=options.output)
    opts = options.__dict__

    has_options = len(list(filter(None, opts.values())))

    if not has_options:
        app.start(video_url=args[0])

    else:
        app.start(**opts)
