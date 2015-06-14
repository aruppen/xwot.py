# xwot.py

This repository contains handy tools for the [xWoT meta-model](http://diuf.unifr.ch/drupal/sites/diuf.unifr.ch.drupal.softeng/files/file/publications/ruppena/meta-model.pdf)
introducded by Andreas Ruppen and Jacques Pasquier.

xwot.py is a python package for creating xWoT web applications.
It features among others some handy tools and some example xwot models:
 * xwot.compiler - compiler which generates a skeleton xWoT web application based on the xWoT meta-model
 * xwot.util - utilities such as hydra annotator for creating hypermedia driven APIs
 * xwot.model - some implemented xwot models (weatherstation, plant, lightbulb, door)
 * xwot.cmd - set of xwot commands like xwotc (compiler), xwotd (description builder)



## Installation

### from source
```
git clone https://github.com/lexruee/xwot.py
cd xwot.py
sudo python setup.py install
```

### pip installer

```
sudo pip install xwot
```

## Commands

### xwot compiler - xwotc
The xwot compiler uses popular micro web frameworks to generate a skeleton application
for different programming platforms such as:

 * ruby
 * python
 * nodejs

Currently there are three basic backends implemented for:

 * [sinatra](http://www.sinatrarb.com/)
 * [flask](http://flask.pocoo.org/)
 * [express.js](http://expressjs.com/)

#### Usage

```bash
usage: xwotc [-h] [-p [{flask,sinatra,express}]] [-o [OUTPUT_DIR]] f

xwot compiler

positional arguments:
  f                     xwot file

optional arguments:
  -h, --help            show this help message and exit
  -p [{flask,sinatra,express}]
                        platform to use
  -o [OUTPUT_DIR]       name of the output directory

```

Options:

 * p: platform - can be express, sinatra or flask
 * f: enhanced xwot file - used to generate the code

#### Example

```bash
xwotc  flask smart-room-example_enhanced.xwot

```


### xwot description builder - xwotd
The xwot description builder takes as argument a xwot xml file and generates a lightweight
device description file in the jsonld format.

#### Usage
```
usage: xwotd [-h] [-o [OUTPUT_FILEPATH]] xwot file

xwot description builder

positional arguments:
  xwot file             a xwot file

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT_FILEPATH]  path of the output file

```


#### Example

```
xwotd  flask smart-room-example_enhanced.xwot description.jsonld
```