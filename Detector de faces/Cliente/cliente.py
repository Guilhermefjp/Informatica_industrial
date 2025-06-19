import socket
import cv2
import os
import numpy as np

class Cliente():
    """
    Classe Cliente - API Socket
    """
    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente
        """
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def start(self):
        """
        Método que inicializa a execução do Cliente
        """
        endpoint = (self.__server_ip,self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    def __method(self):
        """
        Método que envia a imagem
        """
        try:
            while True:
                caminho_imagem = 'faces/image_0001.jpg'
                img = cv2.imread(caminho_imagem)   
                _, img_bytes = cv2.imencode('.jpg', img) 
                img_bytes = bytes(img_bytes)
                tamanho_da_imagem_codificado = len(img_bytes).to_bytes(4, 'big')      

                self.__tcp.send(tamanho_da_imagem_codificado)     
                self.__tcp.sendall(img_bytes)

                tam_codf = self.__tcp.recv(1024)
                tam = int.from_bytes(tam_codf, 'big')

                img_proc_bytes = b''
                for i in range(tam//1024):
                    img_proc_bytes += self.__tcp.recv(1024)
                if (tam % 1024) > 0:
                     img_proc_bytes += self.__tcp.recv(tam%1024)
                
                img = cv2.imdecode(np.frombuffer(img_proc_bytes, np.uint8), cv2.IMREAD_COLOR)

                cv2.imshow('Imagem Processada', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)
