#!/bin/bash


if [ "$#" -ne 1 ]; then
    outfile='log.txt'
else
    outfile="$1"
fi

printf "**** LIST OF PROCESS ****\n" > "$outfile"
#get the process
ps aux >> "$outfile"


printf "\n" >> $outfile
printf "**** PSTREE ****\n" >> $outfile
pstree >> $outfile

printf "\n" >> $outfile
printf "**** NETSTAT ****\n" >>$outfile
netstat -a >> $outfile

printf "\n" >> $outfile
printf "**** VMSTAT ****\n" >> $outfile
vmstat >> $outfile

printf "\n" >> $outfile
printf "**** IOSTAT ****\n" >> $outfile
iostat >> $outfile

printf "\n" >> $outfile
printf "**** FREE ****\n" >> $outfile
free >> $outfile

printf "\n" >> $outfile
printf "**** DF ****\n" >> $outfile
df >> $outfile

printf "\n" >> $outfile
printf "**** DMESG **** \n" >> $outfile
dmesg >> $outfile


