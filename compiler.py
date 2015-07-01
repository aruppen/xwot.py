#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       14.06.2015

"""

import argparse
import os.path
from xwot.compiler import Compiler
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder


backends = Compiler.BACKENDS.keys()
parser = argparse.ArgumentParser(description='xwot compiler')
parser.add_argument('-p', dest='platform', type=str, default='flask', choices=backends, nargs='?',
                    help='platform to use')

parser.add_argument('-o', dest='output_dir', type=str, default='out-app', nargs='?',
                    help='name of the output directory')

parser.add_argument(dest='xwot_file', metavar='f', type=str,
                    help='xwot file')
args = parser.parse_args()
compiler = Compiler(input_file=args.xwot_file, output_dir=args.output_dir, platform=args.platform)
compiler.compile()