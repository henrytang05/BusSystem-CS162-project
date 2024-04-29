#!/bin/bash

echo "Memory usage:"
free -h | awk '/Mem:/{print "Total memory: " $2 "\nUsed memory: " $3 "\nFree memory: " $4 "\nAvailable memory: " $7}'

echo "Number of items in output/shortest_path/:"
{
	wc -l < <(ls output/shortest_path/)
	ls output/shortest_path/
}
