#!/bin/sh
  
sleep_time="$1";

ls, -l, /
sh, -xc, "echo $(date) ': hello world!'"
sh, -c, echo "=========hello world'========="
echo "hello" > /home/cldtest
sleep "$sleep_time"