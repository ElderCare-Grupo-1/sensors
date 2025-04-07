from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, nome, localizacao=None):
        self.nome = nome
        self.localizacao = localizacao
        self.ativo = False if localizacao else True  # Sensores sem localização ficam sempre ativos

    @abstractmethod
    def ler_dados(self):
        pass

    def ativar(self):
        self.ativo = True
        print(f"{self.nome} ativado!")

    def desativar(self):
        if self.localizacao:  # Só pode desativar sensores com localização
            self.ativo = False