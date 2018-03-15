"""Management Tool for PiCN Forwarder and Repo"""

import sys
import argparse
import socket

from PiCN.Mgmt import MgmtClient
from PiCN.Packets import Name

def main(args, help_string):

    mgmt_client = MgmtClient(args.port)

    if args.command == "shutdown":
        try:
            mgmt_client.shutdown()
            print("Shutdown command sent.")
        except ConnectionRefusedError:
            print("Connection Refused. Repo not running?")

    elif args.command == "getrepoprefix":
        try:
            data = mgmt_client.get_repo_prefix()
            print(data)
        except ConnectionRefusedError:
            print("Connection Refused. Repo not running?")

    elif args.command == "getrepopath":
        try:
            data = mgmt_client.get_repo_path()
            print(data)
        except ConnectionRefusedError:
            print("Connection Refused. Repo not running?")

    elif args.command == "newface":
        if len(args.parameters) != 2:
            print("Require IP PORT as parameter")
            sys.exit(-2)
        addr = args.parameters[0]
        port = args.parameters[1]
        try:
            resolved_hostname = socket.inet_aton(addr)
        except:
            resolved_hostname = None
        if not resolved_hostname:
            try:
                resolved_hostname = socket.gethostbyname()
            except:
                print("Resolution of hostname failed.")
                sys.exit(-2)
        else:
            resolved_hostname = addr
        try:
            data = mgmt_client.add_face(resolved_hostname, port)
        except:
            print(help_string)

    elif args.command == "newforwardingrule":
        if len(args.parameters) != 2:
            print("Requires prefix and face id (returned by newface)")
            sys.exit(-2)
        try:
            data = mgmt_client.add_forwarding_rule(Name(args.parameters[0]), args.parameters[1])
        except ConnectionRefusedError:
            print("Connection Refused. Forwarder not running?")
        except:
            print(help_string)

    elif args.command == "newcontent" or args.command == 'addcontent':
        try:
            data = mgmt_client.add_new_content(Name(args.parameters.split(":", 1)[0]), args.parameters.split(":", 1)[1])
        except ConnectionRefusedError:
            print("Connection Refused. Forwarder not running?")
        except:
            print(help_string)
    if data is not None:
        print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Management Tool for PiCN Forwarder and Repo')
    parser.add_argument('-i', '--ip', type=str, default='127.0.0.1',
                            help="IP address or hostname of forwarder (default: 127.0.0.1)")
    parser.add_argument('-p', '--port', type=int, default=9000, help="UDP port of forwarder(default: 9000)")
    parser.add_argument('command', type=str, choices = ['shutdown', 'getrepoprefix', 'getrepopath', 'newface', 'newforwardingrule', 'newcontent'], help="Management Command")
    parser.add_argument('parameters', type=str, nargs='+', help="Command Parameter")
    args = parser.parse_args()
    help_string = parser.format_help()
    main(args, help_string)


# print("\t\tshutdown")
# print("\t\tgetrepopath")
# print("\t\tgetrepoprefix")
# print("\t\tnewface ip:port")
# print("\t\tnewforwardingrule prefix:face")
# print("\t\tnewcontent name:content")
