import traceback

from src.drivers import get_chrome
from .helpers.logging import get_logger
from .modules.auth import AluraAuth
from .modules.course import CourseDownloader
from .modules.formation import FormationDownloader
from .modules.lesson import LessonDownloader
from .modules.video import VideoDownloader
from .types import *

logger = get_logger('Alura Manager')


class AluraDownloader:

    def __init__(self, *args, **kwargs):

        self.errors = []
        self.driver = get_chrome()
        self.driver.scopes = ['.*alura.com.br.*']

        self.args = args
        self.kwargs = kwargs

        self.auth = AluraAuth(alura=self, driver=self.driver, *args, **kwargs)
        self.lesson = LessonDownloader(alura=self, driver=self.driver, *args, **kwargs)
        self.course = CourseDownloader(alura=self, driver=self.driver, *args, **kwargs)
        self.formation = FormationDownloader(alura=self, driver=self.driver, *args, **kwargs)

    def start(self, url, stype=None):

        if not stype and not url:
            pass

        stype = stype()
        downloader = None

        if isinstance(stype, VideoType):
            logger.info('Starting Video Download')
            downloader = VideoDownloader(alura=self, driver=self.driver, *self.args, **self.kwargs)

        elif isinstance(stype, LessionType):
            logger.info('Starting Lesson Download')
            downloader = LessonDownloader(alura=self, driver=self.driver, *self.args, **self.kwargs)

        elif isinstance(stype, CourseType):
            logger.info('Starting Course Download')
            downloader = CourseDownloader(alura=self, driver=self.driver, *self.args, **self.kwargs)

        elif isinstance(stype, (FormationType, FormationListType)):
            logger.info('Starting Formation Download')
            downloader = FormationDownloader(alura=self, driver=self.driver, *self.args, **self.kwargs)

        if downloader:

            try:
                self.auth.login()

                if isinstance(stype, FormationListType):
                    downloader.download_list(url)
                else:
                    downloader.download(url)

            except Exception as error:
                logger.exception(error)

            except KeyboardInterrupt:
                pass

            finally:
                self.driver.quit()
                self.show_errors()

    def show_errors(self):

        for error in self.errors:
            logger.error(f'Error in URL: {error["url"]}')

    def register_errors(self):

        if len(self.errors):
            lines = [f'{i}\n' for i in self.errors]
            open('errors.txt', 'w').writelines(lines)
