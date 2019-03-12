#!/bin/bash

# dev-tcp.sh: /dev/tcp redirection to check Internet connection.
# Script by Troy Engel.
# Used with permission.
TCP_HOST=localhost
TCP_PORT=8090

# Try to connect. (Somewhat similar to a 'ping' . . .)
#echo "HEAD / HTTP/1.0" >/dev/tcp/${TCP_HOST}/${TCP_PORT}
MYEXIT=$?


while true;
do 
if [ "X$MYEXIT" = "X0" ]; then
    echo "HEAD / HTTP/1.0" >/dev/tcp/${TCP_HOST}/${TCP_PORT}
    ffmpeg -f v4l2 -i /dev/video2 http://localhost:8090/feed1.ffm
fi
done
exit $MYEXIT
