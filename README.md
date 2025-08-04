# 🔥 VirtualBox Chat Application

**A Python-based chat system for demonstrating network communication between Windows VMs**

## 👥 Project Team
- **Faridah Adebajo** (n01676123) - VM Setup, Network Configuration, Frontend Development
- **Happy Christelle** (n01686171) - Backend Development, Message Handling, Testing & Documentation

---

## 📋 Project Overview

This project demonstrates real-time chat communication between two Windows Virtual Machines running in Oracle VirtualBox. It's designed to help students understand virtual networking, socket programming, and inter-machine communication in a controlled environment.

### 🎯 Key Features
- ✅ **Real-time messaging** between multiple clients
- ✅ **Multi-threaded server** supporting concurrent connections
- ✅ **Both console and GUI clients** for different user preferences
- ✅ **Internal network configuration** for secure VM-to-VM communication
- ✅ **Cross-platform Python** implementation using standard libraries
- ✅ **Graceful connection handling** with proper disconnect procedures

### 🛠️ Technologies Used
- **VirtualBox** - VM management and network configuration
- **Python 3.8+** - Core programming language
- **Socket Programming** - Network communication
- **Threading** - Concurrent client handling
- **Tkinter** - GUI framework for client interface
- **Windows 10/11** - Operating system for VMs

---

## 🚀 Quick Start Guide

### Prerequisites
- Oracle VirtualBox (6.1+)
- 2 Windows VMs with Python 3.8+ installed
- Internal network configured between VMs

### 📁 File Structure
```
VirtualBox-Chat-Application/
├── chat_server.py          # Multi-threaded chat server
├── chat_client.py          # Console-based client
├── chat_client_gui.py      # GUI-based client
├── SETUP_GUIDE.md          # Detailed setup instructions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### ⚡ Quick Start (3 Steps)

1. **Start the Server** (on Server VM):
   ```cmd
   python chat_server.py
   ```

2. **Connect with Console Client** (on Client VM):
   ```cmd
   python chat_client.py
   ```

3. **Or use GUI Client** (on Client VM):
   ```cmd
   python chat_client_gui.py
   ```

---

## 🔧 Detailed Setup

### 1️⃣ VirtualBox Configuration
- Create 2 Windows VMs (4GB RAM, 50GB storage each)
- Configure internal network: `ChatNetwork`
- Assign static IPs:
  - Server VM: `192.168.100.10`
  - Client VM: `192.168.100.20`

### 2️⃣ Network Testing
```cmd
# Test connectivity between VMs
ping 192.168.100.10  # From client to server
ping 192.168.100.20  # From server to client
```

### 3️⃣ Application Setup
1. Install Python 3.8+ on both VMs
2. Copy chat application files to both VMs
3. No additional pip installations required!

📖 **For detailed instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

---

## 💬 Application Components

### 🖥️ Chat Server (`chat_server.py`)
- **Multi-threaded architecture** for handling multiple clients
- **Broadcast messaging** to all connected users
- **Connection management** with join/leave notifications
- **Graceful shutdown** with Ctrl+C handling
- **Real-time logging** of all chat activity

**Features:**
- Supports unlimited concurrent clients
- Automatic client name assignment
- Message timestamping
- Server status monitoring

### 💻 Console Client (`chat_client.py`)
- **Simple command-line interface** for basic chat functionality
- **Real-time message display** with server notifications
- **Threaded message handling** for smooth user experience
- **Connection error handling** with helpful diagnostics

**Usage:**
```cmd
python chat_client.py
# Enter username, server IP, and port
# Start chatting immediately!
```

### 🎨 GUI Client (`chat_client_gui.py`)
- **Modern tkinter interface** with professional appearance
- **Scrollable message history** with color-coded messages
- **Connection status indicator** and error dialogs
- **Keyboard shortcuts** (Enter to send messages)

**Features:**
- User-friendly connection form
- Real-time message timestamps
- Automatic scrolling to latest messages
- Graceful window closing

---

## 🔗 Network Architecture

```
┌─────────────────┐    Internal Network     ┌─────────────────┐
│   Server VM     │    (ChatNetwork)        │   Client VM     │
│  192.168.100.10 │◄──────────────────────►│  192.168.100.20 │
│                 │                         │                 │
│ chat_server.py  │        Port 12345       │ chat_client.py  │
│     Running     │                         │     Running     │
└─────────────────┘                         └─────────────────┘
```

### 📡 Communication Flow
1. **Server starts** and listens on port 12345
2. **Client connects** to server IP address
3. **Handshake** establishes username and welcome message
4. **Real-time messaging** between all connected clients
5. **Graceful disconnect** when clients leave

---

## 📊 Project Learning Outcomes

### 🎓 Educational Benefits
- **Virtual Networking:** Configure internal networks in VirtualBox
- **Socket Programming:** Understand client-server communication
- **Multi-threading:** Handle concurrent connections efficiently
- **GUI Development:** Create user-friendly interfaces with tkinter
- **Network Troubleshooting:** Diagnose and resolve connectivity issues

### 🔍 Technical Skills Developed
- VirtualBox VM management and networking
- Python socket programming and threading
- Network protocol understanding (TCP/IP)
- Cross-platform application development
- System administration and troubleshooting

---

## 🐛 Troubleshooting

### ❌ Common Issues

**"Connection refused"**
- ✅ Check server is running first
- ✅ Verify IP address (192.168.100.10)
- ✅ Confirm port 12345 is available

**"Cannot ping between VMs"**
- ✅ Verify internal network configuration
- ✅ Check static IP assignments
- ✅ Restart network adapters

**"Python not recognized"**
- ✅ Install Python with "Add to PATH" option
- ✅ Use full path: `C:\Python\python.exe`

### 🔧 Advanced Debugging
```cmd
# Check network configuration
ipconfig /all

# Verify port availability
netstat -an | findstr 12345

# Test Python installation
python --version
```

---

## 🔒 Security Considerations

⚠️ **Important Security Notes:**
- This application is for **educational purposes only**
- **No encryption** - messages sent in plain text
- **No authentication** - anyone can connect
- **Use only on trusted internal networks**
- **Not suitable for production environments**

---

## 📈 Future Enhancements

### 🚀 Potential Improvements
- **Encryption:** Add SSL/TLS for secure communication
- **Authentication:** User login system with passwords
- **File Sharing:** Send files between clients
- **Chat History:** Persistent message storage
- **Emojis & Formatting:** Rich text support
- **Voice Chat:** Audio communication features

### 🎯 Advanced Features
- **Multiple Chat Rooms:** Separate conversation channels
- **Private Messaging:** Direct messages between users
- **Admin Controls:** Server management interface
- **Mobile Support:** Cross-platform mobile clients

---

## 📚 Resources & References

### 📖 Documentation
- [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [VirtualBox User Manual](https://www.virtualbox.org/manual/)
- [Tkinter GUI Programming](https://docs.python.org/3/library/tkinter.html)

### 🎥 Learning Materials
- VirtualBox networking tutorials
- Python socket programming guides
- Network configuration best practices

---

## 📝 Project Requirements Met

### ✅ Technical Requirements
- [x] **Two Windows VMs** configured in VirtualBox
- [x] **Internal network** connecting both machines
- [x] **Socket-based chat application** with real-time messaging
- [x] **Multi-client support** with concurrent connections
- [x] **Both console and GUI interfaces** for user interaction
- [x] **Proper error handling** and connection management

### ✅ Educational Objectives
- [x] **Hands-on virtual networking** experience
- [x] **Socket programming** understanding
- [x] **System communication** demonstration
- [x] **Network troubleshooting** skills development

---

## 📧 Contact & Support

**Project Team:**
- **Faridah Adebajo:** [n01676123@humber.ca](mailto:n01676123@humber.ca)
- **Happy Christelle:** [n01686171@humber.ca](mailto:n01686171@humber.ca)

**Course:** Virtualization and Cloud Computing  
**Institution:** [Your Institution Name]  
**Semester:** [Current Semester]

---

## 📜 License

This project is created for educational purposes as part of a college assignment. Feel free to use and modify for learning purposes.

---

⭐ **If this project helped you understand virtual networking and socket programming, please star this repository!**

**Happy Chatting! 💬🚀**