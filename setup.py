try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='python-bigcommerce',
      version='0.1',
      description='Integration library for BigCommerce',
      author='Coleman Stevenson',
      author_email='cole@imakethe.com',
      url='http://github.com/clean-cole/python-bigcommerce',
      license="MIT License",
      install_requires=['requests>=1.0'],
      tests_require=['mock', 'nose'],
      packages=['bigcommerce'],
      platforms='any',
      classifiers=[
          'Development Status :: 1 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
     )

