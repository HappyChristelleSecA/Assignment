# VirtualBox Chat Application Setup Guide

**Project by:** Faridah Adebajo (n01676123) & Happy Christelle (n01686171)

This guide will help you set up two Windows VMs in VirtualBox and configure them to run a chat application over an internal network.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [VirtualBox VM Setup](#virtualbox-vm-setup)
3. [Network Configuration](#network-configuration)
4. [Python Installation](#python-installation)
5. [Chat Application Setup](#chat-application-setup)
6. [Testing the Connection](#testing-the-connection)
7. [Running the Chat Application](#running-the-chat-application)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- **Oracle VirtualBox** (Version 6.1 or later)
- **Windows 10/11 ISO** file for VM installation
- At least **8GB RAM** on host machine
- At least **50GB** free disk space

### Required Files
- `chat_server.py` - Server application
- `chat_client.py` - Console client application  
- `chat_client_gui.py` - GUI client application

## VirtualBox VM Setup

### Step 1: Create First Windows VM (Server VM)

1. **Open VirtualBox** and click "New"
2. **Configure VM Settings:**
   - Name: `Windows_Server_VM`
   - Type: `Microsoft Windows`
   - Version: `Windows 10/11 (64-bit)`
   - Memory: `4096 MB` (4GB)
   - Hard disk: `Create a virtual hard disk now`
   - Hard disk file type: `VDI`
   - Storage: `Dynamically allocated`
   - Size: `50 GB`

3. **Install Windows:**
   - Start the VM
   - Select your Windows ISO file
   - Complete Windows installation
   - Install VirtualBox Guest Additions

### Step 2: Create Second Windows VM (Client VM)

1. **Repeat the process** for the second VM:
   - Name: `Windows_Client_VM`
   - Same specifications as the server VM
   - Install Windows and Guest Additions

### Step 3: Configure VM Settings

For **both VMs**, configure these settings:
1. **Right-click VM** → Settings
2. **System** → Processor: Allocate 2 CPUs if available
3. **Display** → Video Memory: 128 MB
4. **Network** → (See Network Configuration section)

## Network Configuration

### Step 1: Create Internal Network

1. **In VirtualBox Manager**, go to File → Tools → Network Manager
2. **Click "Create"** to create a new internal network
3. **Name it:** `ChatNetwork`
4. **Enable DHCP** (optional, we'll use static IPs)

### Step 2: Configure VM Network Adapters

**For Server VM (Windows_Server_VM):**
1. VM Settings → Network → Adapter 1
2. **Attached to:** `Internal Network`
3. **Name:** `ChatNetwork`
4. **Advanced → Adapter Type:** Intel PRO/1000 MT Desktop
5. Click OK

**For Client VM (Windows_Client_VM):**
1. Same network configuration as Server VM
2. Both VMs should be on the same `ChatNetwork`

### Step 3: Configure IP Addresses

**Server VM Static IP Configuration:**
1. Boot the Server VM
2. Open **Control Panel** → Network and Internet → Network Connections
3. Right-click **Ethernet** adapter → Properties
4. Select **Internet Protocol Version 4 (TCP/IPv4)** → Properties
5. Select **"Use the following IP address":**
   - IP address: `192.168.100.10`
   - Subnet mask: `255.255.255.0`
   - Default gateway: (leave blank)
   - DNS: (leave blank)
6. Click OK

**Client VM Static IP Configuration:**
1. Boot the Client VM
2. Follow same steps as Server VM
3. Use different IP address:
   - IP address: `192.168.100.20`
   - Subnet mask: `255.255.255.0`
   - Default gateway: (leave blank)
   - DNS: (leave blank)

## Python Installation

### Install Python on Both VMs

1. **Download Python** from https://python.org
   - Get Python 3.8 or later
   - Choose "Windows x86-64 executable installer"

2. **Run the installer:**
   - ✅ Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify installation:**
   ```cmd
   python --version
   pip --version
   ```

### Install Required Libraries

The chat applications use only built-in Python libraries:
- `socket` - for network communication
- `threading` - for handling multiple connections
- `tkinter` - for GUI (included with Python)

No additional pip installations required!

## Chat Application Setup

### Step 1: Transfer Files to VMs

**Option A: Using Shared Folders**
1. VM Settings → Shared Folders
2. Add folder containing Python files
3. Access from `\\vboxsvr\sharename` in Windows

**Option B: Copy and Paste**
1. Enable clipboard sharing in VM settings
2. Copy file contents from host
3. Paste into Notepad and save as `.py` files

**Option C: Download from GitHub/Cloud**
1. Use browser in VM to download files
2. Save to Desktop or Documents folder

### Step 2: Create Project Directory

On **both VMs**, create a folder:
```
C:\ChatApp\
├── chat_server.py
├── chat_client.py
└── chat_client_gui.py
```

## Testing the Connection

### Step 1: Test Network Connectivity

**From Server VM:**
```cmd
ping 192.168.100.20
```

**From Client VM:**
```cmd
ping 192.168.100.10
```

Both pings should be successful with 0% packet loss.

### Step 2: Test Port Communication

**On Server VM**, test if ports are accessible:
```cmd
netstat -an | findstr 12345
```

## Running the Chat Application

### Step 1: Start the Server (Server VM)

1. **Open Command Prompt** as Administrator
2. **Navigate to chat folder:**
   ```cmd
   cd C:\ChatApp
   ```
3. **Run the server:**
   ```cmd
   python chat_server.py
   ```
4. **Server configuration:**
   - Server IP: Press Enter (uses default 0.0.0.0)
   - Port: Press Enter (uses default 12345)
5. **Server should display:**
   ```
   🚀 Chat Server started on 0.0.0.0:12345
   📡 Waiting for connections...
   ```

### Step 2: Start the Client (Client VM)

**Option A: Console Client**
```cmd
cd C:\ChatApp
python chat_client.py
```

**Option B: GUI Client**
```cmd
cd C:\ChatApp
python chat_client_gui.py
```

### Step 3: Connect and Chat

**For Console Client:**
1. Enter username: `YourName`
2. Enter server IP: `192.168.100.10`
3. Enter port: `12345` (or press Enter)
4. Start chatting!

**For GUI Client:**
1. Fill in connection form:
   - Username: `YourName`
   - Server IP: `192.168.100.10`
   - Port: `12345`
2. Click "Connect"
3. Use the GUI to send messages

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to server
**Solutions:**
1. Verify both VMs are on same internal network
2. Check IP addresses are correctly configured
3. Ensure server is running before starting client
4. Disable Windows Firewall temporarily for testing

**Problem:** "Connection refused" error
**Solutions:**
1. Verify server IP address (192.168.100.10)
2. Check port number (12345)
3. Restart server application
4. Check if antivirus is blocking the connection

### Network Issues

**Problem:** Cannot ping between VMs
**Solutions:**
1. Verify internal network configuration
2. Check IP addresses are in same subnet
3. Restart network adapters
4. Reboot both VMs

### Python Issues

**Problem:** "Python is not recognized"
**Solutions:**
1. Reinstall Python with "Add to PATH" checked
2. Add Python to PATH manually
3. Use full path: `C:\Python\python.exe`

**Problem:** Import errors
**Solutions:**
1. Verify Python version (3.8+)
2. All required libraries are built-in
3. Check file syntax and indentation

### Application Issues

**Problem:** Server not accepting connections
**Solutions:**
1. Check server is listening on correct port
2. Verify server didn't crash (check console output)
3. Restart server application
4. Try different port number

**Problem:** Messages not appearing
**Solutions:**
1. Check network connection is stable
2. Verify both client and server are running
3. Look for error messages in console
4. Restart both applications

## Advanced Configuration

### Multiple Clients
- The server supports multiple simultaneous clients
- Start additional client instances on same or different VMs
- Each client needs a unique username

### Custom Port Configuration
- Change port in both server and client applications
- Ensure port is not blocked by firewall
- Common alternative ports: 8080, 9999, 5555

### GUI Customization
- Modify `chat_client_gui.py` for custom appearance
- Change window size, colors, or fonts
- Add additional features like file sharing

## Security Notes

⚠️ **Important:** This application is for educational purposes only
- No encryption or authentication
- Passwords are not required
- Messages are sent in plain text
- Only use on trusted internal networks

## Project Deliverables Checklist

✅ **VM Setup**
- [ ] Two Windows VMs created
- [ ] VirtualBox Guest Additions installed
- [ ] Internal network configured

✅ **Network Configuration**
- [ ] Static IP addresses assigned
- [ ] Ping test successful between VMs
- [ ] Port communication verified

✅ **Application Setup**
- [ ] Python installed on both VMs
- [ ] Chat application files transferred
- [ ] Server successfully starts
- [ ] Client successfully connects

✅ **Testing**
- [ ] Two-way messaging works
- [ ] Multiple clients can connect
- [ ] GUI client functions properly
- [ ] Graceful disconnect works

## Documentation

Remember to document:
1. **Screenshots** of VMs running chat application
2. **Network configuration** details
3. **IP address assignments**
4. **Test results** and connectivity verification
5. **Any challenges** encountered and solutions

---

**Project Team:**
- **Faridah Adebajo (n01676123):** VM setup, network configuration, frontend development
- **Happy Christelle (n01686171):** Backend development, message handling, testing & documentation

**Course:** Virtualalization and Cloud Computing  
**Institution:** Your University/College Name  
**Date:** [Current Date]