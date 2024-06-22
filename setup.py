from setuptools import setup, find_packages

setup(
    name='giraffe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    author='Torben Petré (kipteamm)',
    author_email='contact@kipteam.net',
    description='A simple web framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kipteamm/giraffe',
    entry_points={
        'console_scripts': [
            'giraffe=giraffe.core.cli:main',
        ],
    },
)
