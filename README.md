# xwot.py

xwot.py is a collection of Python tools for developing xWoT web applications based on the [xWoT meta-model](http://diuf.unifr.ch/drupal/sites/diuf.unifr.ch.drupal.softeng/files/file/publications/ruppena/meta-model.pdf)
introduced by Andreas Ruppen and Jacques Pasquier.

For more details visit the website of the [Software Engineering Research Group / University of Fribourg](https://diuf.unifr.ch/drupal/softeng/).

Content:
 * xwot.compiler - compiler for generating a skeleton xWoT web application based on the xWoT meta-model
   * xwot.compiler.backend - different backends
   * xwot.compiler.frontend - visitor, parser, description builder and processing tools
 * xwot.device - example xwot devices (weather station, water dispenser, light bulb, door, window)
 * xwot.i2c.adapter - i2c adapters for xwot devices
 * xwot.model - xwot models
 * xwot.cmd - set of xwot commands like xwotc (compiler), xwotd (description builder)



## Installation

### Dependencies

* build-essential
* libffi-dev
* python-dev
* python-pip
* python-smbus
* i2c-tools
* libi2c-dev

```
sudo apt-get install python-pip python-dev build-essential libffi-dev python-smbus i2c-tools libi2c-dev
```

### from source
```
git clone https://github.com/lexruee/xwot.py
cd xwot.py
sudo python setup.py install
```

### pip installer

```
sudo pip install xwot-py
```

## xWoT Commands

### xwotc: xwot compiler
The xwot compiler uses popular micro web frameworks to generate a skeleton application
for different programming platforms such as:

 * ruby
 * python
 * nodejs

Currently there are four basic backends available:

 * [sinatra / ruby](http://www.sinatrarb.com/)
 * [flask / python](http://flask.pocoo.org/)
 * [klein / python](http://klein.readthedocs.org/)
 * [express.js / node.js](http://expressjs.com/)

#### Usage

```bash
usage: xwotc [-h] [-p [{flask,sinatra,express,klein}]] [-o [OUTPUT_DIR]] f

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


### xwotd: xwot description builder
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
xwotd flask smart-room-example_enhanced.xwot description.jsonld
```


## License & Copyright

```
xwot.py  - Python tools for the extended Web of Things
Copyright (C) 2015  Alexander Rüedlinger
Copyright (C) 2015  Andreas Ruppen

xwot.py is licensed under the GPL 3.0.

```
