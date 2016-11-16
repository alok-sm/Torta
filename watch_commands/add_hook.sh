source log_lib.sh

# preexec_log() { echo "[$(date)] $*" >> log.txt }
# preexec_functions+=(preexec_log)

preexec_log() { echo "{\"ts\": \"$(date)\", \"user\": \"$(whoami)\", \"host\": \"$(hostname)\", \"pwd\": \"$(pwd)\", \"cmd\": \"$*\"}" >> log.txt; }





# Add it to the array of functions to be invoked each time.
preexec_functions+=(preexec_log)
