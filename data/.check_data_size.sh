#!/usr/bin/env bash

# Do NOT change this file!


if [ "$(du -k `dirname $0` | cut -f1)" -gt 1024 ]; then
    echo "ERROR: data directory total size must be less than 1MB!"
    exit 1
fi
