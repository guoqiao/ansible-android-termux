#!/data/data/com.termux/files/usr/bin/python
"""Termux URL Opener

On Android, share URL to Termux, it will be processed by this script.

- YouTube: download video
- YouTube Music: download music as mp3
- Google Play: download apk
"""

import os
import argparse
import logging
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs


LOG = logging.getLogger(__name__)
CWD = os.getcwd()
HERE = Path(__file__).parent.resolve()
MUSIC = os.getenv('TERMUX_MUSIC', default=CWD)
MOVIES = os.getenv('TERMUX_MOVIES', default=CWD)
DOWNLOADS = os.getenv('TERMUX_DOWNLOADS', default=CWD)


def run_cmd(cmd, cwd=None):
    str_cmd = ' '.join(cmd)
    LOG.info('running cmd: %s', str_cmd)
    subprocess.check_call(cmd, cwd=cwd)
    LOG.info('cmd finish: %s', str_cmd)


def main():
    parser = argparse.ArgumentParser(description='Termux URL Opener')
    parser.add_argument('-q', '--quiet', action='store_true', help='Be quiet')
    parser.add_argument('url', help='url shared to Termux')

    args = parser.parse_args()
    level = logging.ERROR if args.quiet else logging.DEBUG
    fmt = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    logging.basicConfig(level=level, format=fmt)

    url = args.url
    LOG.info(url)

    if url.startswith(('https://www.youtube.com', 'https://youtu.be')):
        run_cmd(['youtube-dlc', url], cwd=MOVIES)
    elif url.startswith('https://music.youtube.com'):
        run_cmd([
            'youtube-dlc',
            '--format', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            url,
        ], cwd=MUSIC)
    elif url.startswith('https://play.google.com/store/apps'):
        parse_result = urlparse(url)
        params = parse_qs(parse_result.query)
        run_cmd([
            'gplaycli', '--verbose', '--yes', '--append-version', '--progress',
            '--config', str(HERE/'gplaycli.conf'),
            '--download', params['id'][0], '--folder', str(DOWNLOADS),
        ])
    else:
        LOG.error('sorry, unable to handle url: %s', url)
    # termux will be close, sleep for user to read output
    input('press any key to continue...')


if __name__ == '__main__':
    main()
