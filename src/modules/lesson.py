import os
import time

from .video import VideoDownloader
from ..helpers.logging import get_logger
from ..helpers.text import file_folder_name

logger = get_logger('Lesson')


class LessonDownloader:

    def __init__(self, output, driver, *args, **kwargs):
        self.driver = driver
        self.output = output if output else 'dist'

        self.args = args
        self.kwargs = kwargs

        self.lesson_name = 'undefined-lesson'

        self.videos = []
        self.video = None

    def set_lesson_details(self):

        lesson_name = self.driver.find_element_by_class_name('task-menu-section-title-text').text
        lesson_index = self.driver.find_element_by_class_name('task-menu-section-title-number') \
            .find_element_by_tag_name('strong').text

        self.lesson_name = file_folder_name(f'{lesson_index} - {lesson_name}')

    def open_lesson(self, url):
        logger.info('Loading Page')

        self.driver.get(url)
        time.sleep(2)

        self.set_lesson_details()

    def extract_videos(self):

        self.videos = []

        menu = self.driver.find_element_by_class_name('task-menu-nav-list')
        items = menu.find_elements_by_class_name('task-menu-nav-item')

        for i in items:

            link = i.find_element_by_tag_name('a').get_attribute('href')

            try:

                i.find_element_by_class_name('task-menu-nav-item-infos')
                self.videos.append(link)

            except Exception:
                continue

    def set_video_instance(self):

        self.video = VideoDownloader(
            driver=self.driver,
            output=self.output,
            *self.args,
            **self.kwargs
        )

    def download(self, url):

        start_time = time.time()

        self.open_lesson(url)
        self.extract_videos()

        self.output = os.path.join(self.output, self.lesson_name)

        self.set_video_instance()

        for video_url in self.videos:
            self.video.download(video_url)

        end_time = time.time()

        logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))
