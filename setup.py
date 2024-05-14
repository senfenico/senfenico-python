from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='senfenico',
    version='0.2.1',

    description="Python bindings for the Senfenico API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Senfenico",
    author_email="contact@senfenico.com",
    url="https://github.com/senfenico/senfenico-python",
    license="MIT",
    keywords="Senfenenico api payments",

    project_urls={
        "Bug Tracker": "https://github.com/senfenico/senfenico-python/issues",
        "Documentation": "https://docs.senfenico.com/en/",
        "Source Code": "https://github.com/senfenico/senfenico-python",
    },
    packages=find_packages(),
    install_requires=[
        'requests', 
    ]
)