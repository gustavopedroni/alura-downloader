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
        self.output_formation = ''

        self.args = args
        self.kwargs = kwargs

        self.formation_name = 'undefined-formation'

        self.courses = []
        self.course = None

    def set_formation_details(self):

        formation_name = self.driver.find_element_by_class_name('formacao-headline-titulo').text

        self.formation_name = file_folder_name(formation_name)

    def open_formation(self, url):
        logger.info(f'Loading Page {url}')

        self.driver.get(url)
        time.sleep(2)

        self.set_formation_details()

    def extract_courses(self):

        self.courses = []

        items = self.driver.find_elements_by_class_name('learning-content__link')

        for i in items:
            link = i.get_attribute('href')

            link_type = i.find_element_by_class_name('learning-content__kind').text

            if link_type == 'CURSO':
                self.courses.append(link)

    def set_formation_instance(self):

        self.course = CourseDownloader(
            driver=self.driver,
            output=self.output_formation,
            *self.args,
            **self.kwargs
        )

    def download(self, url):

        start_time = time.time()

        self.open_formation(url)
        self.extract_courses()

        logger.info(f'Starting Formation {self.formation_name}')
        logger.debug(f'Courses from Formation: {self.courses}')

        self.output_formation = os.path.join(self.output, self.formation_name)

        self.set_formation_instance()

        for course_url in self.courses:
            self.course.download(course_url)

        end_time = time.time()
        logger.info(f'Formation Finished {self.formation_name}')
        logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))

    def download_list(self, formation_list):

        formation_list = os.path.abspath(formation_list)
        logger.info(f'Starting formation list from: {formation_list}')

        lines = open(formation_list, 'r').readlines()

        while len(lines) > 0:

            url = lines[0].replace('\n', '')
            self.download(url)

            lines = lines[1::]
            open(formation_list, 'w').writelines(lines)
