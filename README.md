openev2
-------

This is a version of the openev2 source tree from sourceforge imported into git
and somewhat fixed for building on Ubuntu 14-ish. There's still some problems
to work through but it at least can open and display geotiffs.

Thanks to @sanak on github for doing the git import and some hints on making
the build work.


Installing
--------

1a) sudo apt-get install python-software-properties
1b) sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
1c) sudo apt-get update

2) sudo apt-get install python-gdal  (you might need more than this, but it's a start)

3) cd openev2/src && make install && cd ..

4) sudo python setup.py install

`openev2` should now be installed system-wide, in /usr/local.

