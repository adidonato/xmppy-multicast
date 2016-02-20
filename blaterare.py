#! /usr/bin/python
__Author__ = 'Angelo Di Donato'
import os,xmpp,time
import sys
import logging
import getpass
from optparse import OptionParser

class MyParser(OptionParser):
        """
        Blaterare (Jabber in Italian), a python multicaster command line jabber client. See -h for more details.
        """
        def format_epilog(self, formatter):
            """
            Format epilog into something readable.
            """
            return self.epilog

def cb(option, opt_str, value, optp):
        """
        Handle one or more email addresses and send to callback.
        """
        args=[]
        for arg in optp.rargs:
                if arg[0] != "-":
                        args.append(arg)
                else:
                        del optp.rargs[:len(args)]
                        break
        if getattr(optp.values, option.dest):
                args.extend(getattr(optp.values, option.dest))
        setattr(optp.values, option.dest, args)

if __name__ == '__main__':
    optp = MyParser(epilog=
"""
Blaterare (Jabber in Italian), a python multicaster command line jabber client.
The client handles one or more JIDs and sends a message, then disconnects.
Example: ~$ ./blaterare.py -j user@jabber.org -t another_user@jabber.org yet_another_user@jabber.org -p super_secret_password -m "Wassup users??"
Avoid typing username and password each time by creating a ~/.blaterare file with jid and password (if the file does not exist you will be prompted for credentials), e.g:
JID=user@jabber.org
PASSWORD=*******
RESOURCE=wicked-cool-python-client
This client takes none or all the possible arguments.
See available arguments above.
""")
    #optp = OptionParser(epilog=desc)


    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-t", "--to", dest="to", callback=cb,
                    action="callback", help="one or more JIDs to send the message to")
    optp.add_option("-m", "--message", dest="message",
                    help="message to send")

    opts, args = optp.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

if len(sys.argv) < 2:
    print "You forgot the recipient and/or the message dawg!!\n I'm now gonna prompt you for them.\n Avoid this prompt with\nSyntax: blaterare JID text\n"
    opts.to = raw_input("Send To: ")
    opts.message = raw_input("Message: ")

if opts.to is None:
    opts.to = raw_input("Send To: ")
tojid=opts.to

if opts.message is None:
    opts.message = raw_input("Message: ")
text=''.join(opts.message)

jidparams={}

if os.access(os.environ['HOME']+'/.blaterare',os.R_OK):
    for ln in open(os.environ['HOME']+'/.blaterare').readlines():
        if not ln[0] in ('#',';'):
            key,val=ln.strip().split('=',1)
            jidparams[key.lower()]=val
for mandatory in ['jid','password']:
    if mandatory not in jidparams.keys():
        if opts.jid is None:
             opts.jid = raw_input("Username: ")
        if opts.password is None:
            opts.password = getpass.getpass("Password: ")
        jidparams['jid'] = opts.jid
        jidparams['password'] = opts.password
        print '\nNext time you can avoid this by pointing ~/.blaterare config file to valid JID for sending messages.'

if xmpp.protocol.JID(jidparams['jid']) is None:
    jid=opts.jid
else:
    jid=xmpp.protocol.JID(jidparams['jid'])

cl=xmpp.Client(jid.getDomain(),debug=[])

con=cl.connect()
if not con:
    print 'could not connect, dawg!'
    sys.exit()
print 'connected with',con
auth=cl.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())
if not auth:
    print 'could not authenticate, dawg!'
    sys.exit()
print 'authenticated using',auth

#cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
print str(opts.to).count('@')
print opts.to

if str(opts.to).count('@') > 1:
    for to in tojid:
        cl.send(xmpp.protocol.Message(to,text))
        print 'blaterato %s a %s' % (text, to)
        time.sleep(1)
else:
    id=cl.send(xmpp.protocol.Message(tojid[0],text))
    print 'blaterato %s a %s' % (text, tojid)

time.sleep(1)
cl.disconnect()
