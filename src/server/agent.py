# agent.py
# Collects usage statistics and forwards them to the named pipe "usage-stats.fifo".

import psutil, time, os, errno, json

PIPE = "/home/sutwilterdink/linux-iod/src/server/usage-stats.fifo"

def main()->None:
	_io1 = psutil.disk_io_counters()
	_cpu = psutil.cpu_percent(interval=1)
	_io2 = psutil.disk_io_counters()
	usage = {
		"time": time.time(),
		"cpu": _cpu,
		"vm": psutil.virtual_memory().percent,
		"disk": psutil.disk_usage("/").percent,
		"io_r": _io2.read_bytes - _io1.read_bytes,
		"io_w": _io2.write_bytes - _io1.write_bytes,
	}
	# write to pipe
	try: pipe = os.open(PIPE, os.O_WRONLY | os.O_NONBLOCK)
	except OSError as e:
		if e.errno == errno.ENXIO: return
		raise
	try: os.write(pipe, (json.dumps(usage) + "\n").encode())
	except (BrokenPipeError, BlockingIOError): pass
	finally: os.close(pipe)


if __name__ == "__main__":
	while True:
		start = time.monotonic()
		main()
		# start every 5 seconds
		time.sleep(max(5 - (time.monotonic() - start), 0))
