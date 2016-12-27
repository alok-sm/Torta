cd $TRACER_PATH

# store current user for applescript
whoami > meta/user.txt

# touch the "running" file
touch running

# generate session id
openssl rand -hex 5 > meta/session.txt

# create raw_data folder
mkdir raw_data/$(cat meta/session.txt)

# create output folder
mkdir output/$(cat meta/session.txt)

# print session ID
echo "starting session ID $(cat meta/session.txt)"

sudo bash sudo_start.sh