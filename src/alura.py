from src.drivers import get_chrome
from .helpers.logging import get_logger
from .modules.auth import AluraAuth
from .modules.video import VideoDownloader

logger = get_logger('Alura Manager')


class AluraDownloader:

    def __init__(self, *args, **kwargs):

        self.chrome = get_chrome()
        self.chrome.scopes = ['.*cdn12.*']

        self.video = VideoDownloader(driver=self.chrome, *args, **kwargs)
        self.auth = AluraAuth(driver=self.chrome, *args, **kwargs)

    def start(self, lesson_url=None, video_url=None, *args, **kwargs):

        self.auth.login()

        if video_url:
            self.video.download(video_url)
