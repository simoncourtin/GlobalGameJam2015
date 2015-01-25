def recup_message(socket):
    request = ""
    car = socket.recv(1)
    while car != "@":
        request += car
        car = socket.recv(1)

    return request
