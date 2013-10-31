import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'MadeToMeasure',
    ]

setup(name='m2m_groups',
      version='0.1dev',
      description='m2m_groups',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Made to Measure development team',
      author_email='robin@betahaus.net',
      url='https://github.com/GlobalActionPlan/m2m_groups',
      keywords='web pyramid pylons MadeToMeasure',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="m2m_groups",
      entry_points="""\
      """,
      )
