#!/bin/bash
CATEGORY=$1
TITLE=$2

if [ -z "$1" -o -z "$2" ]; then
    echo "Usage:"
    echo "mkpost.sh [category] [title]"
fi

NAME=`echo -n $TITLE | sed -e "s/ /-/g" | awk '{print tolower($0)}'`
TIME=`date --utc '+%Y-%d-%m %H:%M'`
DATE=`echo ${TIME%% *}`
POST=src/$CATEGORY/$DATE-$NAME.md

mkdir -p "src/$CATEGORY"
touch "$POST"

echo "Title: $TITLE" >> "$POST"
echo "Date: $TIME" >> "$POST"
echo "Tags:" >> "$POST"

echo "Created post:"
echo "$POST"
