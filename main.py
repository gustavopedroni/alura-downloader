import optparse
from dotenv import load_dotenv
from src.alura import AluraDownloader

load_dotenv()

parser = optparse.OptionParser()
parser.add_option('-v', '--video', help='Command video url', dest='video_url', metavar='https://alura.com.br/.../')
parser.add_option('-l', '--lesson_url', help='Command lesson url', dest='lesson_url',
                  metavar='https://alura.com.br/.../')
parser.add_option('-c', '--course_url', help='Command course url', dest='course_url',
                  metavar='https://alura.com.br/.../')
parser.add_option('-f', '--formation_url', help='Command formation url', dest='formation_url',
                  metavar='https://alura.com.br/.../')
parser.add_option('-L', '--formation_list', help='Command formation list txt', dest='formation_list',
                  metavar='https://alura.com.br/.../')
parser.add_option('-o', '--output', help='Command base URL', dest='output', metavar='https://alura.com.br/.../')

(options, args) = parser.parse_args()

if __name__ == '__main__':

    opts = options.__dict__
    app = AluraDownloader(**opts)

    try:

        if len(args):
            opts['video_url'] = args[0]

        app.start(**opts)

    except (Exception, KeyboardInterrupt):
        app.chrome.quit()

    finally:
        app.show_errors()
