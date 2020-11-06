import asyncio
import os
import re
import shutil
import time

import aiohttp

from .base import BaseModule
from ..helpers.encoder import Encoder
from ..helpers.logging import get_logger
from ..helpers.path import folder, file
from ..helpers.text import file_folder_name

logger = get_logger('Video')


class VideoDownloader(BaseModule):

    def __init__(self, output, driver, *args, **kwargs):
        BaseModule.__init__(self, *args, **kwargs)

        self.driver = driver
        self.output = output if output else 'dist'

        self.args = args
        self.kwargs = kwargs

        self.video_name = 'undefined-video'
        self.video_list = []
        self.list_file = ''

        self.tmp_folder = 'tmp'

        self.source_url = ''
        self.source = lambda seg: re.sub(r'seg+-\w+-v1', seg, self.source_url)

        self.io_workers = 15

    def wait_video_load(self, timeout=30):

        start = time.time()

        while time.time() - start < timeout:

            try:

                self.driver.find_element_by_class_name('vjs-big-play-button')
                break

            except Exception:
                time.sleep(0.2)

    def different_video(self, request):

        request_search = re.search(r'alura/(.*?)/', request)
        source_search = re.search(r'alura/(.*?)/', self.source_url)

        request_video_name = request_search.group(1) if request_search else ''
        source_video_name = source_search.group(1) if source_search else ''

        if request_video_name != source_video_name:
            return True

        return False

    def wait_video_start(self, timeout=60):

        start = time.time()

        while time.time() - start < timeout:
            request = self.driver.last_request

            if request is not None and request.url.find('.ts') > 0 and self.different_video(request.url):
                self.source_url = request.url
                break

            else:
                time.sleep(0.2)

    def set_video_details(self):

        video_name = self.driver.find_element_by_class_name('task-body-header-title-text').text
        video_index = self.driver.find_element_by_class_name('task-body-header-title') \
            .find_element_by_tag_name('small').text

        self.video_name = file_folder_name(f'{video_index} - {video_name}')

    def open_video(self, url):

        if self.driver.current_url != url:
            logger.info(f'Loading Page {url}')

            self.driver.get(url)
            time.sleep(2)

        self.set_video_details()

        self.wait_video_load()
        self.driver.find_element_by_class_name('vjs-big-play-button').click()
        logger.info('Waiting Video Start')
        self.wait_video_start()
        logger.info('Video Starts!')
        self.driver.find_element_by_class_name('vjs-play-control').click()
        logger.info('Video Paused')

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            return None

    async def download_parts(self):

        folder(self.tmp_folder)
        ts_folder = folder(os.path.join(self.tmp_folder, 'ts'))

        count = 1

        logger.info(f'Starting download video: {self.video_name}')

        async with aiohttp.ClientSession() as session:

            while True:

                tasks = []

                for i in range(self.io_workers):
                    task = asyncio.ensure_future(self.download_part(session, ts_folder, count))
                    tasks.append(task)
                    count += 1

                responses = await asyncio.gather(*tasks)

                works = [i for i in responses if i]

                if len(works) != self.io_workers:
                    break

    async def download_part(self, session, ts_folder, count):

        url = self.source(f'seg-{count}-v1')

        logger.info(f'Downloading Part {count}')
        logger.debug(f'Downloading URL: {url}')

        response = await self.fetch(session, url)
        if not response:
            return False

        file_name = file(f'{ts_folder}/{self.video_name}-{count}.ts')

        with open(file_name, 'wb') as f:
            f.write(response)

        self.video_list.append({
            'count': count,
            'name': file_name,
        })

        return True

    def create_list_file(self):

        video_list = [i['name'] for i in sorted(self.video_list, key=lambda k: k['count'])]
        list_name = f'{self.tmp_folder}/list.txt'

        with open(list_name, 'wb') as f:
            for i in video_list:
                f.write(f"file '{os.path.abspath(i)}'\n".encode())

        self.list_file = list_name

    def check_output_folder(self):

        if self.output:
            folder(self.output)

    def encode_video(self):

        self.check_output_folder()

        output = os.path.abspath(f'{self.output}/{self.video_name}')
        Encoder().ts_to_mp4(self.list_file, output)

    def clean_chunks(self):

        logger.info('Clearing chunks')
        logger.debug('Removing TMP Folder')

        shutil.rmtree(self.tmp_folder)

        logger.debug('Removed TMP Folder')

    def download_video(self):

        self.video_list = []

        futures = [self.download_parts()]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))

        self.create_list_file()

    def download(self, url):

        try:

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

            logger.info("Download Video in: %s seconds" % (download_end - download_start))
            logger.info("Converted Video in: %s seconds" % (converting_end - converting_start))
            logger.info("Downloading & Converting Video in: %s seconds" % (end_time - start_time))

        except Exception as error:
            logger.error(error)

            self.register_error(url, self.output)
