#!/usr/bin/env bash
set -xue

export TERMUX_MUSIC=/tmp/termux_music
export TERMUX_MOVIES=/tmp/termux_movies

rm -rf $TERMUX_MOVIES
mkdir -p $TERMUX_MOVIES

echo "test video download"
URL=https://www.youtube.com/watch?v=kYfNvmF0Bqw
./termux-url-opener.py $URL
ls $TERMUX_MOVIES/*.mkv


rm -rf $TERMUX_MUSIC
mkdir -p $TERMUX_MUSIC

echo "test music download"
URL=https://music.youtube.com/watch?v=m_IhEz2sxDw
./termux-url-opener.py $URL
ls $TERMUX_MUSIC/*.mp3


echo "test pass!"
