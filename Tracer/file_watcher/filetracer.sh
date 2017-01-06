#!/bin/sh
/usr/sbin/dtrace -w -n '
#pragma D option quiet
#pragma D option switchrate=100hz

syscall::open*:entry
{
	self->key = rand();
	self->path = cleanpath(copyinstr(arg0));
	printf("{\"syscall\": \"open\", \"status\": \"entry\", \"key\": \"%d\", \"path\": \"%s\", \"pid\": %d}\n", self->key, self->path, pid);
}

syscall::open*:return
{
	printf("{\"syscall\": \"open\", \"status\": \"return\", \"key\": \"%d\", \"path\": \"%s\", \"pid\": %d, \"fd\": %d}\n", self->key, self->path, pid, arg0);
}

syscall::close*:entry
{
	printf("{\"syscall\": \"close\", \"status\": \"return\", \"key\": \"%d\", \"pid\": %d, \"fd\": %d}\n", rand(), pid, arg0);
}

syscall::write*:entry
{
	printf("{\"syscall\": \"write\", \"status\": \"return\", \"key\": \"%d\", \"pid\": %d, \"fd\": %d}\n", rand(), pid, arg0);
}
'
