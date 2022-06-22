from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='KlebLib',
    version='1.1.0-alpha-2',
    author='Caleb Robson',
    author_email='robson.caleb.299@gmail.com',
    packages=['KlebLib'],
    url='https://github.com/Spartan2909/KlebLib/',
    license='MIT',
    description='A collection of classes and functions that no-one will ever need.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    packages=find_packages(include=['KlebLib', 'KlebLib.*'])
)
