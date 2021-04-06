# emitator Reliable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging
import sys
import random
from threading import Thread
import concurrent.futures
import queue
import traceback
logging.basicConfig(
    format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.NOTSET)

file_in = open('layers.jpg', 'rb')

def connect(sock, adresa_receptor):
    '''
    Functie care initializeaza conexiunea cu receptorul.
    Returneaza ack_nr de la receptor si window
    '''
    seq_nr = random.randint(0, 2**31)  
    flags = 'S'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(
        seq_nr, checksum, flags)
    checksum = calc_checksum(octeti_header_fara_checksum)
    
    octeti_header_cu_checksum = create_header_emitator(seq_nr, checksum, flags)
    mesaj = octeti_header_cu_checksum
    ack_nr=0
    print(seq_nr)
    while ack_nr!=seq_nr+1:
        sock.sendto(mesaj, adresa_receptor)
        try:
            data, server = sock.recvfrom(MAX_SEGMENT)
            print("Primit confirmare, updatez ack")
            ack_nr, checksum, window = parse_header_receptor(data)
            print(ack_nr)
        except socket.timeout as e:
            print("N-am primit confirmarea,mai trimit odt")
    #if verifica_checksum(data) is False:
    #    return -1, -1
    logging.info('Ack Nr: "%d"', ack_nr)
    logging.info('Checksum: "%d"', checksum)
    logging.info('Window: "%d"', window)

    return ack_nr, window
    


def finalize(sock, adresa_receptor, seq_nr):
    '''
    Functie care finalizeaza conexiunea cu receptorul.
    Returneaza ack_nr de la receptor si window
    '''
    flags = 'F'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(
        seq_nr, checksum, flags)
    mesaj = octeti_header_fara_checksum
    checksum = calc_checksum(mesaj)
    
    octeti_header_cu_checksum = create_header_emitator(seq_nr, checksum, flags)
    mesaj = octeti_header_cu_checksum
    ack_nr=0
    while ack_nr!=seq_nr+1:
        sock.sendto(mesaj, adresa_receptor)
        print("Sequence number:",seq_nr)
        print("Incerc sa trimit.")
        try:
            print("Astept confirmarea ca a primit receptorul")
            data, server = sock.recvfrom(MAX_SEGMENT)
            print("Primit confirmare, updatez ack")
            ack_nr, checksum, window = parse_header_receptor(data)
            print(ack_nr)
            break
        except socket.timeout as e:
            print("N-am primit confirmarea,mai trimit odt")
    print("FINALIZAT VIATZA")
    #if verifica_checksum(data) is False:
    #    return -1, -1
    logging.info('Ack Nr: "%d"', ack_nr)
    logging.info('Checksum: "%d"', checksum)
    logging.info('Window: "%d"', window)

    return ack_nr, window

def listen(sock,q):
    data=0
    while not data:
        try:
            data,server=sock.recvfrom(MAX_SEGMENT)
            header = data[:8]
            ack_nr, checksum, window = parse_header_receptor(header)
            q.put((ack_nr,window))
        except socket.timeout as e:
            print(e,"Trying again.")
    
def send(sock, adresa_receptor, seq_nr, window, octeti_payload):
    '''
    Functie care initializeaza conexiunea cu receptorul.
    Returneaza ack_nr de la receptor si window
    '''
    flags = 'P'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(
        seq_nr, checksum, flags)
    mesaj = octeti_header_fara_checksum + octeti_payload
    #checksum = calc_checksum(mesaj)
    seq_nr_curent=seq_nr+len(octeti_payload)
    checksum=calc_checksum(mesaj)
    octeti_header_cu_checksum = create_header_emitator(seq_nr, checksum, flags)
    mesaj = octeti_header_cu_checksum + octeti_payload
    ack_nr=seq_nr_curent
    sock.sendto(mesaj, adresa_receptor)

    #if verifica_checksum(data) is False:
    #    return -1, -1
    '''
    logging.info('Ack Nr: "%d"', ack_nr)
    logging.info('Checksum: "%d"', checksum)
    logging.info('Window: "%d"', window)
    '''

    return ack_nr, window
def main():
    parser = ArgumentParser(usage=__file__ + ' '
                            '-a/--adresa IP '
                            '-p/--port PORT'
                            '-f/--fisier FILE_PATH',
                            description='Reliable UDP Emitter')

    parser.add_argument(
        '-a',
        '--adresa',
        dest='adresa',
        default='198.8.0.2',
        help=
        'Adresa IP a receptorului (IP-ul containerului, localhost sau altceva)'
    )

    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care asculta receptorul pentru mesaje')

    parser.add_argument('-f',
                        '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul care urmeaza a fi trimis')

    # Parse arguments
    args = vars(parser.parse_args())

    ip_receptor = '198.8.0.2'
    port_receptor = 10000
    fisier = "layers.jpg"

    adresa_receptor = (ip_receptor, port_receptor)
    print(adresa_receptor)
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM,
                         proto=socket.IPPROTO_UDP)
    # setam timeout pe socket in cazul in care recvfrom nu primeste nimic in 3 secunde
    sock.settimeout(20)
    window=0
    try:
        ack_nr, window = connect(sock, adresa_receptor)
        print("Am termint connectu")
        ## TODO: send trebuie sa trimită o fereastră de window segmente
        # până primșete confirmarea primirii tuturor segmentelor
        lista_teoretic=[]
        sequencuri=[]
        lista_segmente_ack=[]
        segmente=[]
        q=queue.Queue()
        segment=1
        print("Window initial:",window)
        ack_nr_initial=ack_nr

        ack=0
        window_real=window
        while (segment):
            while (len(lista_segmente_ack)<window_real and segment):
                #print("Window mai mare decat cate am, mai citesc segmente. Window=",window_real,"Lungime segmente:",len(lista_segmente_ack))
                segment = next(citeste_segment(file_in))
                if lista_segmente_ack:
                    ack_teoretic=lista_segmente_ack[-1][1]+len(segment)
                else:
                    ack_teoretic=ack_nr_initial+len(segment)
                lista_segmente_ack.append((segment,ack_teoretic))
            for i in range (len(lista_segmente_ack)):
                ack_nr,window=send(sock,adresa_receptor,lista_segmente_ack[i][1],window,lista_segmente_ack[i][0])
            while (ack!=lista_segmente_ack[0][1]):
                print("N-am primit confirmare real, astept iar pentru",lista_segmente_ack[0][1])
                t=Thread(target=listen,args=(sock,q))
                t.start()
                ack,window=q.get()
                print("Trimit iar atatea:",window_real)
                for i in range (len(lista_segmente_ack)):
                    ack_nr,window=send(sock,adresa_receptor,lista_segmente_ack[i][1],window,lista_segmente_ack[i][0])
            #print("Primit confirmare pt!!!!!!!!!",lista_segmente_ack[0][1])
            print("Lista cu ack")
            for e in lista_segmente_ack:
                print(e[1])
            window_real=window
            ack_nr_initial=ack_nr_initial+len(lista_segmente_ack[0][0])
            lista_segmente_ack.pop(0)
            print("Primit window nou:",window)
        print("Terminat segmente, trimit ce a mai ramas")
        '''
        while (lista_segmente_ack):
            for i in range (len(lista_segmente_ack)):
               ack_nr,window=send(sock,adresa_receptor,lista_segmente_ack[i][1],window,lista_segmente_ack[i][0])
            lista_segmente_ack.pop(0)   
        '''
        while (lista_segmente_ack):
            for i in range (len(lista_segmente_ack)):
               ack_nr,window=send(sock,adresa_receptor,lista_segmente_ack[i][1],window,lista_segmente_ack[i][0])
            while (ack!=lista_segmente_ack[0][1]):
                print("N-am primit confirmare real, astept iar pentru",lista_segmente_ack[0][1])
                t=Thread(target=listen,args=(sock,q))
                t.start()
                ack,window=q.get()
                print("Trimit iar cu fereastra de:",window)
                for i in range (len(lista_segmente_ack)):
                    ack_nr,window=send(sock,adresa_receptor,lista_segmente_ack[i][1],window,lista_segmente_ack[i][0])
            lista_segmente_ack.pop(0)
        
        finalize(sock, adresa_receptor,ack_nr)
        file_in.close()
        
    except Exception as e:
        print("Socket timeout ", str(e))
        print(traceback.format_exc())
        sock.close()



if __name__ == '__main__':
    main()