cd $TRACER_PATH/

rm running

sudo bash sudo_end.sh

python postprocess.py $(cat meta/session.txt)