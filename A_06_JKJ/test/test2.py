# 引入Socket模块
import socket
# 创建Socket对象
socket_client = socket.socket()
# 连接到服务端
socket_client.connect(("localhost", 8888))
# 与服务端通信
while True:
    send_msg = input("请输入要发送的消息: ")
    if send_msg == "exit":
        break
    socket_client.send(send_msg.encode("UTF-8"))
    recv_data = socket_client.recv(1024).decode("UTF-8")
    print(f"收到服务端的回复为: {recv_data}")

# 关闭Socket对象
socket_client.close()