#!/usr/bin/env python3
"""
VirtualBox Chat Application - GUI Client Component
Developed for: Faridah Adebajo (n01676123) & Happy Christelle (n01686171)

This GUI-based client provides a user-friendly interface for the chat application.
Uses tkinter for cross-platform compatibility on Windows VMs.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import time
from datetime import datetime

class ChatClientGUI:
    def __init__(self, root):
        """Initialize the GUI chat client"""
        self.root = root
        self.root.title("VirtualBox Chat Client")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        # Chat client properties
        self.client_socket = None
        self.connected = False
        self.username = ""
        
        # Setup GUI
        self.setup_gui()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔥 VirtualBox Chat Client", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding="5")
        conn_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        conn_frame.columnconfigure(1, weight=1)
        
        # Username
        ttk.Label(conn_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.username_entry = ttk.Entry(conn_frame, width=20)
        self.username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Server IP
        ttk.Label(conn_frame, text="Server IP:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.server_ip_entry = ttk.Entry(conn_frame, width=15)
        self.server_ip_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Port
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=4, sticky=tk.W, padx=(10, 5))
        self.port_entry = ttk.Entry(conn_frame, width=8)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=0, column=5, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Connect button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=6, padx=(10, 0))
        
        # Chat area
        chat_frame = ttk.LabelFrame(main_frame, text="Chat Messages", padding="5")
        chat_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Message display area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            state=tk.DISABLED, 
            wrap=tk.WORD,
            height=15,
            font=("Consolas", 10)
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for different message types
        self.chat_display.tag_configure("system", foreground="blue", font=("Consolas", 10, "italic"))
        self.chat_display.tag_configure("own", foreground="green", font=("Consolas", 10, "bold"))
        self.chat_display.tag_configure("other", foreground="black")
        self.chat_display.tag_configure("timestamp", foreground="gray", font=("Consolas", 8))
        
        # Message input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        
        # Message entry
        self.message_entry = ttk.Entry(input_frame, font=("Arial", 11))
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.bind("<KP_Enter>", self.send_message_event)
        
        # Send button
        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.grid(row=0, column=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to connect")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Initially disable chat controls
        self.set_chat_controls_state(False)
    
    def set_chat_controls_state(self, enabled):
        """Enable or disable chat controls"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.message_entry.config(state=state)
        self.send_btn.config(state=state)
        
        if enabled:
            self.message_entry.focus()
    
    def toggle_connection(self):
        """Toggle connection to server"""
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        """Connect to the chat server"""
        # Get connection parameters
        username = self.username_entry.get().strip()
        server_ip = self.server_ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        # Validate inputs
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            self.username_entry.focus()
            return
        
        if not server_ip:
            messagebox.showerror("Error", "Please enter server IP address")
            self.server_ip_entry.focus()
            return
        
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid port number")
            self.port_entry.focus()
            return
        
        # Attempt connection
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(10)  # 10 second timeout
            
            self.status_var.set(f"Connecting to {server_ip}:{port}...")
            self.connect_btn.config(state=tk.DISABLED)
            self.root.update()
            
            self.client_socket.connect((server_ip, port))
            self.connected = True
            self.username = username
            
            # Update GUI
            self.status_var.set(f"Connected to {server_ip}:{port}")
            self.connect_btn.config(text="Disconnect", state=tk.NORMAL)
            self.set_chat_controls_state(True)
            
            # Add connection message to chat
            self.add_message_to_chat("✅ Connected to server", "system")
            
            # Start message handling thread
            self.message_thread = threading.Thread(target=self.handle_server_messages)
            self.message_thread.daemon = True
            self.message_thread.start()
            
            # Send username to server
            self.setup_chat_session()
            
        except socket.timeout:
            messagebox.showerror("Connection Error", "Connection timed out. Please check server address and port.")
            self.reset_connection_state()
        except socket.error as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.reset_connection_state()
    
    def setup_chat_session(self):
        """Setup the chat session after connection"""
        try:
            # Wait for server to request username
            initial_message = self.client_socket.recv(1024).decode('utf-8')
            if initial_message == "ENTER_NAME":
                # Send username to server
                self.client_socket.send(self.username.encode('utf-8'))
                
                # Wait for welcome message
                welcome_message = self.client_socket.recv(1024).decode('utf-8')
                self.add_message_to_chat(welcome_message, "system")
                
        except Exception as e:
            self.add_message_to_chat(f"❌ Error setting up chat: {e}", "system")
    
    def handle_server_messages(self):
        """Handle incoming messages from server (runs in separate thread)"""
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Skip the initial name request as it's handled in setup
                if message == "ENTER_NAME":
                    continue
                
                # Handle server shutdown
                if message.startswith("🛑"):
                    self.root.after(0, self.add_message_to_chat, message, "system")
                    self.root.after(100, self.reset_connection_state)
                    break
                
                # Regular message
                self.root.after(0, self.add_message_to_chat, message, "other")
                
            except socket.error:
                if self.connected:
                    self.root.after(0, self.add_message_to_chat, "❌ Connection lost", "system")
                    self.root.after(100, self.reset_connection_state)
                break
    
    def send_message_event(self, event):
        """Handle Enter key press in message entry"""
        self.send_message()
        return "break"  # Prevent default behavior
    
    def send_message(self):
        """Send a message to the server"""
        if not self.connected:
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        try:
            # Send message to server
            self.client_socket.send(message.encode('utf-8'))
            
            # Add to chat display
            self.add_message_to_chat(f"You: {message}", "own")
            
            # Clear entry
            self.message_entry.delete(0, tk.END)
            
        except socket.error as e:
            self.add_message_to_chat(f"❌ Failed to send message: {e}", "system")
            self.reset_connection_state()
    
    def add_message_to_chat(self, message, message_type="other"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.chat_display.insert(tk.END, timestamp, "timestamp")
        
        # Add message
        self.chat_display.insert(tk.END, message + "\n", message_type)
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def disconnect_from_server(self):
        """Disconnect from the server"""
        if self.connected:
            try:
                self.client_socket.send("quit".encode('utf-8'))
                time.sleep(0.1)
            except:
                pass
        
        self.reset_connection_state()
        self.add_message_to_chat("🔌 Disconnected from server", "system")
    
    def reset_connection_state(self):
        """Reset connection state and GUI"""
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        # Update GUI
        self.status_var.set("Ready to connect")
        self.connect_btn.config(text="Connect", state=tk.NORMAL)
        self.set_chat_controls_state(False)
    
    def on_closing(self):
        """Handle window closing event"""
        if self.connected:
            self.disconnect_from_server()
        
        self.root.destroy()

def main():
    """Main function to start the GUI chat client"""
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        # You can add an icon file here if available
        # root.iconbitmap("chat_icon.ico")
        pass
    except:
        pass
    
    # Create and run the application
    app = ChatClientGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()