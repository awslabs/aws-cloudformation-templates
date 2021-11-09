"""
This script transforms a CloudFormation YAML element into its JSON equivalent.
This is useful when the CloudFormation does not accept a YAML element and you 
still want to write it down as YAML in order to make it more readable.
"""

from app import lambda_handler
from argparse import ArgumentParser, RawTextHelpFormatter
from functools import partial
import json
import logging
import sys


logging.basicConfig(format='%(asctime)s | %(levelname)-5s | %(module)s:%(lineno)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger()


def parse_command_line():
    parser = ArgumentParser(
        prog='yaml2json', description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run the program in debug mode',
        default=False)
    parser.add_argument('--event', help='The event file', required=True)
    parser.add_argument('--output', help='The output file. Default to STDOUT', required=False, default=None)
    parser.set_defaults(func=partial(_general_help, parser))
    return parser.parse_args()


def _general_help(parser, _):
    parser.print_help(sys.stderr)


def main():
    try:
        args = parse_command_line()
        if args.debug:
            logger.setLevel(logging.DEBUG)
        logger.debug(f"Processing event {args.event}...")
        with open(args.event) as json_file:
            response = lambda_handler(json.load(json_file), None)
            res_str = json.dumps(response, indent=2)
            if args.output:
                with open(args.output, 'w') as output_file:
                    output_file.write(res_str)
            else:
              print(res_str)
        return 0
    except ValueError as e:
        logging.error(e)
        return 1
    except Exception as e:
        logging.error(e, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
