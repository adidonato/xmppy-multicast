# Blaterare
####(Jabber in Italian), a python multicaster command line jabber client.

## Dependencies
```
pip install -r requirements.txt
```

## Info
The client handles one or more JIDs and sends a message, then disconnects.
Ideal to broadcast the same message to multiple users

## TODO
Handle a file with list of JID for reoccuring broadcasts

## Usage

Example:
```
~$ ./blaterare.py -j user@jabber.org -t another_user@jabber.org yet_another_user@jabber.org -p super_secret_password -m "Wassup users??"
```
<p>You can avoid typing username and password each time by creating a ~/.blaterare file with jid and password (if the file does not exist you will be prompted for credentials), e.g:</p>
```
JID=user@jabber.org
PASSWORD="*******"
RESOURCE=wicked-cool-python-client
```
The client takes none or all the possible arguments.

See available arguments
```./blaterare.py -h```.

## License

See License file.
