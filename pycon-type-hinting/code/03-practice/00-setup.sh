#!/bin/bash

cd /tmp

wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0b2.tgz

tar zxf Python-3.6.0b2.tgz && \
    cd Python-3.6.0b2 && \
    ./configure && \
    make && \
    sudo make install

python3.6 -m venv venv
source venv/bin/activate
pip install mypy-lang typed_ast

git clone https://github.com/etingof/talks/tree/master/pycon-type-hinting
