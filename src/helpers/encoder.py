import os
import subprocess


def ts_to_mp4(file_list, output):
    print('TS to MP4: Creating Mp4 File')
    file_list = os.path.abspath(file_list)

    command = f'ffmpeg -f concat -safe 0 -i "{file_list}" -c copy "{output}.ts"'

    subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    ).wait()

    print('TS to MP4: Grouping Files')

    command = f'ffmpeg -i "{output}.ts" -acodec copy -vcodec copy "{output}.mp4"'

    subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    ).wait()
    print('TS to MP4: Finished')
