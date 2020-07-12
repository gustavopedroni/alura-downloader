import os
import time

from .course import CourseDownloader
from ..helpers.logging import get_logger
from ..helpers.text import file_folder_name

logger = get_logger('Formation')


class FormationDownloader:

    def __init__(self, output, driver, *args, **kwargs):
        self.driver = driver
        self.output = output if output else 'dist'

        self.args = args
        self.kwargs = kwargs

        self.formation_name = 'undefined-formation'

        self.courses = []
        self.course = None

    def set_formation_details(self):

        formation_name = self.driver.find_element_by_class_name('formacao-headline-titulo').text

        self.formation_name = file_folder_name(formation_name)

    def open_formation(self, url):
        logger.info('Loading Page')

        self.driver.get(url)
        time.sleep(2)

        self.set_formation_details()

    def extract_courses(self):

        items = self.driver.find_elements_by_class_name('learning-content__link')

        for i in items:
            link = i.get_attribute('href')

            link_type = i.find_element_by_class_name('learning-content__kind').text

            if link_type == 'CURSO':
                self.courses.append(link)

    def set_formation_instance(self):

        self.course = CourseDownloader(
            driver=self.driver,
            output=self.output,
            *self.args,
            **self.kwargs
        )

    def download(self, url):

        start_time = time.time()

        self.open_formation(url)
        self.extract_courses()

        self.output = os.path.join(self.output, self.formation_name)

        self.set_formation_instance()

        from IPython import embed; embed()

        for course_url in self.courses:
            self.course.download(course_url)

        end_time = time.time()

        logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))
