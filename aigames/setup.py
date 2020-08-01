
from setuptools import setup, find_packages
from aigames.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='aigames',
    version=VERSION,
    description='Basic games with AI',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alan Lo',
    author_email='john.doe@example.com',
    url='https://github.com/johndoe/myapp/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'aigames': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        aigames = aigames.main:main
    """,
)
