import socket
import threading

BUFF_SIZE = 1024
server_host = "127.0.0.1"
server_port = 55555

nickname = input("Choose a nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host,server_port))

def receive():
	while True:
		try:
			msg = client_socket.recv(BUFF_SIZE).decode('ascii')
			if msg == 'NICK':
				client_socket.send(nickname.encode('ascii'))
			else:
				print(msg)
		except:
			print("An error occured!")
			client_socket.close()
			break
			
def write():
	while True:
		msg = f"{nickname}: {input("")}"
		client_socket.send(msg.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

writing_thread = threading.Thread(target=write)
writing_thread.start()
