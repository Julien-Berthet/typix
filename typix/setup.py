from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    readme = readme.read()

setup(
    name = 'typix',
    version = '1.0.0',
    author = 'Julien BERTHET',
    author_email = 'julienberthet00@gmail.com',
    description = 'An advanced module to hide type handling code behind type annotations',
    packages = find_packages(),
    long_description = readme,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    license = 'MIT'
)