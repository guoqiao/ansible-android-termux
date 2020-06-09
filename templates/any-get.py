#!/usr/bin/env python3
"""Termux URL Opener

On Android, share URL to Termux, it will be processed by this script.

- YouTube: download video
- Google Play: download apk
"""

import argparse
import logging
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs


LOG = logging.getLogger(__name__)

HOME = Path(__file__).home()
VIDEO = HOME / 'Video'
MUSIC = HOME / 'Music'
IMAGE = HOME / 'Pictures'
DOWNLOAD = HOME / 'Download'


def run_cmd(cmd):
    str_cmd = ' '.join(cmd)
    LOG.info('cmd start: %s', str_cmd)
    subprocess.check_call(cmd)
    LOG.info('cmd finish: %s', str_cmd)


def main():
    parser = argparse.ArgumentParser(
        description='Termux URL Opener',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)

    parser.add_argument(
        '-q', '--quiet', action='store_true', help='Be quiet')

    parser.add_argument(
        'url', help='url shared to Termux')

    args = parser.parse_args()

    level = logging.ERROR if args.quiet else logging.DEBUG
    fmt = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    logging.basicConfig(level=level, format=fmt)

    url = args.url
    LOG.info(url)

    if url.startswith(('https://www.youtube.com', 'https://youtu.be')):
        run_cmd([
            'youtube-dl',
            '--format', 'best',
            '--output', f'{VIDEO}/%(title)s.%(ext)s',
            url,
        ])
    elif url.startswith('https://music.youtube.com'):
        run_cmd([
            'youtube-dl',
            '--format', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--output', f'{MUSIC}/%(artist)s/%(title)s.%(ext)s',
            url,
        ])
    elif url.startswith('https://play.google.com/store/apps'):
        parse_result = urlparse(url)
        params = parse_qs(parse_result.query)
        run_cmd([
            'gplaycli', '--verbose', '--yes', '--append-version', '--progress',
            '--config', HOME / 'gplaycli.conf',
            '--download', params['id'][0], '--folder', DOWNLOAD,
        ])
    else:
        LOG.error('sorry, unable to handle url: %s', url)
    # termux will be close, sleep for user to read output
    input('press any key to continue...')


if __name__ == '__main__':
    main()
