#!/usr/bin/env python3
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


LOG = logging.getLogger()
HERE = Path(__file__).parent.resolve()
MUSIC = os.getenv('TERMUX_MUSIC')
MOVIES = os.getenv('TERMUX_MOVIES')
DOWNLOADS = os.getenv('TERMUX_DOWNLOADS')


def run_cmd(cmd, cwd=None):
    str_cmd = ' '.join(cmd)
    LOG.info('running cmd: %s', str_cmd)
    try:
        subprocess.check_call(cmd, cwd=cwd)
    except subprocess.CalledProcessError as exc:
        LOG.exception('cmd raised exception')
        if exc.output:
            # output is none, but returncode is 1
            LOG.error('exception output: %s', exc.output)
            raise
        else:
            LOG.info('exception output is empty, ignore')
    LOG.info('cmd finish: %s', str_cmd)
    if cwd:
        LOG.info('cwd: %s', cwd)


def youtube_download_video(url):
    return run_cmd([
        'youtube-dlc',
        '--yes-playlist', '--ignore-errors',
        # man youtube-dlc, FORMAT SELECTION
        '--format', 'bestvideo+bestaudio',
        url,
    ], cwd=MOVIES)


def youtube_download_audio(url):
    return run_cmd([
        'youtube-dlc',
        '--yes-playlist', '--ignore-errors',
        # man youtube-dlc, FORMAT SELECTION
        '--format', 'mp3/bestaudio',
        '--extract-audio',
        '--audio-format', 'mp3',
        url,
    ], cwd=MUSIC)


def main():
    parser = argparse.ArgumentParser(description='Termux URL Opener')
    parser.add_argument('-q', '--quiet', action='store_true', help='Be quiet')
    parser.add_argument(
        '-w', '--wait-on-finish',
        dest='wait_on_finish', action='store_true',
        help='wait on finish')
    parser.add_argument('url', help='url shared to Termux')

    args = parser.parse_args()
    level = logging.ERROR if args.quiet else logging.DEBUG
    fmt = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=level, format=fmt)

    url = args.url
    LOG.info(url)

    if url.startswith(('https://www.youtube.com', 'https://youtu.be')):
        answer = input('Download audio? (y/N)')
        if answer and answer.lower() == 'y':
            youtube_download_audio(url)
        else:
            youtube_download_video(url)
    elif url.startswith('https://music.youtube.com'):
        youtube_download_audio(url)
    elif url.startswith('https://play.google.com/store/apps'):
        parse_result = urlparse(url)
        params = parse_qs(parse_result.query)
        run_cmd([
            'gplaycli', '--verbose', '--yes', '--append-version', '--progress',
            '--config', str(HERE/'gplaycli.conf'),
            '--download', params['id'][0],
        ], cwd=DOWNLOADS)
    else:
        LOG.error('sorry, unable to handle url: %s', url)
    if args.wait_on_finish:
        # termux will be close, sleep for user to read output
        input('press any key to continue...')


if __name__ == '__main__':
    main()
