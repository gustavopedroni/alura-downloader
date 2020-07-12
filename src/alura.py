from src.drivers import get_chrome
from .helpers.logging import get_logger
from .modules.auth import AluraAuth
from .modules.course import CourseDownloader
from .modules.lesson import LessonDownloader
from .modules.video import VideoDownloader
from .modules.formation import FormationDownloader

logger = get_logger('Alura Manager')


class AluraDownloader:

    def __init__(self, *args, **kwargs):

        self.chrome = get_chrome()
        self.chrome.scopes = ['.*cdn12.*']

        self.auth = AluraAuth(driver=self.chrome, *args, **kwargs)
        self.video = VideoDownloader(driver=self.chrome, *args, **kwargs)
        self.lesson = LessonDownloader(driver=self.chrome, *args, **kwargs)
        self.course = CourseDownloader(driver=self.chrome, *args, **kwargs)
        self.formation = FormationDownloader(driver=self.chrome, *args, **kwargs)

    def start(self, **kwargs):

        self.auth.login()

        if kwargs.get('video_url'):
            logger.info('Starting Video Download')
            self.video.download(kwargs['video_url'])

        if kwargs.get('lesson_url'):
            logger.info('Starting Lesson Download')
            self.lesson.download(kwargs['lesson_url'])

        if kwargs.get('course_url'):
            logger.info('Starting Course Download')
            self.course.download(kwargs['course_url'])

        if kwargs.get('formation_list'):
            logger.info('Starting Formation List Download')
            self.formation.download_list(kwargs['formation_list'])

        self.chrome.quit()
