from setuptools import setup, find_packages

setup(
    name='giraffe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here, e.g.,
        # 'somepackage>=1.0',
    ],
    entry_points={
        'console_scripts': [
            # If you have any command-line scripts, you can define them here
            # 'myframework=myframework.cli:main',
        ],
    },
    python_requires='>=3.6',
    author='Your Name',
    author_email='your.email@example.com',
    description='A custom web framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/myframework',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)