import random
import re
import ssl
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from common import HOST, PORT, BUFF_SIZE, modinv


def receive():
    global i, g, p, public_keys, is_veto, last_answer, send_key
    while True:
        try:
            msg = client_socket.recv(BUFF_SIZE).decode("utf8")
            if 'Your ID is' in msg:
                tmp = msg[::]
                i = int(re.sub(r'\D', '', tmp))
            elif 'Proposed g, p' in msg:
                g, p = [int(x) for x in re.findall(r'\d+', msg)]
            elif 'Everyone has send pub_key' in msg:
                public_keys = eval(msg.split('\n')[1])
            elif 'Push enter to sent the public key' in msg:
                send_key = True
            elif 'QUESTION' in msg:
                last_answer = True
            print(msg)
        except OSError:
            break


def send():
    global i, g, p, x_i, last_answer, is_veto, send_key
    while True:

        if not send_key:
            msg = input()

        if last_answer and not send_key:
            is_veto = True if msg == 't' else False
            msg = str(gen_answer(is_veto))
            try:
                client_socket.send(bytes(msg, "utf8"))
            except (ConnectionResetError, ssl.SSLEOFError):
                pass
        elif send_key:
            x_i = random.randint(0, 100)
            msg = str(g ** x_i % p)
            print('I am sending public key: {}'.format(msg))
            send_key = False
            try:
                client_socket.send(bytes(msg, "utf8"))
            except (ConnectionResetError, ssl.SSLEOFError):
                pass
        if not send_key and msg == r"\q":
            client_socket.close()
            break
        try:
            client_socket.send(bytes(msg, "utf8"))
        except (ConnectionResetError, ssl.SSLEOFError):
            pass


def gen_answer(is_veto):
    global p, i, x_i, public_keys
    gy = 1
    n = 3
    user_number = i
    tmp_public_keys = [x[1] for x in sorted([[x, y] for x, y in public_keys.items()])]
    for j in range(user_number):
        gy = gy * tmp_public_keys[j] % p
    for j in range(user_number + 1, n):
        gy = gy * modinv(tmp_public_keys[j], p) % p
    if is_veto:
        x_i += random.randint(0, p - 1)
    return gy ** x_i % p


def gen_g_x(g, p):
    r = random.randint(0, p - 1)
    return g ** r % p


g = None
p = None
i = None
x_i = None
public_keys = {}
is_veto = None
last_answer = None
send_key = False

if __name__ == '__main__':
    ADDR = (HOST, PORT)
    server_sni_hostname = 'veto.pl'
    server_cert = 'server.crt'
    client_cert = 'client.crt'
    client_key = 'client.key'

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    s = socket(AF_INET, SOCK_STREAM)
    client_socket = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
