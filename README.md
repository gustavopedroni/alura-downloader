# Alura Downloader

### Requirements
 - Python 3.6
 - [Pipenv](https://github.com/pypa/pipenv)
 - [FFmpeg](https://ffmpeg.org/download.html) 4.3
 - [Chromium Driver](https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/)

### Installing

 Follows all the steps to install the environment and run the script

 - Install Virtualenv ```pipenv install```
 - Create a ```.env``` file and define the following variables: 
    - ```CHROMIUM_DRIVER``` - Localization of chrome driver
    - ```ALURA_USER``` - Alura username or email
    - ```ALURA_PASS``` - Alura password
 
 
 ### Using
 
 ###### OBS: All videos are downloaded in .MP4
 
```
 ☤ Usage
 $ python main.py
 Usage: python [OPTIONS] video_url

 Options:
   -f or --formation_url | Specifying a Formation
   -c or --course_url | Specifying a Course
   -l or --lesson_url | Specifying a Lesson
   -v or --video_url | Specifying a Video
   -o or --output | Specifying a folder to all videos output

 Usage Examples:
   Specifying a folder to download all formation videos:
   $ python main.py -f https://cursos.alura.com.br/formacao-devops -o D:\Alura

   Specifying download all course videos on default folder:
   $ python main.py -c https://cursos.alura.com.br/course/linux-ubuntu

   Specifying download all lesson videos on default folder:
   $ python main.py -l https://cursos.alura.com.br/course/linux-ubuntu/section/1436/tasks

   Download a alura video:
   $ python main.py https://cursos.alura.com.br/course/linux-ubuntu/task/3216

   or 

   $ python main.py -v https://cursos.alura.com.br/course/linux-ubuntu/task/3216
```