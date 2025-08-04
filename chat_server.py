#!/usr/bin/env python3
"""
VirtualBox Chat Application - Server Component
Developed for: Faridah Adebajo (n01676123) & Happy Christelle (n01686171)

This server handles connections from multiple chat clients and broadcasts
messages between them. Designed to run on one of the Windows VMs.
"""

import socket
import threading
import datetime
import signal
import sys

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        """
        Initialize the chat server
        
        Args:
            host (str): Server IP address (0.0.0.0 binds to all interfaces)
            port (int): Port number for the server
        """
        self.host = host
        self.port = port
        self.clients = []
        self.client_names = {}
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """Start the chat server and listen for connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🚀 Chat Server started on {self.host}:{self.port}")
            print("📡 Waiting for connections...")
            print("Press Ctrl+C to stop the server\n")
            
            # Set up signal handler for graceful shutdown
            signal.signal(signal.SIGINT, self.signal_handler)
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"🔗 New connection from {client_address}")
                    
                    # Start a new thread to handle the client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"❌ Error accepting connection: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
        finally:
            self.shutdown_server()
    
    def handle_client(self, client_socket, client_address):
        """
        Handle individual client connections
        
        Args:
            client_socket: Socket object for the client
            client_address: Address tuple of the client
        """
        try:
            # Request client name
            client_socket.send("ENTER_NAME".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            
            if not client_name:
                client_name = f"User_{client_address[0]}"
            
            # Add client to the list
            self.clients.append(client_socket)
            self.client_names[client_socket] = client_name
            
            # Notify all clients about the new user
            join_message = f"📥 {client_name} joined the chat"
            print(f"{self.get_timestamp()} {join_message}")
            self.broadcast_message(join_message, sender_socket=None)
            
            # Send welcome message to the new client
            welcome_msg = f"🎉 Welcome to the chat, {client_name}! Type 'quit' to leave."
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Handle messages from this client
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    if message.lower() == 'quit':
                        break
                    
                    # Format and broadcast the message
                    formatted_message = f"{client_name}: {message}"
                    print(f"{self.get_timestamp()} {formatted_message}")
                    self.broadcast_message(formatted_message, sender_socket=client_socket)
                    
                except socket.error:
                    break
                    
        except Exception as e:
            print(f"❌ Error handling client {client_address}: {e}")
        finally:
            self.disconnect_client(client_socket)
    
    def broadcast_message(self, message, sender_socket=None):
        """
        Broadcast a message to all connected clients
        
        Args:
            message (str): Message to broadcast
            sender_socket: Socket of the sender (None if server message)
        """
        disconnected_clients = []
        
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except socket.error:
                    disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.disconnect_client(client)
    
    def disconnect_client(self, client_socket):
        """
        Disconnect a client and clean up
        
        Args:
            client_socket: Socket of the client to disconnect
        """
        if client_socket in self.clients:
            client_name = self.client_names.get(client_socket, "Unknown")
            
            # Remove from lists
            self.clients.remove(client_socket)
            if client_socket in self.client_names:
                del self.client_names[client_socket]
            
            # Close the socket
            try:
                client_socket.close()
            except:
                pass
            
            # Notify remaining clients
            leave_message = f"📤 {client_name} left the chat"
            print(f"{self.get_timestamp()} {leave_message}")
            self.broadcast_message(leave_message, sender_socket=None)
    
    def get_timestamp(self):
        """Get current timestamp for logging"""
        return datetime.datetime.now().strftime("[%H:%M:%S]")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal for graceful shutdown"""
        print(f"\n{self.get_timestamp()} 🛑 Server shutdown initiated...")
        self.running = False
        self.shutdown_server()
    
    def shutdown_server(self):
        """Shutdown the server and disconnect all clients"""
        print(f"{self.get_timestamp()} 🔌 Disconnecting all clients...")
        
        # Notify all clients about server shutdown
        shutdown_message = "🛑 Server is shutting down. Goodbye!"
        for client in self.clients[:]:  # Create a copy to avoid modification during iteration
            try:
                client.send(shutdown_message.encode('utf-8'))
                client.close()
            except:
                pass
        
        self.clients.clear()
        self.client_names.clear()
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print(f"{self.get_timestamp()} ✅ Server stopped")
        sys.exit(0)

def main():
    """Main function to start the chat server"""
    print("=" * 60)
    print("🔥 VirtualBox Chat Server")
    print("📚 Project by: Faridah Adebajo & Happy Christelle")
    print("=" * 60)
    
    # Get server configuration
    try:
        host = input("Enter server IP (press Enter for default 0.0.0.0): ").strip()
        if not host:
            host = '0.0.0.0'
        
        port_input = input("Enter port number (press Enter for default 12345): ").strip()
        if port_input:
            port = int(port_input)
        else:
            port = 12345
            
    except ValueError:
        print("❌ Invalid port number. Using default 12345")
        port = 12345
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
        return
    
    # Start the server
    server = ChatServer(host, port)
    server.start_server()

if __name__ == "__main__":
    main()