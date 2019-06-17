"""Server for multithreaded (asynchronous) chat application."""
import random
import ssl
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from common import HOST, PORT, BUFF_SIZE, QUESTION, is_veto

index = 0

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("{} has connected.".format(client_address))
        client = context.wrap_socket(client, server_side=True)
        client.send(str("Type your name: ").encode('utf-8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def get_name(client):
    global index
    name = client.recv(BUFF_SIZE)
    name = name.decode("utf8")
    if name not in clients.values():
        welcome = r'Welcome {}! If you ever want to quit, type \q to exit.'.format(name)
        client.send(str(welcome).encode('utf-8'))
        time.sleep(0.01)
        client.send(str('Your ID is {}'.format(index)).encode('utf-8'))
        client_id = index
        index += 1
    else:
        client.send(bytes('This nickname is already taken. Please provide different nick: ', "utf8"))
        return get_name(client)
    return name, client_id


def get_g_p(client, client_id):
    global response_p_g, g, p, agreement, alreadyUsedID, ktory_wybiera
    if client_id == ktory_wybiera:
        msg = 'Suggest please g,p [number comma number]'
        client.send(str(msg).encode('utf-8'))
        response = client.recv(BUFF_SIZE).decode('utf-8')
        response_p_g[client_id] = response
        g, p = [int(x) for x in response.split(',')]
        while not len(clients) == 3:
            pass
        msg = 'Proposed g, p = {}.'.format(response)
        broadcast(str(msg).encode('utf-8'))
    else:
        response = client.recv(BUFF_SIZE).decode('utf-8')
        response_p_g[client_id] = response
        if response == 'y':
            agreement += 1
            print('Agreed on g = {} and p = {}'.format(g, p))
            while len(response_p_g) != 2 or alreadyUsedID:
                pass
        elif response == 'n':
            broadcast(bytes('You have to accept. Restars server and accepts next time.', 'utf-8'))


def handle_client(client):
    global clients_public_keys, client_answers, p, agreement, ktory_wybiera, should_print
    name, client_id = get_name(client)
    msg = "{} join chat!".format(name)
    broadcast(str(msg).encode('utf-8'))
    clients[client] = name
    get_g_p(client, client_id)
    alreadyUsedID = True
    if client_id == ktory_wybiera:
        broadcast(bytes('Push enter to sent the public key', 'utf-8'))
    first = True
    while True:
        try:
            msg = client.recv(BUFF_SIZE)
            if msg == bytes(r"\q", "utf8"):
                client.close()
                del clients[client]
                broadcast(str("{} has just left the chat".format(name)).encode('utf-8'))
                break
            else:
                if msg.decode('utf-8').isdigit() and first:
                    client.send(str('You said {}. Waiting fot the rest of people.'.format(int(msg))).encode('utf-8'))
                    clients_public_keys[client_id] = int(msg)
                    first = False
                    if len(clients_public_keys.keys()) == 3:
                        broadcast(str('Everyone has send pub_key:\n{}'.format(clients_public_keys)).encode('utf-8'))
                        time.sleep(0.01)
                        broadcast(str('You will see QUESTION, please answer').encode('utf-8'))
                        time.sleep(0.01)
                        broadcast(str('QUESTION: {} [t/n]'.format(QUESTION)).encode('utf-8'))
                        time.sleep(0.01)
                elif msg.decode('utf-8').isdigit():
                    client_answers[client_id] = int(msg.decode('utf-8'))
                    time.sleep(0.01)
                    if len(client_answers.keys()) == 3 and should_print:
                        tmp_client_answers = [x[1] for x in sorted([[x, y] for x, y in client_answers.items()])]
                        result = is_veto(tmp_client_answers, p)
                        msg = 'Your answer is: {}'.format(str(result))
                        broadcast(str(msg).encode('utf-8'))
                        should_print = False
        except ConnectionResetError:
            del clients_public_keys[client_id]
            del clients[client]


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(str(prefix).encode('utf-8') + msg)


g = 3
p = 2003
alreadyUsedID = False
agreement = 1
answer = 0
should_print = True
response_p_g = {}
clients = {}
addresses = {}
clients_public_keys = {}
client_answers = {}
ktory_wybiera = random.randint(0, 2)
ADDR = (HOST, PORT)

server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
