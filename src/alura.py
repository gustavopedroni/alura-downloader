from src.drivers import get_chrome
from .helpers.logging import get_logger
from .modules.auth import AluraAuth
from .modules.course import CourseDownloader
from .modules.formation import FormationDownloader
from .modules.lesson import LessonDownloader
from .modules.video import VideoDownloader

logger = get_logger('Alura Manager')


class AluraDownloader:

    def __init__(self, *args, **kwargs):

        self.chrome = get_chrome()
        self.chrome.scopes = ['.*cdn12.*']

        self.errors = []

        self.auth = AluraAuth(alura=self, driver=self.chrome, *args, **kwargs)
        self.video = VideoDownloader(alura=self, driver=self.chrome, *args, **kwargs)
        self.lesson = LessonDownloader(alura=self, driver=self.chrome, *args, **kwargs)
        self.course = CourseDownloader(alura=self, driver=self.chrome, *args, **kwargs)
        self.formation = FormationDownloader(alura=self, driver=self.chrome, *args, **kwargs)

    def start(self, **kwargs):

        self.auth.login()

        if kwargs.get('video_url'):
            logger.info('Starting Video Download')
            self.video.download(kwargs['video_url'])

        elif kwargs.get('lesson_url'):
            logger.info('Starting Lesson Download')
            self.lesson.download(kwargs['lesson_url'])

        elif kwargs.get('course_url'):
            logger.info('Starting Course Download')
            self.course.download(kwargs['course_url'])

        elif kwargs.get('formation_url'):
            logger.info('Starting Formation Download')
            self.formation.download(kwargs['formation_url'])

        elif kwargs.get('formation_list'):
            logger.info('Starting Formation List Download')
            self.formation.download_list(kwargs['formation_list'])

        self.chrome.quit()

    def show_errors(self):

        for error in self.errors:
            logger.error(f'Error in URL: {error["url"]}')

    def register_errors(self):

        if len(self.errors):
            lines = [f'{i}\n' for i in self.errors]
            open('errors.txt', 'w').writelines(lines)
