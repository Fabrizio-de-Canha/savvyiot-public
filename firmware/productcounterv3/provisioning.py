import machine # type: ignore
import network # type: ignore
import time
import os
import socket

# Include the custom URL decoding function
def url_decode(encoded_str):
    """Decode a URL-encoded string."""
    decoded = ''
    i = 0
    while i < len(encoded_str):
        if encoded_str[i] == '%':
            # Convert the hex value to a character
            hex_value = encoded_str[i + 1:i + 3]
            decoded += chr(int(hex_value, 16))
            i += 3  # Skip the encoded part
        elif encoded_str[i] == '+':
            decoded += ' '  # Decode spaces
            i += 1
        else:
            decoded += encoded_str[i]
            i += 1
    return decoded

PROVISION_TIMEOUT = 5

# Files to save WiFi credentials
WIFI_CONFIG_FILE = 'wifi_config.txt'

# Access Point credentials (for the ESP32 itself)
AP_SSID = 'InjectionIOT_Provision'
AP_PASSWORD = '12345678'

# Ensure proper security mode for the AP
AP_AUTHMODE = network.AUTH_WPA_WPA2_PSK

led_pin = machine.Pin(13, machine.Pin.OUT)
led2_pin = machine.Pin(12, machine.Pin.OUT)
relay_1 = machine.Pin(33, machine.Pin.OUT)
relay_2 = machine.Pin(32, machine.Pin.OUT)

def save_credentials(ssid, password:str):
    """Save WiFi credentials to a file."""
    password = password.replace('\\r\\nAccept-Encoding:', '') 

    print(f"Saving SSID: {ssid}, Password: {password}") 

    try:
        with open('wifi_config.txt', 'w') as f:
            f.write(f"{ssid}\n{password}")
        print("WiFi credentials saved successfully.")

        machine.reset()
    except Exception as e:
        print("Error saving WiFi credentials:", e)

def load_wifi_credentials():
    """Load WiFi credentials from file."""
    if WIFI_CONFIG_FILE in os.listdir():
        with open(WIFI_CONFIG_FILE, 'r') as f:
            ssid = f.readline().strip()
            password = f.readline().strip()
            return ssid, password
    return None, None

def start_access_point():
    """Create an access point for provisioning."""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=AP_AUTHMODE)

    while not ap.active():
        pass

    print(f"Access Point started. SSID: {AP_SSID}, IP: {ap.ifconfig()[0]}")
    return ap.ifconfig()[0]  # Return the AP IP address

def web_page(success=False):
    """A well-formatted HTML page for WiFi provisioning."""
    message = "<p style='color: green; font-size: 28px;'>WiFi credentials saved successfully!</p>" if success else ""
    message2 = "<p style='color: green; font-size: 28px;'>Device will reset now</p>" if success else ""

    html = f"""
    <html>
        <head>
            <title>ESP32 WiFi Provisioning</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 40px;  /* Increased padding for more space */
                    width: 90%;  /* Full width with some margin */
                    max-width: 100vw;  /* Maximum width for larger screens */
                    text-align: center;
                }}
                h1 {{
                    font-size: 50px;  /* Increased font size for the header */
                    margin-bottom: 20px;
                }}
                label {{
                    display: block;
                    margin: 15px 0 5px;
                    font-size: 32px;  /* Increased label font size */
                }}
                input[type="text"], input[type="password"] {{
                    width: 100%;
                    padding: 28px;  /* Increased padding */
                    margin: 5px 0 15px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 28px;  /* Increased input font size */
                }}
                input[type="submit"] {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 30px;  /* Increased padding */
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 32px;  /* Increased button font size */
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>WiFi Provisioning</h1>
                {message}
                {message2}
                <p style="font-size: 28px;">Enter your WiFi credentials below:</p>
                <form action="/save" method="GET">
                    <label for="ssid">SSID:</label>
                    <input type="text" id="ssid" name="ssid" required>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                    <input type="submit" value="Save">
                </form>
            </div>
        </body>
    </html>
    """
    return html

def send_response(client, content):
    """Send the HTTP response and close the connection immediately."""
    try:
        headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n'
        print("Sending response headers...")
        client.sendall(headers.encode())  # Ensure headers are bytes
        print("Sending response body...")
        client.sendall(content.encode())  # Ensure content is bytes
        print("Response fully sent, closing connection.")
    except Exception as e:
        print(f"Error sending response: {e}")
    finally:
        client.close()  # Close the client socket explicitly

def start_web_server():
    """Start the web server to handle requests."""
    addr_info = socket.getaddrinfo('0.0.0.0', 80)

    # Debug: Print address info
    print("Address Info:", addr_info)

    if not addr_info:
        print("No address info found!")
        return

    # Get the address for binding
    addr = addr_info[0][-1]  # Get the last element, which is the address and port tuple
    print("Binding to address:", addr)

    s = socket.socket()

    try:
        s.bind(addr)  # Bind the socket to the address and port
        s.listen(1)  # Start listening for connections
        print('Web server started on', addr)

        while True:
            cl, addr = s.accept()  # Accept a new connection
            print('Client connected from', addr)
            request = cl.recv(1024)  # Receive request data
            request = str(request)
            # print('Received request:', request)

            # Use a flag to track if the save operation was done
            saved = False

            # Handle the request as before...
            if '/save' in request and not saved:
                try:
                    # Extract SSID and password from the request
                    ssid_start = request.find('ssid=') + len('ssid=')
                    ssid_end = request.find('&', ssid_start)
                    if ssid_end == -1:  # If no '&' is found, take the rest of the request
                        ssid_end = request.find(' HTTP/1.1')  # Find end of SSID before the HTTP version
                    ssid = request[ssid_start:ssid_end]

                    password_start = request.find('password=') + len('password=')
                    password_end = request.find(' ', password_start)  # Find space after the password
                    if password_end == -1:  # If no space is found, take the rest of the request
                        password_end = request.find(' HTTP/1.1', password_start)  # Find end of password before the HTTP version
                    password = request[password_start:password_end]

                    ssid = url_decode(ssid)
                    password = url_decode(password)

                    print(password)
                    print(ssid)

                    # Save the WiFi credentials
                    save_credentials(ssid, password)

                    # Show success message
                    response = web_page(success=True)
                    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()

                    saved = True  # Set flag to prevent duplicate processing
                except Exception as e:
                    print("Error parsing request:", e)
                    response = web_page(success=False)
                    cl.send('HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
            else:
                # Show the main page with the form
                response = web_page()
                cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()

    except OSError as e:
        print("Socket error:", e)
    finally:
        s.close()  # Ensure the socket is closed properly


def start_provisioning():
    """Start provisioning mode by setting up an access point and web server."""
    print("Starting provisioning mode...")
    ip_address = start_access_point()
    print(f"Connect to the network {AP_SSID} and go to http://{ip_address} to configure WiFi.")
    start_web_server()