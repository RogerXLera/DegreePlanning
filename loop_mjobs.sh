#!/bin/bash

# Use mapfile to read lines into an array
mapfile -t lines < "data/jobs_instances.txt"

count=0
# Print the array elements
for line in "${lines[@]}"; do
  echo $line
  python3 problem.py -j $line > "solutions2/sol-$count.txt"
  count=$((count+1))
done
