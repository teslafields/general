#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import time
import RPi.GPIO as GPIO
import MFRC522
 
# UID dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '4F:FD:2F:0:9D': 'FilipeFlop',
    '3C:2F:4F:0:2D': 'Teste',
}
 
try:
    # Inicia o módulo RC522.
    LeitorRFID = MFRC522.MFRC522()
 
    print('Aproxime seu carto RFID')
 
    while True:
        # Verifica se existe uma tag próxima do módulo.
        status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
 
        if status == LeitorRFID.MI_OK:
            print('Carto detectado!')
 
            # Efetua leitura do UID do cartão.
            status, uid = LeitorRFID.MFRC522_Anticoll()
 
            if status == LeitorRFID.MI_OK:
                uid = ':'.join(['%X' % x for x in uid])
                print('UID do carto: %s' % uid)
 
                # Se o cartão está liberado exibe mensagem de boas vindas.
                if uid in CARTOES_LIBERADOS:
                    print('Acesso Liberado!')
                    print('Ol %s.' % CARTOES_LIBERADOS[uid])
                else:
                    print('Acesso Negado!')
 
                print('\nAproxime seu carto RFID')
 
        time.sleep(.25)
except KeyboardInterrupt:
    # Se o usuário precionar Ctrl + C
    # encerra o programa.
    GPIO.cleanup()
    print('\nPrograma encerrado.')
