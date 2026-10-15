#!/bin/bash
# stress-gen.sh
# Generates periodic stresses on the server's IO, CPU, filesystem, and memory

while true
do
	# stress IO
	echo "Stressing IO..."
	stress-ng --hdd 0 --timeout 15s -q
	echo "Finished IO stressing"
	systemd-notify WATCHDOG=1

	# stress CPU
	echo "Stressing CPU..."
	stress-ng --cpu 0 --timeout 15s -q
	echo "Finished CPU stressing"
	systemd-notify WATCHDOG=1

	# stress filesystem
	echo "Stressing filesystem..."
	stress-ng --dir 0 --timeout 15s -q
	echo "Finished filesystem stressing"
	systemd-notify WATCHDOG=1

	# stress memory
	echo "Stressing memory..."
	stress-ng --vm 0 --timeout 15s -q
	echo "Finished memory stressing"
	systemd-notify WATCHDOG=1
done
