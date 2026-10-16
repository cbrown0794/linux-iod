import socket, threading, os

HOST = "10.0.2.2"
PORT = 6767

PIPE = "/home/sutwilterdink/linux-iod/src/server/usage-stats.fifo"
data = b""

def main()->None:
	threading.Thread(target=get_pipe_data).start()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
		# bind socket
		_socket.bind((HOST, PORT))
		# listen for connection
		_socket.listen()
		print(f"Server listening on {HOST}:{PORT}...")
		# accept connection
		while True:
			conn, addr = _socket.accept()
			# handle connection on a thread to allow multiple connections at once
			t = threading.Thread(target=handle_connection, args=(conn, addr))
			t.start()


def get_pipe_data():
	global data
	while True:
		with open(PIPE, "rb") as pipe:
			data = pipe.read()


def handle_connection(conn, addr)->None:
	global data
	with conn:
		print(f"Connection started by {addr}")
		while conn.recv(64):
			conn.sendall(data)


if __name__ == "__main__":
	main()
