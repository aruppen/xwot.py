
import argparse
from xwot.compiler import Compiler

def parse_args(backends):
        parser = argparse.ArgumentParser(description='compiler - xwot compiler')
        parser.add_argument('-p', dest='platform', type=str, default='flask', choices=backends, nargs='?',
                            help='platform to use')

        parser.add_argument('-o', dest='output_dir', type=str, default='out-app', nargs='?',
                            help='name of the output directory')

        parser.add_argument(dest='xwot_file', metavar='f', type=str,
                            help='xwot file')
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = parse_args(Compiler.BACKENDS.keys())
    compiler = Compiler(input_file=args.xwot_file, output_dir=args.output_dir, platform=args.platform)
    compiler.compile()