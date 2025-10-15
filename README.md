Remote Administration Tool
Overview
This project consists of a client-server remote administration system with multiple capabilities for remote management and monitoring. The system includes a Command and Control (C2) server and a client agent.

⚠️ IMPORTANT LEGAL NOTICE: This software is provided for educational and authorized testing purposes only. Unauthorized use on systems you do not own or have explicit permission to access is illegal and unethical.

Project Structure
text
├── client.py                 # Client application (runs on target systems)
├── C2.py                     # Command and Control server (control center)
└── README.md                 # This file
Client Application (client.py)
The client application runs on target systems and provides remote access capabilities to the C2 server.

Features
1. Persistence Mechanisms
System Copy: Automatically copies itself to multiple system locations

Startup Registration: Adds itself to Windows Registry for automatic startup

Firewall Bypass: Includes placeholder for firewall modification

2. Remote Access Capabilities
Command Execution: Execute system commands remotely

File System Navigation: Change directories and list contents

Process Management: Start and manage system processes

3. File Transfer Operations
Upload: Receive files from C2 server to client

Download: Send files from client to C2 server

4. Surveillance Features
Camera Recording: Capture video from webcam

Screen Recording: Record desktop activity

Screenshot Capture: Take multiple screenshots with configurable delays

5. Social Engineering Modules
Phishing Attacks: Launch fake login pages for various services

Fake Dialogs: Display custom dialog boxes to trick users

Installation and Persistence
The client automatically implements persistence through:

Copying to AppData\Local directory across multiple drives

Adding registry entry in HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run

Multiple drive location redundancy for increased persistence

Connection Configuration
python
# Configure these settings in client.py
SERVER_HOST = '192.168.77.132'  # C2 Server IP address
SERVER_PORT = 9999              # C2 Server port
Command and Control Server (C2.py)
The C2 server provides the control interface for managing connected clients and executing remote operations.

Features
1. Connection Management
Multi-client Support: Handle multiple simultaneous client connections

Session Management: Select and manage individual client sessions

Connection Listing: View all active client connections with IP details

2. Remote Operations
Command Execution: Send and execute commands on remote systems

Real-time Output: Receive command outputs in real-time

Directory Management: Navigate and explore remote file systems

3. File Transfer Operations
File Upload: Transfer files from server to client

File Download: Retrieve files from client to server

Chunked Transfers: Handle large files through efficient chunked transfer

4. Surveillance Control
Camera Control: Initiate and manage webcam recording sessions

Screen Recording: Start/stop desktop recording with frame control

Screenshot Management: Configure and capture screenshots with timing options

5. Social Engineering Toolkit
Phishing Templates: 15 pre-configured phishing pages for popular services

Custom Dialogs: Create fake system dialogs and warning messages

User Interaction: Capture user responses and inputs through social engineering

Server Setup and Operation
bash
python C2.py
The server will:

Bind to 0.0.0.0:9999 (configurable)

Listen for incoming client connections

Provide interactive command interface for client management

Usage Guide
Starting the C2 Server
Configure server settings if needed in C2.py:

python
SERVER_HOST = '0.0.0.0'  # Bind address
SERVER_PORT = 9999       # Listen port
Run the server:

bash
python C2.py
Server starts listening for client connections

Client Deployment
Deploy client.py to target system

Configure C2 server connection details in client code:

python
SERVER_HOST = 'YOUR_SERVER_IP'  # C2 Server IP
SERVER_PORT = 9999              # C2 Server port
Client automatically connects and registers with C2 server

Basic Operations
Listing Active Connections
text
Session> list
Selecting a Client Session
text
Session> select 0
Remote Command Execution
Select client session

Choose option 1 - Remote Access

Enter system commands as needed

View real-time command outputs

File Transfer Operations
Select client session

Choose option 2 - File Transfer

Select upload (to client) or download (from client)

Specify source and destination file paths

Social Engineering Toolkit
Available Phishing Templates
Social Media: Facebook, Instagram, Twitter, Snapchat

Email Services: Google, Yahoo, ProtonMail

Professional: LinkedIn, Microsoft, GitHub

Entertainment: Netflix, Spotify

Other Services: Pinterest, WordPress

Fake Dialog Options
Yes/No Dialogs: Force user decision making

Input Dialogs: Capture user credentials or information

Custom Messages: Tailored social engineering scenarios

Technical Specifications
Network Protocol
TCP socket communication

Custom command protocol with error handling

Chunked file transfer for large files

Comprehensive timeout and recovery mechanisms

Security Features
Connection persistence with automatic retry logic

Robust error handling and recovery procedures

Timeout management for large file transfers

Multiple fallback mechanisms

Dependencies
Client Dependencies (client.py)
python
import socket
import subprocess
import os
import threading
import time
import webbrowser
from tkinter import *
import tkinter.messagebox
from PIL import ImageGrab
import numpy as np
import winreg
import getpass
import cv2  # OpenCV for camera features
C2 Server Dependencies (C2.py)
python
import socket
import threading
from queue import Queue
import time
import os
Configuration Guide
Client Configuration
Modify these constants in client.py:

python
SERVER_HOST = '192.168.77.132'  # C2 Server IP address
SERVER_PORT = 9999              # C2 Server port
C2 Server Configuration
Modify these constants in C2.py:

python
SERVER_HOST = '0.0.0.0'         # Bind address (0.0.0.0 for all interfaces)
SERVER_PORT = 9999              # Listen port
Ethical and Legal Considerations
Legal Compliance Requirements
Authorization: Only use on systems you own or have explicit written permission to test

Compliance: Adhere to all local, state, and federal laws and regulations

Documentation: Maintain proper authorization documentation for all testing activities

Responsible Usage Guidelines
Authorized Testing Only: Use exclusively in authorized penetration testing scenarios

Educational Context: Suitable for cybersecurity education and research

Professional Ethics: Follow established ethical guidelines and professional standards

Responsible Disclosure
If vulnerabilities are discovered during usage:

No Unauthorized Exploitation: Do not exploit vulnerabilities without explicit permission

Proper Reporting: Report findings to appropriate authorities or vendors

Ethical Practices: Follow responsible disclosure protocols and timelines

Troubleshooting Guide
Common Issues and Solutions
Connection Issues
Problem: Client cannot connect to C2 server

Solution: Verify server IP configuration, check firewall settings, ensure port availability

Feature Malfunctions
Problem: Specific features (camera, recording) not working

Solution: Verify all dependencies are installed, check client system capabilities

File Transfer Problems
Problem: File transfers failing or incomplete

Solution: Verify file paths and permissions, check available disk space, monitor network stability

Persistence Issues
Problem: Client not maintaining persistence

Solution: Check registry permissions, verify file copy locations, review system security software

Debugging Steps
Check Server Logs: Monitor C2 server for connection attempts and errors

Verify Network Connectivity: Ensure proper network configuration between client and server

Review Client Outputs: Check client-side outputs for specific error messages

Validate Dependencies: Confirm all required Python packages are installed and compatible

Disclaimer
This software is provided strictly for educational purposes and authorized security testing. The authors and contributors are not responsible for any misuse, damage, or legal violations caused by this program. Users are solely responsible for ensuring they have proper authorization before deploying or using this software in any environment.

Always obtain explicit written permission before testing on any system, and comply with all applicable laws and regulations in your jurisdiction.
