#!/usr/bin/env python
import requests
import xml.etree.ElementTree as ET
import numpy as np
import socket

class Menu:
    def __init__(self):
        self.self_ip = '192.168.100.142'

        self.menu = '''
        1. Marcar a terminal
        2. Salir
        '''
        self.opciones = {
            '1': self.call,
            '2': self.salir
        }

    def mostrar_menu(self):
        print(self.menu)

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input('Elija una opción: ')
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print('{0} no es una opción válida'.format(opcion))

    def call(self):

        # Pedir número de terminal
        terminal = input('Introduzca la IP de la terminal: ')

        # Crear paquete SIP
        sip = '''INVITE sip:''' + terminal+  ''' SIP/2.0
Via: SIP/2.0/UDP ''' +self.self_ip+ ''':5060;rport;branch=z9hG4bKPjiNeUsXjdMuRBU2j.KGSI94O1i7pQoYqc
Max-Forwards: 70
From: sip:''' +self.self_ip+ ''';tag=PKcMBzp6yhIZQG-du1TsYkW1MPmX6L5V
To: sip:''' + terminal + '''
Contact: <sip:''' +self.self_ip+ ''':5060>
Call-ID: 2mdIf8lexOTBIMg2pPgKOBdDB3SowCcf
CSeq: 124 INVITE
Allow: INVITE, ACK, BYE, CANCEL, UPDATE
Supported: 
Content-Type: application/sdp
Content-Length: 219

v=0
o=pjsip-siprtp 3878938575 3878938575 IN IP4 videoportero
s=pjsip
c=IN IP4 ''' + self.self_ip + '''
t=0 0
m=video 5000 RTP/AVP 0 96
a=rtpmap:0 PCMU/8000
a=sendrecv
a=rtpmap:121 telephone-event/8000
a=fmtp:121 0-15
'''

        print('Llamando a terminal')
        # Enviar packete SIP a la terminal
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(sip.encode(), (terminal, 5060))
        print('Paquete SIP enviado')
        
    
    def salir(self):
        print('Saliendo del programa')
        exit()


def main():
    """ # Escuchar el puerto de SIP (5060)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('192.168.100.119', 5060))
    while True:
        data, addr = sock.recvfrom(1024)
        print(data) """

    #Mostrar menú
    menu = Menu()
    menu.ejecutar()
        
    #Realizar petición POST a una URL y obtener el resultado
    url = 'http://192.168.100.232/Media2'
    data = '''
    <soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:tr2="http://www.onvif.org/ver20/media/wsdl"
    xmlns:tt="http://www.onvif.org/ver10/schema">
    <soap:Header>
        <wsse:Security
            soap:mustUnderstand="true"
            xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken
                wsu:Id="UsernameToken-35"
                xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Username>
                    admin
                    </wsse:Username>
                <wsse:Password
                    Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">
                    123456
                </wsse:Password>
                <wsu:Created>
                    2022-11-22T23:08:05Z
                    </wsu:Created>
                </wsse:UsernameToken>
            </wsse:Security>
        </soap:Header>
    <soap:Body>
    <tr2:GetStreamUri>
        <tr2:Protocol>RTSP</tr2:Protocol>
        <tr2:ProfileToken>SubStream</tr2:ProfileToken>
        </tr2:GetStreamUri>
    </soap:Body>
</soap:Envelope>
    '''
    
    headers = {
        'Host': '192.168.100.232',
        'Content-type': 'application/soap+xml; charset="utf-8"',
        'Conection': 'keep-alive',
        'User-Agent': 'HTTP_USER_AGENT',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'gb2312,utf8;q=0.7,*;q=0.7'
    }
    r = requests.post(url, data=data, headers=headers)
    root = ET.fromstring(r.text)
    
    # Obtener el índice de root cuando atributo es igual a 'Body'
    for i in range(len(root)):
        if root[i].tag == '{http://www.w3.org/2003/05/soap-envelope}Body':
            index = i
            break

    root = root[index]
    for child in root:
        for subchild in child:
            #print(subchild.tag, subchild.text)
            if subchild.tag.split('}')[1] == 'Uri':
                uri = subchild.text
                print(uri)
                # Realizar streaming de video RTSP con OpenCV y la URI obtenida
                
    #print(root)

if __name__ == '__main__':
    main()