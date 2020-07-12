import os
import time

from .lesson import LessonDownloader
from ..helpers.logging import get_logger
from ..helpers.text import file_folder_name

logger = get_logger('Course')


class CourseDownloader:

    def __init__(self, output, driver, *args, **kwargs):
        self.driver = driver
        self.output = output if output else 'dist'

        self.args = args
        self.kwargs = kwargs

        self.course_name = 'undefined-course'

        self.lessons = []
        self.lesson = None

    def set_course_details(self):

        course_name = self.driver.find_element_by_class_name('course-header-banner-title') \
            .find_element_by_tag_name('strong').text

        self.course_name = file_folder_name(course_name)

    def open_course(self, url):
        logger.info('Loading Page')

        self.driver.get(url)
        time.sleep(2)

        self.set_course_details()

    def extract_lessons(self):

        self.lessons = []

        menu = self.driver.find_element_by_class_name('courseSectionList')
        items = menu.find_elements_by_class_name('courseSection-listItem')

        for i in items:

            link = i.find_element_by_tag_name('a').get_attribute('href')
            self.lessons.append(link)

    def set_lesson_instance(self):

        self.lesson = LessonDownloader(
            driver=self.driver,
            output=self.output,
            *self.args,
            **self.kwargs
        )

    def download(self, url):

        start_time = time.time()

        self.open_course(url)
        self.extract_lessons()

        self.output = os.path.join(self.output, self.course_name)

        self.set_lesson_instance()

        for lesson_url in self.lessons:
            self.lesson.download(lesson_url)

        end_time = time.time()

        logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))
