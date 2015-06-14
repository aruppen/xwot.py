#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       12.04.2015

"""

import sys
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder


def main():
    if len(sys.argv) < 2:
        print "Please pass a valid file path as argument!"
        sys.exit()

    xml_file = sys.argv[1]
    description_builder = JSONLDDescriptionBuilder()
    out = description_builder.build(xml_file=xml_file, base='')

    with open(xml_file + ".jsonld", "w+") as f:
        f.write(out)

if __name__ == '__main__':
    main()
