import os

from src.helpers.logging import get_logger

logger = get_logger('Encoder')


class Encoder:

    @staticmethod
    def run_command(command):
        logger.debug(command)

        os.system(command)

    def ts_to_mp4(self, file_list, output):
        logger.info('Starting Conversion')
        file_list = os.path.abspath(file_list)

        command = f'ffmpeg -f concat -safe 0 -i "{file_list}" -c copy "{output}.ts"'

        logger.info('Aggregating Videos')
        self.run_command(command)
        logger.info('Videos Aggregated')
        command = f'ffmpeg -i "{output}.ts" -acodec copy -vcodec copy "{output}.mp4"'

        logger.info('Converting Video to MP4')
        self.run_command(command)
        logger.info('Converted Video to MP4')

        logger.info(f'File: {output}.mp4')
