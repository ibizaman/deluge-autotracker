#!/nix/store/5n8r5fgscx6f5ifmqqpd8gxjf44a0y2l-bash-5.1-p16/bin/bash
BASEDIR=$(cd `dirname $0` && pwd)
CONFIG_DIR=$( test -z $1 && echo "/home/timi/Projects/deluge-autotracker/.config" || echo "$1")
[ -d "$CONFIG_DIR/plugins" ] || echo "Config dir "$CONFIG_DIR" is either not a directory or is not a proper deluge config directory. Exiting"
[ -d "$CONFIG_DIR/plugins" ] || exit 1
cd $BASEDIR
test -d $BASEDIR/temp || mkdir $BASEDIR/temp
export PYTHONPATH=$BASEDIR/temp
python3.9 setup.py build develop --install-dir $BASEDIR/temp
cp $BASEDIR/temp/*.egg-link $CONFIG_DIR/plugins
rm -fr $BASEDIR/temp
