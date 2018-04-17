from setuptools import setup, find_packages

setup(
    name='doodle-dashboard',
    version='0.0.3',
    description='Extensible dashboard designed to display data from multiple sources.',
    url='https://github.com/SketchingDev/Doodle-Dashboard',
    license = 'MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'slackclient',
        'feedparser',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['doodledashboard=doodledashboard.command_line:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    python_requires='>=3.6'
)
