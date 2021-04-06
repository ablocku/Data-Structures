# receptor Reiable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging
import scapy

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

def main():
    parser = ArgumentParser(usage=__file__ + ' '
                                             '-p/--port PORT'
                                             '-f/--fisier FILE_PATH',
                            description='Reliable UDP Receptor')

    parser.add_argument('-p', '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care sa porneasca receptorul pentru a primi mesaje')

    parser.add_argument('-f', '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul in care se vor scrie octetii primiti')

    # Parse arguments
    args = vars(parser.parse_args())
    #port = args['port']
    #fisier = args['fisier']
    port=10000
    #fisier="test"
    #f=open(fisier)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    adresa = '0.0.0.0'
    server_address = (adresa, port)
    sock.bind(server_address)
    logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)
    emitator=('172.8.0.2',10000)
    sock.settimeout(10)
    mesaj_nou=0
    data=0
    contor_data=0
    fisier=open("verificare.jpg",'wb')
    sequencer=[]
    spf=0
    while True and not (spf & 0b001):
        logging.info('Asteptam mesaje...')
        while not data:
            try:
                data, address = sock.recvfrom(MAX_SEGMENT+8)
                print(address)
            except socket.timeout as e:
                print("N am primit nimic,incerc iar")
        header = data[:8]
        #TODO: pentru fiecare mesaj primit
        #1. verificam checksum
        #if verifica_checksum(header): TODO
        seq_nr, checksum, spf_zero = struct.unpack('!LHH', header)
        
        spf = spf_zero >> 13
        if spf & 0b100 or spf & 0b001:
                    # inseamna ca am primit S sau F
                ack_nr = seq_nr + 1
        elif spf & 0b010:
                        # inseamna ca am primit P
                ack_nr = seq_nr
        window = random.randint(1, 5)
        octeti = struct.pack('!LHH', ack_nr, checksum, window)
        seq_nr_nou=seq_nr

        print("SEQUENCE NUMBER ESTE:,",seq_nr)
        if (seq_nr not in sequencer):
            if (sequencer):
                if (seq_nr>=sequencer[-1]):
                    with open("verificare.jpg",'ab') as f:
                        f.write(data[8:])
                        sequencer.append(seq_nr)
            else:
                with open("verificare.jpg",'ab') as f:
                    f.write(data[8:])
                sequencer.append(seq_nr)
        while seq_nr_nou==seq_nr:
            sock.sendto(octeti,address)
            try:
                data,address=sock.recvfrom(MAX_SEGMENT+8)
                header=data[:8]
                seq_nr_nou, checksum, spf_zero = struct.unpack('!LHH', header)
                print(seq_nr_nou)
                spf=spf_zero>>13
                if (spf & 0b001):
                    break
            except:
                print("Nu putem mesaje noi pt ca n am primit confirmare")
    fisier.close()

            
        


        #4. scriem intr-un fisier octetii primiti
        #5. verificam la sfarsit ca fisierul este la fel cu cel trimis de emitator clearly not dar will be
        


if __name__ == '__main__':
    main()