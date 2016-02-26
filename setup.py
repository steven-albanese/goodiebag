from setuptools import setup

VERSION = 0.1
__version__ = VERSION

setup(name='goodiebag',
      version=__version__,
      description='small molecule targeted kinase inhibitors',
      url='https://github.com/juliebehr/goodiebag',
      author='Julie M. Behr',
      author_email='julie.behr@choderalab.org',
      packages=['goodiebag','goodiebag.approved','goodiebag.intrials','goodiebag.kinases','goodiebag.tests'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
)
