# Server side
import sys
import socket
import select
from thread import *

def clientthread(conn, addr): 
    # sends a message to the client whose user object is conn 
    conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    print("<" + addr[0] + "> " + message) 
 
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
  
                else:
                    remove(conn) 
  
            except: 
                continue

def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients)

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	  
	if len(sys.argv) != 3: 
	    print("Correct usage: script, IP address, port number")
	    exit() 
	  
	IP_address = str(sys.argv[1])
	Port = int(sys.argv[2]) 
	  
	server.bind((IP_address, Port)) 
	server.listen(100) 
	  
	list_of_clients = [] 
	    
	while True: 
	  
	    """Accepts a connection request and stores two parameters,  
	    conn which is a socket object for that user, and addr  
	    which contains the IP address of the client that just  
	    connected"""
	    conn, addr = server.accept() 
	  
	    list_of_clients.append(conn) 
	  
	    # prints the address of the user that just connected 
	    print(addr[0] + " connected")
	  
	    # creates and individual thread for every user  
	    # that connects 
	    start_new_thread(clientthread,(conn,addr))     
	  
	conn.close() 
	server.close()

if __name__ == "__main__":
	main()
