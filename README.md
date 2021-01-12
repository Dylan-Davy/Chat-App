Chat App

This application was built as a personal project with the goal of learning how to use the Qt framework, as well as how to design and build an larger application that utilises a database, threaded server, and multiple connected clients. An early version of this application was used towards an assignment in my Master of Software Development.

Running the application:
To run this application, you must have Python installed and install the packages listed in 
requirements.txt, as well as setup the PostgreSQL database. 

The server can be run from the command line, calling the Server.py file when in the App directory. The database details in ServerThread.py need to match those of your PostgreSQL database.

Clients can be run from the command line, calling the Client.py file when in the App directory.

Alternatively the server and client can be built into executibles using Pyinstaller, again executed from the App directory.

Using the application:
New users can be registered, and then logged in to through a client. Message other existing users by entering their name into the top text input of the home screen you reach after logging in, and then sendding them a message.

If a client recieves a message while logged in, the GUI will automatically update to include the new message.

All data transfer between clients and the server are encrypted, and login details are hashed before being saved in the database. (WIP)

Sending and recieving of images is supported, selected from your files. (WIP)