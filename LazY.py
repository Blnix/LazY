import paramiko
import sys
import os
import time
import subprocess

hostlist = ['192.168.0.2','192.168.0.1']        #Ip`s without port. SSH server port must be 22. Can be multiple.
username = 'user'                               #Username of the windows account. Must be admin.
password = 'password'                           #The password of the account
auto_reconnect = False        #If set to True, will ping the host until it is back online except when doing a shutdown.

os.system('cls' if os.name == 'nt' else 'clear')
print("LazY is running")
print("Made by Blnix.")
print("")

while True:
    if len(hostlist) > 1:
        print("Multiple host found:")
        for index, item in enumerate(hostlist, start=1):
            print(f"{index}. {item}")
        user_choice = input()
        if user_choice.isdigit() and 1 <= int(user_choice) <= len(hostlist):
            host = hostlist[int(user_choice) - 1]
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please enter a valid number.")
    else:
        host = hostlist[0]
        break

def create_ssh(host=host, username=username, password=password):
    try:
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        print("connected")
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed. Check your username and password.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    if auto_reconnect:
        wait_for_host()
    else:
        sys.exit()

def shutdown_target():
    print("Trying to shutdown target")
    try:
        ssh.exec_command('shutdown /s /t 0')
        print("Target will shutdown soon")
    except Exception as e:
        print("Something went wrong:", str(e))

def reboot_target():
    print("Trying to reboot target")
    try:
        ssh.exec_command('shutdown /r /t 0')
        print("Target will reboot soon")
    except Exception as e:
        print("Something went wrong:", str(e))

def sleep_target():
    print("Trying to turn to sleep mode")
    try:
        ssh.exec_command('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        print("Target will sleep soon")
    except Exception as e:
        print("Something went wrong:", str(e))

def logoff_target():
    global ssh
    try:
        print("Closing connection")
        ssh.close()
        print("Closed")
    except:
        print("Exiting script.")
        ssh = None

def wait_for_host():
    global ssh
    print("Waiting for host to start:")
    time.sleep(5)
    online = False
    check = 0
    while not online:
        progressbar = "[" + "#" * check + " " * (30 - check) + "]"
        print("\r" + progressbar, end="", flush=True)
        time.sleep(0.1)
        check = check + 1
        if check > 30:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Checking host.")
            is_host_up = ping()
            if is_host_up:
                print("Host is back up!")
                ssh = create_ssh()
                online = True
            else:
                print("Host is still down.")
            check = 0

def ping():
    if os.name == 'nt':
        ping_command = f"ping -n 1 {host}"
    else:
        ping_command = f"ping -c 1 {host}"

    try:
        ping_result = str(subprocess.check_output(ping_command, shell=True))
    except:
        ping_result = ""

    return 'ttl' in ping_result.lower()



print(f"Connecting to: {host}")
ssh = create_ssh()

while True:
    print("Commands to execute:")
    print("1. for shutdown")
    print("2. for reboot")
    print("3. for sleep")
    print("4. for exit")
    command = input()

    if command == '1':
        shutdown_target()
        logoff_target()
        sys.exit()
    elif command == '2':
        reboot_target()
    elif command == '3':
        sleep_target()
    elif command == '4':
        logoff_target()
        sys.exit()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{command} is not a valid input.")

    if (command == '2' or command == '3') and not auto_reconnect:
        logoff_target()
        sys.exit()
    elif (command == '2' or command == '3') and auto_reconnect:
        logoff_target()
        wait_for_host()