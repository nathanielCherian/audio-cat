import argparse 
import sys

from .utils import download_youtube_audio


def main():

    parser = argparse.ArgumentParser(prog='audio-supervisor', 
        description ='manipulate audio.', 
        usage='%(prog)s [command]', 
        epilog='read the docs!', 
        allow_abbrev=False,
        add_help=True)

    parser.version= '0.1'


    subparsers = parser.add_subparsers(help='commands')

    dl_parser = subparsers.add_parser('download', help='download audio from youtube')
    dl_parser.add_argument('url', action='store', help='youtube video url')
    dl_parser.add_argument('title', action='store', help='stored title')
    dl_parser.add_argument('--des', action='store', help='destination default=audio')
    dl_parser.add_argument('--split', action='store', help='split interval default=2500', type=int)
    dl_parser.add_argument('--blurb', action='store', help='full audio storage default=FULL_AUDIO')
    dl_parser.add_argument('--dry', action='store_true')


    parser.add_argument("--version", action='version', help="display program version")



    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.dry is None:

        if sys.argv[1] == 'download':
                print(download_youtube_audio(args.url, args.title))

    else:
        print(args, "DRY")
