# Socket Chat

Socket Chat project is server and client socket chat implementation written on Python.

![Socket Chat Preview](.\public\socket-chat-preview.png)

## Usage

To start server, within project folder execute the following:

```bash
python3 server.py
```
Note: there must be only one instance of a server that will run locally on 15397 port.

Server allows following launch parameters: 
* `-address` for binding server address, 
* `-port` for binding server port.

To start client, within project folder execute the following:
```bash
python3 client.py
```
Note: server accepts up to 2048 clients.

Client allows following launch parameters: 
* `-s_address` for binding server address,
* `-s_port` for binding server port,
* `-address` for binding client address,
* `-port` for binding client port.

## Features
Socket Chat allows chatting within one room between currently connected users. 
Server supports a set of commands that should follow with `cmd!` prefix. Those commands are:

### `private-message` 
Send private messages to one or many users. Full syntax is: 
```
cmd!private-message [user1] [user2] ... [userN]: [private message]
```
Example:
```
cmd!private-message max pasha: is message sent to more than 1 person is considered private?
```

### `rock-paper-scissors`
Play rock-paper-scissors game with server. While playing game you can't start another game; 
while playing you can keep chatting with other people. Game ends when server answers on your rock/paper/scissors choice.
Syntax for starting game:
```
cmd!rock-paper-scissors 
```
Syntax for throwing rock/paper/scissors
```
cmd!game-step: [rock/paper/scissors]
```
Example:
```
cmd!rock-paper-scissors
server > Rock-paper-scissors game started
cmd!game-step: rock
server > Server chose scissors, you won, the game is over
```

### `participants` and `participants-count`
Check who is in chat by sending `cmd!participants` command to server or see how many users are in chat by sending
`cmd!participants-count` command. Examples:
```
cmd!participants
server > List of participants: clientOne, clientTwo, clientThreee
cmd!participants-count
server > The number of participants is 3
```

### `server-time`
Check server uptime by sending `cmd!server-time` command. Example:
```
cmd!server-time
server > Server uptime: 00h 41m 03s
```

### `Ctrl + C` or type !EXIT! to leave chat
Leave chat at anytime by using world-known interruption key combination or type message !EXIT!!
Example:
```
^C
2020-09-25 00:50:30,956 - Closing client ...
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
