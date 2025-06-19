import socket
import cv2
import os
import numpy as np

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
            """
            Método que inicializa a execução do servidor
            """
            endpoint = (self._host, self._port)
            try:
                self.__tcp.bind(endpoint)
                self.__tcp.listen(1)
                print("Servidor iniciado em ", self._host, ": ", self._port)
                while True:
                    con, client = self.__tcp.accept()
                    self._service(con, client)
            except Exception as e:
                print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, cliente):
        """
        Método que recebe a imagem e junta os fragmentos
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        while True:
            try:
                tamanho_da_imagem_codificado = con.recv(1024)
                tam = int.from_bytes(tamanho_da_imagem_codificado, 'big')
                img_bytes_total = b''
                for i in range(tam//1024):
                    img_bytes_total += con.recv(1024)
                if (tam % 1024) > 0:
                     img_bytes_total += con.recv(tam%1024)
                
                img = cv2.imdecode(np.frombuffer(img_bytes_total, np.uint8), cv2.IMREAD_COLOR)

                img_process = self.process(img)

                _, img_process = cv2.imencode('.jpg', img_process) 
                img_process = bytes(img_process)
                tamanho_da_imagem_codificado = len(img_process).to_bytes(4, 'big') 
                con.send(tamanho_da_imagem_codificado)
                con.sendall(img_process)
                
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                        cliente, ": ", e.args)
                con.send(bytes("Erro", 'ascii'))
                return            

    def process(self, img):
        """
        Método que processa a imagem
        :param img: imagem completa
        """
        xml_classificador = os.path.join(os.path.relpath(
            cv2.__file__).replace('__init__.py', ''), 'data\haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(
            xml_classificador)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return img

        
