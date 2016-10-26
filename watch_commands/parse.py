import sys
import os

prompt = sys.argv[1].decode('string_escape')
print "prompt", prompt
session_text = open('typescript').read()

print session_text.encode('string_escape')