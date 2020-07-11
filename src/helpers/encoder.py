import os
import subprocess
import time

from src.helpers.logging import get_logger

logger = get_logger('Encoder')


class Encoder:

    @staticmethod
    def run_command(command):

        logger.debug('Converted Video to MP4')

        subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        ).wait()

    def ts_to_mp4(self, file_list, output):

        logger.info('Starting Conversion')
        file_list = os.path.abspath(file_list)

        command = f'ffmpeg -f concat -safe 0 -i "{file_list}" -c copy "{output}.ts"'

        logger.info('Aggregating Videos')
        self.run_command(command)
        logger.info('Aggregated Videos')
        command = f'ffmpeg -i "{output}.ts" -acodec copy -vcodec copy "{output}.mp4"'

        logger.info('Converting Video to MP4')
        self.run_command(command)
        logger.info('Converted Video to MP4')

        logger.info(f'File: {output}.mp4')
