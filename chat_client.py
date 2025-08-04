#!/usr/bin/env python3
"""
VirtualBox Chat Application - Console Client Component
Developed for: Faridah Adebajo (n01676123) & Happy Christelle (n01686171)

This console-based client connects to the chat server and allows users
to send and receive messages. Designed to run on the Windows VMs.
"""

import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self):
        """Initialize the chat client"""
        self.client_socket = None
        self.connected = False
        self.username = ""
        
    def connect_to_server(self, host, port):
        """
        Connect to the chat server
        
        Args:
            host (str): Server IP address
            port (int): Server port number
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.connected = True
            print(f"✅ Connected to server at {host}:{port}")
            return True
            
        except socket.error as e:
            print(f"❌ Failed to connect to server: {e}")
            return False
    
    def handle_server_messages(self):
        """Handle incoming messages from the server (runs in separate thread)"""
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Handle special server messages
                if message == "ENTER_NAME":
                    # Server is requesting username
                    continue
                elif message.startswith("🛑"):
                    # Server shutdown message
                    print(f"\n{message}")
                    self.connected = False
                    break
                else:
                    # Regular message - display it
                    print(f"\r{message}")
                    # Reprint the input prompt
                    print("You: ", end="", flush=True)
                    
            except socket.error:
                if self.connected:
                    print("\n❌ Connection to server lost")
                    self.connected = False
                break
    
    def send_message(self, message):
        """
        Send a message to the server
        
        Args:
            message (str): Message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            self.client_socket.send(message.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def start_chat(self):
        """Start the chat session"""
        if not self.connected:
            print("❌ Not connected to server")
            return
        
        try:
            # Wait for server to request username
            initial_message = self.client_socket.recv(1024).decode('utf-8')
            if initial_message == "ENTER_NAME":
                # Send username to server
                self.send_message(self.username)
                
                # Wait for welcome message
                welcome_message = self.client_socket.recv(1024).decode('utf-8')
                print(f"\n{welcome_message}")
            
            # Start thread to handle incoming messages
            message_thread = threading.Thread(target=self.handle_server_messages)
            message_thread.daemon = True
            message_thread.start()
            
            print("\n💬 Chat started! Type your messages below.")
            print("📝 Type 'quit' to leave the chat.")
            print("-" * 50)
            
            # Main chat loop
            while self.connected:
                try:
                    user_input = input("You: ")
                    
                    if user_input.lower() == 'quit':
                        break
                    
                    if user_input.strip():  # Only send non-empty messages
                        if not self.send_message(user_input):
                            break
                            
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except EOFError:
                    print("\n👋 Goodbye!")
                    break
                    
        except Exception as e:
            print(f"❌ Chat error: {e}")
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Disconnect from the server"""
        if self.connected:
            try:
                self.send_message("quit")
                time.sleep(0.1)  # Give server time to process
            except:
                pass
            
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            
        print("🔌 Disconnected from server")

def get_user_input():
    """Get user input for connection parameters"""
    try:
        # Get username
        username = input("Enter your username: ").strip()
        if not username:
            username = f"User_{int(time.time()) % 10000}"
            print(f"Using default username: {username}")
        
        # Get server details
        server_ip = input("Enter server IP address: ").strip()
        if not server_ip:
            print("❌ Server IP is required")
            return None, None, None
        
        port_input = input("Enter server port (default 12345): ").strip()
        if port_input:
            try:
                port = int(port_input)
            except ValueError:
                print("❌ Invalid port number. Using default 12345")
                port = 12345
        else:
            port = 12345
        
        return username, server_ip, port
        
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
        return None, None, None

def main():
    """Main function to start the chat client"""
    print("=" * 60)
    print("💬 VirtualBox Chat Client")
    print("📚 Project by: Faridah Adebajo & Happy Christelle")
    print("=" * 60)
    
    # Get connection parameters
    username, server_ip, port = get_user_input()
    if not all([username, server_ip, port]):
        return
    
    # Create and connect client
    client = ChatClient()
    client.username = username
    
    print(f"\n🔄 Connecting to {server_ip}:{port}...")
    
    if client.connect_to_server(server_ip, port):
        try:
            client.start_chat()
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted")
        finally:
            client.disconnect()
    else:
        print("❌ Failed to connect to server. Please check:")
        print("   • Server is running")
        print("   • IP address is correct")
        print("   • Port number is correct")
        print("   • Network connectivity between VMs")

if __name__ == "__main__":
    main()