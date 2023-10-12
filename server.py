import time
import socket
import ssl
import select
import os
import struct as st
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from datetime import datetime
from config import CACHE_DIR

hdrsize = 11
bufsize = 2048
accepttimeout = 5
readtimeout = 3
maxclients = 10
signatura = b'ncb'


class DataHeader:
    # filetypes: 0 - None, 1 - image, 2 - text, 3 - file
    def __init__(self, addr):
        # Заголовок
        self.filesize = 0
        self.filetype = 0
        self.addr = addr
        self.fnlen = 0
        # Имя файла это часть контента, не заголовка, т.к. нет фиксированной длины строки
        self.filename = ''

    def read(self, data):
        l = len(data)
        if l < hdrsize: return False
        if data[:3] == signatura:
            self.filesize, self.filetype, self.fnlen = st.unpack('IBH', data[3:])
            return True
        else:
            return False

    def toBytes(self):
        fn = self.filename.encode('utf-8')
        self.fnlen = len(fn)
        return signatura + st.pack('IBH', self.filesize, self.filetype, self.fnlen) + fn


class StreamServer(QtCore.QObject):
    onFinish = QtCore.pyqtSignal(str)
    onRead = QtCore.pyqtSignal(DataHeader)

    def __init__(self, thread, sets):
        super().__init__()
        self.sock = None
        self.sets = sets
        self.keep_running = False
        self.thread = thread
        self.childlist = []
        self.ipport = ('0.0.0.0', sets.serverport)
        if self.sets.ssl:
            self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self.sslcontext.load_cert_chain(certfile=self.sets.ssl_certfile, keyfile=self.sets.ssl_keyfile)
        else:
            self.sslcontext = None

    def childread(self, hdr):
        self.onRead.emit(hdr)

    def childFinish(self, receiver):
        self.childlist.remove(receiver)
        if (not self.keep_running) and (len(self.childlist) == 0):
            self.onFinish.emit('')
            if self.thread is not None:
                self.thread.quit()
                self.thread = None

    def newThread(self, client, addr):
        if self.sslcontext is not None:
            try:
                sock = self.sslcontext.wrap_socket(client, server_side=True)
            except Exception as e:
                print(str(e))
                client.close()
                return
        else:
            sock = client
        thread = QThread()
        receiver = Receiver(thread, sock, addr, self.onRead)
        receiver.onFinish.connect(self.childFinish)
        # receiver.onRead.connect(self.childread)
        receiver.moveToThread(thread)
        thread.started.connect(receiver.run)
        self.childlist.append(receiver)
        thread.start()

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(accepttimeout)
        try:
            self.sock.bind(self.ipport)
        except socket.error:
            print('can not open port', self.ipport)
            self.onFinish.emit('Ошибка открытия порта, возможно он уже занят')
            self.thread.quit()
            self.thread = None
            return
        except Exception as e:
            print('error', e)
        else:
            print('server listening:', self.ipport)
        self.sock.listen(maxclients)
        self.keep_running = True
        while self.keep_running:
            try:
                client, addr = self.sock.accept()
            except socket.timeout:
                time.sleep(0.5)
                # print('sleep')
            except socket.error as err:
                self.onFinish.emit(f'error accept: {err}')
                self.keep_running = False
                break
            except Exception as e:
                print('error acception', e)
            else:
                if addr[0] in self.sets.blacklist:
                    print(f'client not accepted, because ip {addr[0]} in blacklist')
                    client.close()
                elif self.sets.onlywhitelist and addr[0] not in self.sets.whitelist:
                    print(f'client not accepted, because ip {addr[0]} not in whitelist')
                    client.close()
                else:
                    print('client accepted:', addr)
                    self.newThread(client, addr)

        self.sock.close()
        print('server stoped')
        if len(self.childlist) == 0:
            self.onFinish.emit('')
            self.thread.quit()
            self.thread = None


class Receiver(QtCore.QObject):
    onFinish = QtCore.pyqtSignal(QtCore.QObject)

    # onRead = QtCore.pyqtSignal(DataHeader)

    def __init__(self, thread, sock, addr, onRead):
        super().__init__()
        sock.settimeout(readtimeout)
        self.sock = sock

        self.keep_running = True
        self.addr = addr
        self.thread = thread
        self.onRead = onRead

    def stop(self):
        self.keep_running = False

    def read(self, bs):
        try:
            data = self.sock.recv(bs)
        except socket.timeout:
            return None, 2
        except socket.error as err:
            print(f'error read: {err}')
            return None, 0
        else:
            return data, 1

    def readfilename(self, hdr):
        data, state = self.read(hdr.fnlen)
        if state == 1:
            hdr.filename = data.decode('utf-8')
        return state

    def run(self):
        sleepcount = 0
        recvsize = 0
        fls = 0
        hdr = None
        self.keep_running = True
        f = None
        while self.keep_running:
            if hdr is None:
                data, state = self.read(hdrsize)
                if state == 2:
                    time.sleep(0.5)
                    sleepcount += 1
                    if sleepcount > 5:
                        break
                    else:
                        continue
                elif state == 0:
                    break
                hdr = DataHeader(self.addr)
                hdr.filename = None
                if not hdr.read(data):
                    hdr = None
                    break
                if hdr.filesize == 0:
                    hdr = None
                    break
                if hdr.fnlen == 0:
                    now = datetime.now()
                    hdr.filename = now.strftime("%d-%m-%Y_%H-%M")
                else:
                    state = self.readfilename(hdr)
                    if state == 2:
                        time.sleep(0.5)
                        sleepcount += 1
                        if sleepcount > 5:
                            break
                        else:
                            continue
                    elif state == 0:
                        break
            elif hdr.filename is None:
                state = self.readfilename(hdr)
                if state == 2:
                    time.sleep(0.5)
                    sleepcount += 1
                    if sleepcount > 5:
                        break
                    else:
                        continue
                elif state == 0:
                    break

            fls = hdr.filesize
            if f is None:
                f = open(os.path.join(CACHE_DIR, hdr.filename), 'wb')
            data, state = self.read(2048)
            if state == 2:
                time.sleep(0.5)
                continue
            elif state == 0:
                f.close()
                break
            recvsize += len(data)
            while (len(data) > 0):
                f.write(data)
                if (recvsize >= hdr.filesize):
                    break
                data, state = self.read(2048)
                recvsize += len(data)
                if state != 1:
                    self.keep_running = False
                    break
            f.close()
            break
        self.sock.close()
        if hdr is not None:
            self.onRead.emit(hdr)
        self.onFinish.emit(self)
        self.thread.quit()
        self.thread = None


class Sender(QtCore.QObject):
    onError = QtCore.pyqtSignal(str)

    def __init__(self, hdr, data, ipport, thread, ssl=False):
        super().__init__()
        self.hdr = hdr
        self.data = data
        self.ipport = ipport
        self.thread = thread
        self.ssl = ssl

    def run(self):
        # This will run when you call .start method
        if self.hdr.filesize < 3:
            print('Sender.run: filesize < 3')
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        if self.ssl:
            sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA")

        try:

            sock.connect(self.ipport)
            sock.settimeout(None)
            sock.sendall(self.hdr.toBytes())
            sock.sendall(self.data)
            sock.close()
        except socket.timeout:
            print('sender error connection, time out')
            self.onError.emit(f'error connect to: {self.ipport}, timeout')
        except socket.error:
            print('sender error connection')
            self.onError.emit(f'error connect to: {self.ipport}')
        except Exception as e:
            print('Sender exception: %s' % e)
        # else:
        #    print('sended ok')
        self.thread.quit()
        self.thread = None


class SenderFile(QtCore.QObject):
    onError = QtCore.pyqtSignal(str)

    def __init__(self, hdr, ipport, thread, ssl=False):
        super().__init__()
        self.hdr = hdr
        self.ipport = ipport
        self.thread = thread
        self.ssl = ssl

    def closethread(self):
        self.thread.quit()
        self.thread = None

    def run(self):
        if not os.path.isfile(self.hdr.filename):
            print('SenderFile run error no such file: ', self.hdr.filename)
            self.closethread()
            return
        self.hdr.filesize = os.path.getsize(self.hdr.filename)
        if (self.hdr.filesize < 3): return
        try:
            f = open(self.hdr.filename, 'rb')
        except Exception as e:
            print(e.message())
            self.closethread()
            return

        self.hdr.filename = os.path.basename(self.hdr.filename)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        if self.ssl:
            sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA")

        buf = self.hdr.toBytes()
        # buf += self.hdr.filesize.to_bytes(4,'big') + self.hdr.filetype.to_bytes(2,'little') + str.encode(self.hdr.ext)

        try:
            sock.connect(self.ipport)
            sock.settimeout(None)
            sock.sendall(buf)
        except socket.timeout:
            f.close()
            self.onError.emit(f'error TIMEOUT connect to: {self.ipport}, timeout')
            self.closethread()
            return
        except socket.error:
            f.close()
            self.onError.emit(f'error connect to: {self.ipport}')
            self.closethread()
            return
        except Exception as e:
            f.close()
            self.onError.emit(f'error connect to: {self.ipport} {str(e)}')
            self.closethread()
            return
        readed = 0
        while True:
            r = 0
            try:
                data = f.read(2048)
                r = len(data)
            except:
                break
            if r > 0:
                readed += r
                sock.sendall(data)
            else:
                break
        f.close()
        sock.close()
        self.closethread()


'''
import socket
import ssl

# SET VARIABLES
packet, reply = "<packet>SOME_DATA</packet>", ""
HOST, PORT = 'XX.XX.XX.XX', 4434

# CREATE SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

# WRAP SOCKET
wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")

# CONNECT AND PRINT REPLY
wrappedSocket.connect((HOST, PORT))
wrappedSocket.send(packet)
print wrappedSocket.recv(1280)

# CLOSE SOCKET CONNECTION
wrappedSocket.close()
'''
