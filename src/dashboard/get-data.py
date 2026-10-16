# get-data.py
# Starts a connection to each server and requests data
import socket, json


DESTS = [
	"10.0.1.2",
	"10.0.2.2",
	"10.0.3.2",
	"10.0.4.2",
]
DEST_PORT = 6767


def main():
	for addr in DESTS:
		try: print(connect_to(addr, DEST_PORT))
		except RuntimeError as e: print(e)


def connect_to(addr, port)->dict:
	try:
		with socket.create_connection((addr, port), timeout=10) as conn:
			print(f"Connection started to {addr}:{port}")
			conn.sendall(("r").encode())
			data = ""
			while not data.endswith("\n"):
				buf = conn.recv(1024)
				if not buf:
					break
				data += buf.decode()
			return json.loads(data)
	except (OSError, json.JSONDecodeError) as e:
		raise RuntimeError(f"Connection to {addr} failed: {e}")

if __name__ == "__main__":
	main()
