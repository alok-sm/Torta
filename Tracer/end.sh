# store the end time of the session
date +%s > end_time.txt

sudo bash sudo_end.sh

python postprocess.py $(cat session.txt)