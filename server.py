import socket
import threading

BUFF_SIZE = 1024
# ~ HEADER_LENGTH = 10
host = "127.0.0.1"
port = 55555
			
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

clients = []
nicknames = []

def broadcast(msg):
	for client in clients:
		client.send(msg)
		
def handle(client):
	while True:
		try:
			msg = client.recv(BUFF_SIZE)
			broadcast(msg)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			
			nickname = nicknames[index]
			end_conn_msg = f"{nickname} left the chat!"
			broadcast(end_conn_msg.encode('ascii'))
			
			nicknames.remove(nickname)
			print(f"{nickname} disconnected and has been removed from the client list")
			break
			
def receive():
	while True:
		# accept the connection from a client and assign client id and address
		client, address = server_socket.accept()
		print(f"{str(address)} connected to the server!")
		
		# ask for nickname and register the client into the list
		client.send('NICK'.encode('ascii'))
		nickname = client.recv(BUFF_SIZE).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)
		
		# inform all the other clients that someone has joined
		print(f"Nickname of the client is {nickname}")
		broadcast(f"{nickname} has connected to the server!".encode('ascii'))
		client.send(f"You are connected to the server!".encode('ascii'))
		
		# start a thread for the sending function
		thread = threading.Thread(target=handle, args=(client,))
		thread.start()
		
print("Server is now listening...")
receive()
	
	
	

