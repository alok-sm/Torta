cd $TRACER_PATH/

# store the end time of the session
date +%s > end_time.txt

rm running

sudo bash sudo_end.sh

python postprocess.py $(cat session.txt)