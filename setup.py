from setuptools import setup, find_packages

version = '0.4.3'

setup(name="helga-twitter",
      version=version,
      description=('twitter via irc'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='helga twitter',
      author='Justin Caratzas',
      author_email='bigjust@lambdaphil.es',
      url='https://github.com/bigjust/helga-twitter',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      py_modules=['helga_twitter'],
      zip_safe=True,
      entry_points = dict(
          helga_plugins = [
              'twitter = helga_twitter:TwitterPlugin',
          ],
      ),
      install_requires = (
          'tweepy'
      ),
)
