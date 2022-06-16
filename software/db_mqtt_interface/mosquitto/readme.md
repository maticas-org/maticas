# Moquitto Set up

## Configuration
The `/etc/mosquitto/mosquitto.conf` file contains required parameters to make the broker run properly, such as:
- `listener`: The instance's IP adress.
- `port`: Port to init the service.
- `passfile`: Credential management file.
- `ssl config`: Init certificates files.
## TLS Set up
In order to secure communication between microcontrollers and MQTTBroker it is necessary to create an SSL certificate.
This process has been automated with the script `ssl_create` keep in mind that this script requires sudo privileges.
### Useful files
- Client:
    These files must be burned into microcontrollers with authentication propouses.
        - `ca.crt`
        - `client.crt`
        - `client.key`
- Server:
    These files are required by mosquitto ssl authentication:
        - `ca.crt`
        - `server.crt`
        - `server.key`
## Instructions and ussage
### Boot Up
    To start running the service use the following command:
    `sudo mosquitto -c /etc/mosquitto/mosquitto.conf -d`
### Debug
For debugging propouses the following commands allow the user plublicate and subscribe into the broker:
- PUB:
    `mosquitto_pub --cafile ca.crt -h IP -p PORT -t "topic" -m "test" -u "user" -P "password" --cert client.crt  --key client.key`
- SUB:
    `mosquitto_sub --cafile ca.crt -h IP -t "topic" -p PORT --cert client.crt --key client.key`
