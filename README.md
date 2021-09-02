# Alura Downloader

### Requirements
 - Python 3.6
 - [Pipenv](https://github.com/pypa/pipenv)
 - [FFmpeg](https://ffmpeg.org/download.html) 4.3

### Installing

 Follows all the steps to install the environment and run the script

 - Install Virtualenv ```pipenv install```
 - Create a ```.env``` file and define the following variables: 
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

## All Formations

### Mobile
- Android
- iOS
- Testes automatizados no Android
- Multiplataforma mobile Xamarin
- Arquitetura Android
- Flutter

### Programação:
- Java
- .NET
- Jogos com Unity
- PHP
- Wordpress
- Iniciante em Programação
- Certificação Java
- Ruby On Rails
- Expert em Orientação a Objetos
- Certificação C# Programming
- Integração de Aplicações Java
- Java EE
- VB.NET
- Clojure
- Node.JS
- Python
- Django

### Front-end:
- Acessibilidade Web
- Angular
- Vue.js
- HTML e CSS
- React JS
- Front End

### Infraestrutura:
- Administrador de Redes
- Segurança de aplicações
- Raspberry Pi
- Internet das Coisas
- Amazon Web Services
- Certificação LPI Linux Essentials
- Microcontroladores e Eletrônica Aplicada
- DevOps
- Apache Kafka
- Certificação Docker DCA

### Design & UX:
- UX Design
- Motion Design
- Design Gráfico
- Editor de vídeo
- Unreal Engine
- Produção com Photoshop
- Produção Gráfica com Illustrator
- Adobe XD
- Pintura Digital no Photoshop
- Desenho humano no Photoshop
- Ilustração Publicitária no Photoshop
- InDesign
- Sketch
- Produção de vídeo no Premiere
- UX Research
- ZBrush
- Figma

### Data Science:
- Data Science
- Machine Learning
- SQL com Microsoft SQL Server 2017
- BI e Data Warehouse com Pentaho
- BI e Data Warehouse com SQL Server e Power BI
- SQL com MySQL Server da Oracle
- SQL com Oracle Database
- Python para Data Science
- Matemática para Programação e Data Science
- Datomic
- Power BI

### Marketing Digital:
- Marketing Digital
- SEO
- Social Media

### Inovação & Gestão:
- Gerente Ágil
- Business Agility
- Desenvolvimento Pessoal
- Currículos
- Empreendedorismo Digital
- E-commerce
- Certificação ITIL Foundation
- Certificação Cobit 5
- Certificação PMP e CAPM do PMI
- Digital & Agile Thinking
- Comunicação
