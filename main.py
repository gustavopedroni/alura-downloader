import click
from dotenv import load_dotenv
from src.alura import AluraDownloader
from src.types import *

load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
@click.option('-o', '--output', type=click.Path(exists=True))
@click.argument('url')
def video(url, output=None):

    app = AluraDownloader(output=output)
    app.start(url, stype=VideoType)


@cli.command()
@click.option('-o', '--output', type=click.Path(exists=True))
@click.argument('url')
def lession(url, output=None):

    app = AluraDownloader(output=output)
    app.start(url, stype=LessionType)


@cli.command()
@click.option('-o', '--output', type=click.Path(exists=True))
@click.argument('url')
def course(url, output=None):

    app = AluraDownloader(output=output)
    app.start(url, stype=CourseType)


@cli.command()
@click.option('-o', '--output', type=click.Path(exists=True))
@click.argument('url')
def formation(url, output=None):

    app = AluraDownloader(output=output)
    app.start(url, stype=FormationType)


@cli.command()
@click.option('-o', '--output', type=click.Path(exists=True))
@click.argument('f_list', type=click.File())
def formation_list(f_list, output=None):

    app = AluraDownloader(output=output)
    app.start(f_list, stype=FormationListType)


if __name__ == '__main__':

    cli()
