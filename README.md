# NetBuffer
Select Language: **English**, [Russian](https://github.com/GennadiyVick/NetBuffer/blob/master/README-ru.md)  

Network clipboard program uses tcp/ip stack as base protocol
You can copy at a time: text, picture or 1 file, copy several
files are not currently supported.
How it works: you copy text, picture or file to the clipboard, then
right mouse button on the program shortcut in the tray calls the context menu or
the left mouse button immediately sends the contents of the buffer to the selected host.
Hosts can be added by clicking send in the context menu in the opened
window opposite the field "Where" there is a button "..." everything is intuitively clear there.

When data arrives on the socket, the data type is passed in the header.
The data is automatically transferred to the buffer if the following conditions are met:
- the ip address from which the data came is in the white list (see settings)
- if the corresponding option is enabled in the settings.  

in all other cases a pop-up window opens
at the bottom and right of the screen, which displays the content text, picture
and buttons copy, save to file, cancel and block ip addresses,
if you click on blocking, then the ip address is blacklisted (see settings),
on an incoming connection, if this address is blacklisted,
then there is an immediate shutdown.

In the settings, you can enable the use of an SSL secure protocol, for this you must
have a certificate and a key. They can be generated with the command:
```console
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
```
in this case, a self-signed certificate will be generated, that is, a certificate and a key in one file.
In settings, you can enter the name of the certificate file without specifying the entire path to the file; in this case, the certificate must be located in the same directory with the program.
Attention!! Antiviruses can block ssl traffic.

## Dependencies and running the program!
### WINDOWS:
You must have `python3` interpreter installed, download [python.org](https://www.python.org/downloads/)
after installation, you need to install the `PyQt5` library, to install in the console (cmd) enter:
```console
python -m pip install pyqt5
```
now you can run the program with the command
```console
pythonw program_path\netbuffer.py
```
or create a shortcut and specify this command.
After launch, the program icon should appear in the tray.

### Linux:
on linux OS `python3` should already be pre-installed check with command
```console
python3 --version
```
and you also need to install the `PyQt5` library with the command:
```console
pip3 install pyqt5
```
now you can run the program with the command
```console
python3 program_path\netbuffer.py
```
or create a desktop icon with this command.
