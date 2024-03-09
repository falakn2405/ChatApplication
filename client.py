import socket
import threading
import tkinter as tk

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.setup_ui()
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('127.0.0.1', 5555))
        except Exception as e:
            print("Error connecting to server:", e)
            self.master.destroy()

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def setup_ui(self):
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)

        self.chat_log = tk.Text(self.chat_frame, state=tk.DISABLED)
        self.chat_log.pack(expand=True, fill=tk.BOTH)

        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(fill=tk.BOTH)

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                self.display_message("Server", data)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode())
                self.display_message("You", message)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                print("Error sending message:", e)

    def display_message(self, sender, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{sender}: {message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END) 

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
