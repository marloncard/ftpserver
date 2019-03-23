import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    """
    Define new user having full r/w permissions and a read-only 
    anonymous user
    perm (Permissions):
    *Read*
    'e' = change directory(CWD, CDUP commands)
    'l' = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
    'r' = retrieve file from the server (RETR command)
    *Write*
    'a' = append data to an existing file (APPE command)
    'd' = delete file or directory (DELE, RMD, commands)
    'f' = rename file or directory (RNFR, RNTO commands)
    'm' = create directory (MKD command)
    'w' = store a file to the server (STOR, STOU commands)
    'M' = change file mode / permission (SITE CHMOD command)
    'T' = change file modification time (SITE MFMT command)
    """
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    server = FTPServer(address, handler)

    # set limit for connections
    server.max_cons = 5
    server.max_cons_per_ip = 2

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()
