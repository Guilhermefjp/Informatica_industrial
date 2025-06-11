from conta import Conta, ContaPoupanca

class Banco():

    #__contas = []               # lista privada (declaracao)
    def __init__(self):

        self.contas = []
        self.contas.append(Conta( 1, "Guilherme", "1234", 200))       # append adiciona item a lista
