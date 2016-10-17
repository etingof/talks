#!/bin/bash

for s in slides
do
  rst2html5 --jquery --reveal-js --reveal-js-opts theme=white,progress=true,transition=none --pretty-print-code ${s}.rst > ${s}.html
done
