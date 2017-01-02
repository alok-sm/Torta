#!/bin/sh
/usr/sbin/dtrace -w -n '
#pragma D option quiet

syscall::open:entry, syscall::open_nocancel:entry, syscall::open_extended:entry
{
	key = rand();
	path = cleanpath(copyinstr(arg0));
	printf("{\"syscall\": \"open\", \"status\": \"entry\", \"key\": \"%d\", \"path\": \"%s\", \"pid\": %d}\n", key, path, pid);

	self->pathp = arg0;
	self->key = key;
}

syscall::open:return, syscall::open_nocancel:return, syscall::open_extended:return
{
	path = cleanpath(copyinstr(self->pathp));
	key = self->key;

	printf("{\"syscall\": \"open\", \"status\": \"return\", \"key\": \"%d\", \"path\": \"%s\", \"pid\": %d, \"fd\": %d}\n", key, path, pid, arg0);

}

syscall::close:return, syscall::close_nocancel:return
{
	printf("{\"syscall\": \"close\", \"status\": \"return\", \"pid\": %d, \"fd\": %d}\n", pid, arg0);
}
'
