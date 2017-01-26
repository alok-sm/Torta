#!/bin/sh
/usr/sbin/dtrace -w -n '
#pragma D option quiet
#pragma D option switchrate=100hz

syscall::open*:entry
{
	self->key = rand();
	self->path = cleanpath(copyinstr(arg0));
	printf("{\"timestamp\": %d, \"syscall\": \"open\",   \"status\": \"entry\",  \"key\": \"%d\", \"pid\": %d, \"path\": \"%s\"}\n", walltimestamp/1000000000, self->key, pid, self->path);
}

syscall::open*:return
{
	printf("{\"timestamp\": %d, \"syscall\": \"open\",   \"status\": \"return\", \"key\": \"%d\", \"pid\": %d, \"path\": \"%s\", \"fd\": %d}\n", walltimestamp/1000000000, self->key, pid, self->path, arg0);
	//system("bash getcwd.sh %d cwd_log.txt &", pid)
}

syscall::close*:entry
{
	printf("{\"timestamp\": %d, \"syscall\": \"close\",  \"status\": \"entry\",  \"key\": \"%d\", \"pid\": %d, \"fd\": %d}\n", walltimestamp/1000000000, rand(), pid, arg0);
	//system("bash getcwd.sh %d cwd_log.txt &", pid)
}

syscall::write*:entry
{
	printf("{\"timestamp\": %d, \"syscall\": \"write\",  \"status\": \"entry\",  \"key\": \"%d\", \"pid\": %d, \"fd\": %d}\n", walltimestamp/1000000000, rand(), pid, arg0);
	//system("bash getcwd.sh %d cwd_log.txt &", pid)
}

syscall::unlink*:entry
{
	printf("{\"timestamp\": %d, \"syscall\": \"unlink\", \"status\": \"entry\",  \"key\": \"%d\", \"pid\": %d, \"path\": \"%s\"}\n", walltimestamp/1000000000, rand(), pid, cleanpath(copyinstr(arg0)));
	//system("bash getcwd.sh %d cwd_log.txt &", pid)
}

syscall::rename*:entry
{
	printf("{\"timestamp\": %d, \"syscall\": \"rename\", \"status\": \"entry\",  \"key\": \"%d\", \"pid\": %d, \"old_path\": \"%s\", \"new_path\": \"%s\"}\n", walltimestamp/1000000000, rand(), pid, cleanpath(copyinstr(arg0)), cleanpath(copyinstr(arg1)));
	//system("bash getcwd.sh %d cwd_log.txt &", pid)
}
'
