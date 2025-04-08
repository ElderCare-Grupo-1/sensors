from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, nome, localizacao=None):
        self.nome = nome
        self.localizacao = localizacao
        self.ativo = False if localizacao else True

    @abstractmethod
    def ler_dados(self, quantidade=1):
        pass

    def ativar(self):
        self.ativo = True
        return True

    def desativar(self):
        if self.localizacao:
            self.ativo = False
        return True