#!/bin/bash
# this script will setup the virtual environment for developing 

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PYTHON=`which python2.7`
OUTDIR=python
while getopts "hd:s" OPTION; 
do 
  case $OPTION in 
h) echo "Usage: $0 [-d directory] [-s]"
   exit 1
   ;;
s) SELENIUM="no"; 
   ;;
d) OUTDIR="$OPTARG"
   ;;
  esac
done
echo "OUTDIR: $OUTDIR"

$PYTHON "$DIR"/virtualenv.py "$OUTDIR"
"$OUTDIR/bin/easy_install" -U setuptools
#"$OUTDIR/bin/pip" install --upgrade SQLAlchemy==0.9.3
#"$OUTDIR/bin/pip" install --upgrade alembic==0.5.0
"$OUTDIR/bin/pip" install --upgrade numpy==1.9
"$OUTDIR/bin/pip" install --upgrade matplotlib==1.4.2
"$OUTDIR/bin/pip" install --upgrade jinja2==2.7
"$OUTDIR/bin/pip" install --upgrade scipy==0.14.0
