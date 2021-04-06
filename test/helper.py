import struct
import socket
import logging
from scapy.all import *
MAX_UINT32 = 0xFFFFFFFF
MAX_BITI_CHECKSUM = 16
MAX_SEGMENT = 1400

def compara_endianness(numar):
    '''
    https://en.m.wikipedia.org/wiki/Endianness#Etymology
        numarul 16 se scrie in binar 10000 (2^4)
        pe 8 biti, adaugam 0 pe pozitiile mai mari: 00010000
        pe 16 biti, mai adauga un octet de 0 pe pozitiile mai mari: 00000000 00010000
        daca numaratoarea incepe de la dreapta la stanga:
            reprezentarea Big Endian (Network Order) este: 00000000 00010000
                - cel mai semnificativ bit are adresa cea mai mica
            reprezentarea Little Endian este: 00010000 00000000
                - cel mai semnificativ bit are adresa cea mai mare 
    '''
    print ("Numarul: ", numar)
    print ("Network Order (Big Endian): ", [bin(byte) for byte in struct.pack('!H', numar)])
    print ("Little Endian: ", [bin(byte) for byte in struct.pack('<H', numar)])


def create_header_emitator(seq_nr, checksum, flags='S'):
    if (flags=='S'):
        spf = 0b100 # seteaza flag S = 1
    if (flags=='F'):
        spf=0b001
    if (flags=='P'):
        spf=0b010
    spf_zero = spf << 13
    header = struct.pack('!LHH', seq_nr, checksum, spf_zero)
    return header
    
def parse_header_emitator(octeti):
    
    
    seq_nr, checksum, spf = struct.unpack('!LHH',octeti)
    flags = ''
    if spf & 0b100:
        # inseamna ca am primit S
        flags = 'S'
    elif spf & 0b001:
        # inseamna ca am primit F
        flags = 'F'
    elif spf & 0b010:
        # inseamna ca am primit P
        flags = 'P'
    spf_zero = spf << 13 # muta cei trei biti cu 13 pozitii la stanga
    return (seq_nr, checksum, flags)


def create_header_receptor(ack_nr, checksum, window):
    
    octeti = struct.pack('!LHH',ack_nr,checksum,window)
    return octeti


def parse_header_receptor(octeti):

    ack_nr, checksum, window = struct.unpack('!LHH',octeti)
    return (ack_nr, checksum, window)


def citeste_segment(file_descriptor):


    yield file_descriptor.read(MAX_SEGMENT)


def exemplu_citire(cale_catre_fisier):
    with open(cale_catre_fisier, 'rb') as file_in:
        for segment in citeste_segment(file_in):
            print(segment)


def calc_checksum(packet):
    total = 0

    # Add up 16-bit words
    num_words = len(packet) // 2
    for chunk in struct.unpack("!%sH" % num_words, packet[0:num_words*2]):
        total += chunk

    # Add any left over byte
    if len(packet) % 2:
        total += ord(packet[-1]) << 8

    # Fold 32-bits into 16-bits
    total = (total >> 16) + (total & 0xffff)
    total += total >> 16
    return (~total + 0x10000 & 0xffff)


def verifica_checksum(octeti):
    if calc_checksum(octeti):
        return True
    return False



if __name__ == "__main__":
    compara_endianness(356)
    create_header_emitator(1,0)
    #print(verifica_checksum())