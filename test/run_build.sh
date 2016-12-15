#!/bin/bash

PYTHON=$(which python)
VERSION=$($PYTHON -V 2>&1 | cut -d' ' -f2)

echo "test requirements"

[ -x "$PYTHON" ] && {
    echo "python seems to be installed"
} || {
    echo "python is missing..."
    exit 1
}

pip install --upgrade pip
pip install -r requirements.txt
pip install wheel

echo "building dist"
[ "$(sed 's/\([[:digit:]]*\)\..*$/\1/' <<<$VERSION)" -eq 2 ] && $PYTHON setup.py sdist bdist_wheel
$PYTHON setup.py bdist_egg

echo "publishing build"
cd dist
tgz=$(ls -1rt dist/burp-ui*.tar.gz | grep -v burp-ui.dev.tar.gz | tail -1)
egg=$(ls -1rt dist/burp_ui*.egg | grep -v burp_ui-dev-py | tail -1)
whl=$(ls -1rt dist/burp_ui*.whl | grep -v burp_ui-dev-py2.py3-none-any.whl | tail -1)
cd ..
cp -vf dist/burp-ui*.tar.gz /pub/ 2>/dev/null
cp -vf dist/burp_ui*.egg /pub/ 2>/dev/null
cp -vf dist/burp_ui*.whl /pub/ 2>/dev/null

cd /pub
rm burp-ui.dev.tar.gz burp_ui-dev-py${VERSION}.egg burp_ui-dev-py2.py3-none-any.whl 2>/dev/null
ln -sf $tgz burp-ui.dev.tar.gz
ln -sf $egg burp_ui-dev-py${VERSION}.egg
ln -sf $whl burp_ui-dev-py2.py3-none-any.whl

exit 0
