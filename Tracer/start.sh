# store current user for applescript
whoami > user.txt

# generate session id
openssl rand -hex 5 > session.txt

sudo bash sudo_start.sh