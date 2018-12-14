from setuptools import setup, find_packages
version = '0.1'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='mr.wheelwright',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Buildout",
      ],
      keywords='Plone',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'mr.developer',
      ],
      extras_require=dict(
          test=[
          ]),
      entry_points="""
      [mr.developer.commands]
      wheels = mr.wheelwright.commands:CmdBuildWheels
      """)
