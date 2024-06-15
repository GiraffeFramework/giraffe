from setuptools import setup, find_packages

setup(
    name='giraffe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here, e.g.,
        # 'somepackage>=1.0',
    ],
    python_requires='>=3.6',
    author='Torben Petré (kipteamm)',
    author_email='contact@kipteam.net',
    description='A simple web framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kipteamm/giraffe',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
