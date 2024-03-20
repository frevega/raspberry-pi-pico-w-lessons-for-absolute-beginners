import  socket

serverAddress = ("192.168.100.242", 2222)
bufferSize = 1024
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    cmd = input("What's your command? ")
    cmdEncoded = cmd.encode("utf-8")
    udpClient.sendto(cmdEncoded, serverAddress)
    message, address = udpClient.recvfrom(bufferSize)
    messageDecoded = message.decode("utf-8")
    print(address[0], messageDecoded)
    
