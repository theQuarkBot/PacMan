#!/bin/bash

rm *.ps

for file in *.py;
do
    filename=`basename $file .py`
    a2ps $file -o $filename.ps
done