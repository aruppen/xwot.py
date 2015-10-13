#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot.py - Python tools for the extended Web of Things
# Copyright (C) 2015  Alexander Rüedlinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Alexander Rüedlinger'

import argparse
from xwot.compiler import Compiler
import sqlite3
import os


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

conn = sqlite3.connect(os.path.join(args.output_dir,'clients.db'))
conn.execute('CREATE TABLE if not exists "Resource" (id integer primary key autoincrement, name text);')
conn.execute('CREATE TABLE if not exists "SensorEvent" (id integer primary key autoincrement, data text, subscriberid int);')
conn.execute('CREATE TABLE if not exists "Subscriber" (id integer primary key autoincrement, uri text, method text, accept text, resourceid int);')
conn.commit()
conn.close()
