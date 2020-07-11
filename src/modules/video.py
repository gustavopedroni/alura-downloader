import os
import re
import time
import shutil

import requests

from ..helpers.path import folder, file
from ..helpers.text import file_folder_name
from ..helpers.encoder import ts_to_mp4
from ..helpers.logging import get_logger

logger = get_logger('Video')


class VideoDownloader:

    def __init__(self, driver, *args, **kwargs):
        self.driver = driver

        self.args = args
        self.kwargs = kwargs

        self.source = None

        self.playlist_name = 'undefined-playlist'
        self.video_name = 'undefined-video'
        self.base_folder = ''

    def set_base_folder(self, base_folder):
        self.base_folder = base_folder

    def wait_video_start(self, timeout=30):

        start = time.time()

        while time.time() - start < timeout:
            request = self.driver.last_request

            if request is not None and request.path.find('.ts') > 0:
                return
            else:
                time.sleep(0.2)

    def get_video(self, url):
        logger.info('Get Video: Waiting Page')
        self.driver.get(url)

        time.sleep(2)

        self.playlist_name = file_folder_name(
            self.driver.find_element_by_class_name('task-menu-header-info-title-text').text
        )

        video_name = self.driver.find_element_by_class_name('task-body-header-title-text').text
        video_index = self.driver.find_element_by_class_name('task-body-header-title') \
            .find_element_by_tag_name('small').text

        self.video_name = file_folder_name(f'{video_index} - {video_name}')

        self.driver.find_element_by_class_name('vjs-big-play-button').click()
        logger.info('Get Video: Waiting Video Start')
        self.wait_video_start()
        logger.info('Get Video: Video Starts!')
        self.driver.find_element_by_class_name('vjs-play-control').click()
        logger.info('Get Video: Pause Video')
        # seg+-\w-v1

        self.source = lambda seg: re.sub(r'seg+-\w-v1', seg, self.driver.last_request.path)

    def download_ts(self):

        folder(self.playlist_name)
        ts_folder = folder(os.path.join(self.playlist_name, 'ts'))

        count = 1

        logger.info(f'Starting Video: {self.video_name}')

        ts_list = []

        while True:

            try:

                url = self.source(f'seg-{count}-v1')

                r = requests.get(url)
                r.raise_for_status()

                file_name = file(f'{ts_folder}/{self.video_name}-{count}.ts')

                ts_list.append(file_name)

                with open(file_name, 'wb') as f:
                    f.write(r.content)

                logger.info(f'Downloaded URL: {url}')

                count += 1

            except requests.exceptions.HTTPError:
                break

        return ts_list

    def create_list_file(self, video_list):

        list_name = f'{self.playlist_name}/list.txt'

        with open(list_name, 'wb') as f:
            for i in video_list:
                f.write(f"file '{os.path.abspath(i)}'\n".encode())

        return list_name

    def to_mp4(self, ts_list_file):

        output = os.path.abspath(f'{self.playlist_name}/{self.video_name}')
        ts_to_mp4(ts_list_file, output)

    def remove_ts(self):
        shutil.rmtree(os.path.abspath(os.path.join(self.playlist_name, 'ts')))
        ts_file = os.path.abspath(f'{self.playlist_name}/{self.video_name}.ts')
        os.unlink(ts_file)

    def remove_list(self):
        list_name = f'{self.playlist_name}/list.txt'
        os.unlink(list_name)

    def download(self, url):

        start_time = time.time()

        self.get_video(url)
        ts_list = self.download_ts()
        ts_list_file = self.create_list_file(ts_list)

        self.to_mp4(ts_list_file)

        self.remove_ts()
        self.remove_list()

        timed = time.time() - start_time

        logger.info("Download Video in: %s seconds" % timed)
