# xwot.py

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


## Compiler
The xwot compiler uses popular micro web frameworks to generate a skeleton application
for different programming platforms such as:

 * ruby
 * python
 * nodejs

Currently there are three basic backends implemented for:

 * [sinatra](http://www.sinatrarb.com/)
 * [flask](http://flask.pocoo.org/)
 * [express.js](http://expressjs.com/)

## Usage

```bash
usage: Compiler.py [-h] [p] f

```

Options:

 * p: platform - can be express, sinatra or flask
 * f: enhanced xwot file - used to generate the code

## Example Usage

```bash
python Compiler.py  flask smart-room-example_enhanced.xwot

```