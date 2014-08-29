openev2
-------

This is a version of the openev2 source tree from sourceforge imported into git
and somewhat fixed for building on Ubuntu 14-ish. There's still some problems
to work through but it at least can open and display geotiffs.

Thanks to @sanak on github for doing the git import and some hints on making
the build work.


Installing
--------

1. sudo apt-get install python-software-properties
2. sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
3. sudo apt-get update

4. sudo apt-get install python-gdal  (you might need more than this, but it's a start)

5. cd openev2/src && make install && cd ..

6. sudo python setup.py install

`openev2` should now be installed system-wide, in /usr/local.

