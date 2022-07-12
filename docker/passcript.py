#!/bin/python
import subprocess
import sys
import os
from dotenv import dotenv_values, load_dotenv, find_dotenv, set_key
# load_dotenv()
# print(os.getenv('test', 'no hay no existe'))
# set_key(find_dotenv(), 'test', 'test-si hay si existe2')
# print(os.getenv('test', 'no hay no existe'))

def clear_passfile():
    with open('/etc/mosquitto/passfile', 'w') as f:
        f.write('')
        print("Passfile cleared")
        print("WARNING: NO default user is set to connect to the broker")
        print("You must add a default user to connect to the broker")
        new_usrname, new_passwd = add_usr()
        env = find_dotenv()
        print(f"Writing new default user to env file: {env}")
        set_key(env, 'MQTT_USERNAME', new_usrname)
        set_key(env, 'MQTT_PASSWORD', new_passwd)
        print(f"New defaults:\nUser: {new_usrname}\nPassword: {new_passwd}")


def add_usr():
    subprocess.run(f"killall mosquitto", shell=True)
    new_usrname = input("Enter a new username: ")
    new_passwd = input("Enter a new password: ")
    subprocess.run(f"mosquitto_passwd -b /etc/mosquitto/passfile {new_usrname} {new_passwd}", shell=True)
    print("User added. Restaring mosquitto")
    subprocess.run(f"mosquitto -c /etc/mosquitto/mosquitto.conf -d", shell=True)
    print("Restarted mosquitto")
    return new_usrname, new_passwd


def main():
    if len(sys.argv) == 1:
        print("Usage: passcript.py [add|clear]")
        sys.exit(1)
    if sys.argv[1] == "add":
        add_usr()
    elif sys.argv[1] == "clear":
        clear_passfile()
    else:
        print("Usage: passcript.py [add|clear]")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
