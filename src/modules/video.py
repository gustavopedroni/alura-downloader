import os
import re
import time
import shutil

import requests

from ..helpers.path import folder, file
from ..helpers.text import file_folder_name
from ..helpers.encoder import Encoder
from ..helpers.logging import get_logger

logger = get_logger('Video')


class VideoDownloader:

    def __init__(self, output, driver, *args, **kwargs):
        self.driver = driver
        self.output = output if output else 'dist'

        self.args = args
        self.kwargs = kwargs

        self.video_name = 'undefined-video'
        self.list_file = ''

        self.tmp_folder = 'tmp'

        self.source = lambda seg: re.sub(r'seg+-\w-v1', seg, self.driver.last_request.path)

    def wait_video_start(self, timeout=30):

        start = time.time()

        while time.time() - start < timeout:
            request = self.driver.last_request

            if request is not None and request.path.find('.ts') > 0:
                return
            else:
                time.sleep(0.2)

    def set_video_details(self):

        video_name = self.driver.find_element_by_class_name('task-body-header-title-text').text
        video_index = self.driver.find_element_by_class_name('task-body-header-title') \
            .find_element_by_tag_name('small').text

        self.video_name = file_folder_name(f'{video_index} - {video_name}')

    def open_video(self, url):
        logger.info('Loading Page')
        self.driver.get(url)
        time.sleep(2)

        self.set_video_details()

        self.driver.find_element_by_class_name('vjs-big-play-button').click()
        logger.info('Waiting Video Start')
        self.wait_video_start()
        logger.info('Video Starts!')
        self.driver.find_element_by_class_name('vjs-play-control').click()
        logger.info('Video Paused')

    def download_ts(self):

        folder(self.tmp_folder)
        ts_folder = folder(os.path.join(self.tmp_folder, 'ts'))

        count = 1

        logger.info(f'Starting Video: {self.video_name}')

        ts_list = []

        while True:

            try:

                logger.debug(f'Downloading Part {count}')

                url = self.source(f'seg-{count}-v1')
                logger.debug(f'Downloading URL: {url}')

                r = requests.get(url)
                r.raise_for_status()

                file_name = file(f'{ts_folder}/{self.video_name}-{count}.ts')

                ts_list.append(file_name)

                with open(file_name, 'wb') as f:
                    f.write(r.content)

                count += 1

            except requests.exceptions.HTTPError:
                break

        return ts_list

    def create_list_file(self, video_list):

        list_name = f'{self.tmp_folder}/list.txt'

        with open(list_name, 'wb') as f:
            for i in video_list:
                f.write(f"file '{os.path.abspath(i)}'\n".encode())

        return list_name

    def check_output_folder(self):

        if self.output:
            folder(self.output)

    def encode_video(self):

        self.check_output_folder()

        output = f'{self.output}/{self.video_name}'
        Encoder().ts_to_mp4(self.list_file, output)

    def clean_chunks(self):

        logger.info('Clearing chunks')
        logger.debug('Removing TMP Folder')

        shutil.rmtree(self.tmp_folder)

        logger.debug('Removed TMP Folder')

        logger.debug('Removing TS File')
        ts_file = os.path.abspath(f'{self.output}/{self.video_name}.ts')
        os.unlink(ts_file)
        logger.debug('Removed TS File')

    def download_video(self):

        ts_list = self.download_ts()
        self.list_file = self.create_list_file(ts_list)

    def download(self, url):

        start_time = time.time()

        self.open_video(url)

        download_start = time.time()
        self.download_video()
        download_end = time.time()

        converting_start = time.time()
        self.encode_video()
        converting_end = time.time()

        self.clean_chunks()

        end_time = time.time()

        logger.info("Converted Video in: %s seconds" % (download_end - download_start))
        logger.info("Download Video in: %s seconds" % (converting_end - converting_start))
        logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))
