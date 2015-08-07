
DeDupe
======

**Dedupe** is an algorithm to find near duplicates in an m-dimensional featureset with an O(mnlog(n)) runtime.

Inspiration
-----------

Removing near duplicates from an SQL table.

Download
--------

Download the repository with git:
```
    $ git clone https://github.com/nliolios24/dedupe
```
Then create an image and run with Docker
```
    $ docker build -rm -t dedupe .
    $ docker run dedupe
```