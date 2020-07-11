from src.drivers import get_chrome
from .modules.auth import AluraAuth
from .modules.video import VideoDownloader


class AluraDownloader:

    def __init__(self, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs

        self.chrome = get_chrome()
        self.chrome.scopes = ['.*cdn12.*']

        self.video = VideoDownloader(driver=self.chrome)
        self.auth = AluraAuth(driver=self.chrome)

    def start(self, url, playlist=False, base_folder=None, *args, **kwargs):
        self.auth.login()

        if not playlist:
            self.video.set_base_folder(base_folder)
            self.video.download(url)
        else:
            print('aaa')
