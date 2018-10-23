"""
Fetch Content with resolved chunking
"""

import argparse
import base64

from PiCN.Packets import Name
from PiCN.ProgramLibs.Fetch import Fetch
from PiCN.Layers.PacketEncodingLayer.Encoder import NdnTlvEncoder
from PiCN.Layers.PacketEncodingLayer.Encoder import SimpleStringEncoder


def main(args):
    #name = Name(args.name)
    name_str = args.name
    if args.code is not None and "#" in name_str:
        try:
            f_content = read_content(args.code)
        except:
            print("Could not open file!")
            return
        base64_content = '"' + base64.b64encode(f_content.encode()).decode() + '"'
        name_str = name_str.replace('#', base64_content)
    name = unescape_str_to_Name(name_str)
    name.format = args.format
    #name = unescape_name(name)

    encoder = NdnTlvEncoder() if args.format == 'ndntlv' else SimpleStringEncoder
    fetchTool = Fetch(args.ip, args.port, encoder=encoder, autoconfig=args.autoconfig)

    content = fetchTool.fetch_data(name)
    print(content)

    fetchTool.stop_fetch()

def read_content(name):
    file = open(name, "r")
    return file.read()


def unescape_name(name: Name):
    r = []
    for n in range(0, len(name.string_components)):
        r.append(name.string_components[n].replace("%2F", "/"))
    name.string_components = r
    return name

def unescape_str_to_Name(name: str) -> Name:
    r = []
    if '[' not in name or ']' not in name:
        return Name(name)
    tmp_comps1 = name.split('[')
    tmp_comps2 = tmp_comps1[1].split(']')
    if tmp_comps1[0].endswith("/"):
        tmp_comps1[0] = tmp_comps1[0][:-1]
    if tmp_comps2[1].startswith("/"):
        tmp_comps2[1] = tmp_comps2[1][1:]
    comps = [tmp_comps1[0], tmp_comps2[0], tmp_comps2[1]]

    name = Name(comps[0])
    name += comps[1]
    name += comps[2]

    return name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ICN Fetch Tool')
    parser.add_argument('--format', choices=['ndntlv', ' simple'], type=str,
                        default='ndntlv', help='default is: "ndntlv"')
    parser.add_argument('-a', '--autoconfig', action='store_true')
    parser.add_argument('ip', type=str,
                        help="IP addr of forwarder")
    parser.add_argument('port', type=int,
                        help="UDP port of forwarder")
    parser.add_argument('name', type=str,
                        help="ICN name of content to fetch")
    parser.add_argument('--code', type=str,
                        help="code from file to be published", default=None)
    args = parser.parse_args()

    main(args)
