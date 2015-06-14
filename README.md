# xWoT-base

xwot-base is a set of tools for creating xWoT web applications:
 * xwot.compiler - compiler which generates a skeleton xWoT web application based on the xWoT meta-model
 * xwot.util - utilities such as hydra annotator for creating hypermedia driven APIs
 * xwot.model - some implemented xwot models (weatherstation, plant, lightbulb, door)


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