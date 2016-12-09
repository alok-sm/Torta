# store the start time of the session
date +%s > start_time.txt

# store current user for applescript
whoami > user.txt

# generate session id
openssl rand -hex 5 > session.txt

# create results folder
mkdir results/$(cat session.txt)

# create output folder
mkdir output/$(cat session.txt)

# print session ID
echo "starting session ID $(cat session.txt)"

sudo bash sudo_start.sh