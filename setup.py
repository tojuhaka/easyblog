import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_zodbconn',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'ZODB3',
    'webError',
    'docutils',
    'passlib',
    'webtest',
    'pyramid_simpleform',
    'formencode',
    'nose',
    'pyramid_zcml',
    'pyramid_viewgroup',
    ]

setup(name='easyblog',
      version='0.1',
      description='easyblog',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="easyblog",
      entry_points = """\
      [paste.app_factory]
      main = easyblog:main
      """,
      )

