from setuptools import setup, find_packages

# https://caremad.io/posts/2013/07/setup-vs-requirement/
setup(
    name='Doodle Dashboard',
    version='0.1',
    description='Extensible dashboard designed to display data from multiple sources.',
    url='https://github.com/SketchingDev/Doodle-Dashboard',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['doodledashboard=doodledashboard.command_line:main'],
    }
)
