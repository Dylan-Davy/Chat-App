### Chat App

This application was built as a personal project with the goal of learning how to use the Qt framework, as well as how to design and build an larger application that utilises a database, threaded server, and multiple connected clients. An early version of this application was used towards an assignment in my Master of Software Development.

#### Running the application:
To run this application, you must have Python installed and install the packages listed in 
requirements.txt, as well as setup the PostgreSQL database. 

The server can be run from the command line, calling the Server.py file when in the App directory. The database details in ServerThread.py need to match those of your PostgreSQL database.

Clients can be run from the command line, calling the Client.py file when in the App directory.

Alternatively the server and client can be built into executibles using Pyinstaller, again executed from the App directory.

#### Using the application:
New users can be registered, and then logged in to through a client. Message other existing users by entering their name into the top text input of the home screen you reach after logging in, and then sending them a message. Navigate back or logout using the back button. Images and contacts are both scrollable lists, that automatically update and/or generate when new messages come in. The images below show the screens in the application.

![Register](https://user-images.githubusercontent.com/38117354/107001623-d2b6ba00-67ee-11eb-95eb-e9237f0b06e3.png)
![Home](https://user-images.githubusercontent.com/38117354/107001639-d9ddc800-67ee-11eb-844c-d03c99c0479b.png)
![Messages](https://user-images.githubusercontent.com/38117354/107001641-dc402200-67ee-11eb-9419-a079a9555217.png)
![Image](https://user-images.githubusercontent.com/38117354/107001653-e2360300-67ee-11eb-871d-4c052abbdc2b.png)

If a client recieves a message while logged in, the GUI will automatically update to include the new message.

All data transfer between clients and the server are encrypted, and login details are hashed before being saved in the database. (WIP)

Sending and recieving of images is supported, selected from your files. (WIP)
