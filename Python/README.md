# How to use this 

## Server Side

All you have to do to setup the server is call server.py and pass an <optional>
command line port. If you do pass the port, the system will try to use said
port, else it will try to connect to the default port.

```
./server.py <port no>
```

## Client Side

Basically, every connection has an associated ID with it. Every connection you
make has to be followed with two **compulsory** command-line arguments, viz. `<port>` and `<id>`.
Thus, every connection has to be of the form:

```
./client.py <port> <id> ...
```

### Types of command line arguments

- `<port> <id>`: Default arguments, have to be passed with every request
- `-<argument>`: Server-side arguments, have to be passed to establish and
  remove a connection
- `--<command>`: Command-type arguments, used to signal some action to the
  server.
- `@<variable>`: Variable arguments. Used to signal the filename(S) for sending
  and receiving.


### Sequence of Steps

- First of all, every given ID has to be _connected_ to the server. 
```
./client.py <port> <id> -connect
```
- Once, a connect request has been sent, this id is added to the server store,
  and marked as having initiated a connection. Every subsequent request has to
  be followed with a `-connected` system flag. 
- After this step, the client can request a command.
    - `--list-files`: This command will list the files available at the server
      end.
```

./client.py <port> <id> -connected --list-files

    ```
    
    - `--receive-files @filename1 @filename2`: This command will send a
      request to receive filename1 and filename2 from the server.
    
```

./client.py <port> <id> -connected --receive-files @filename1 @filename2 ...

    ```
- Once the receving is done, the given ID can be _disconnected_ from the server.
  This ID system allows a fix set of users to only connect to the server,
  allowing a layer of manual control on the number of connections.

```

./client.py <port> <id> -disconnect

```

## Status

### Features

- Connection establishment
- Multiple error handling for various sections
- Multiple ID-ed users and connections
- JSON based API with multiple command types

### To Be Implemented

- Multiple file transfer 
- Threading support

