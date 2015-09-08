
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()



def flush(args):
    print "flush"

parser = argparse.ArgumentParser()


parser_flush = subparsers.add_parser('flush')


args = parser.parse_args()
args.func(args)

