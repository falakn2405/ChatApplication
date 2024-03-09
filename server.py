import socket
import threading
import tkinter as tk

class ChatServer:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Server")

        self.setup_ui()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 5555))
        self.server_socket.listen(5)
        self.update_server_status("Server listening on port 5555...")
        self.client_sockets = []

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def setup_ui(self):
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)

        self.chat_log = tk.Text(self.chat_frame, state=tk.DISABLED)
        self.chat_log.pack(expand=True, fill=tk.BOTH)

        self.server_status_label = tk.Label(self.chat_frame, text="")
        self.server_status_label.pack()

        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(fill=tk.BOTH)

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def accept_clients(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.update_server_status(f"Connected to {address}")
            self.client_sockets.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                self.broadcast_message(data)
            except Exception as e:
                print("Error receiving message:", e)
                break

        self.client_sockets.remove(client_socket)
        client_socket.close()

    def broadcast_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"Client: {message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)  

    def send_message(self):
        message = self.message_entry.get()
        if message:
            for client_socket in self.client_sockets:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print("Error sending message:", e)
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(tk.END, f"Server: {message}\n")
            self.chat_log.config(state=tk.DISABLED)
            self.chat_log.see(tk.END)
            self.message_entry.delete(0, tk.END)

    def update_server_status(self, status):
        self.server_status_label.config(text=status)

def main():
    root = tk.Tk()
    app = ChatServer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
