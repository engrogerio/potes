#-*- encoding:utf-8 -*-

from pote import Pote
import datetime

class Potes:

    def __init__(self, ano = datetime.datetime.now().year, mes = datetime.datetime.now().month):
        """
        Conjunto de potes para um ano e mês específicos.
        """
        self.potes = []
        self.ano = ano
        self.mes = mes
        # Cria um pote default 
        self.potes.append(Pote())

    def __str__(self):
        return '{0} {1}, totalizando R$ {total:0.2f} de saldo'.format(
            len(self.potes), 'potes' if len(self.potes)>1 else 'pote', total=self.total())

    def __len__(self):
        return len(self.potes)

    def cria_potes(self, potes_spec):
        """
        Cria os potes conforme especificação informada (Nome, Limite, Prioridade)
        e retorna-os em uma lista.
        """
        
        for p in sorted(potes_spec, key=lambda x: x[2]):
            self.potes.append(Pote().get_pote(*p))
        return self.potes

    def adiciona_potes(self, potes):
        self.potes.append(potes)
        return len(potes)

    def get_potes(self):
        return self.potes

    def distribue_valor(self, valor, potes):
        """
        Distribue salário nos potes por ordem de prioridade.
        Potes = lista de potes
        """
        for pote in potes:
            if valor > pote.maximo:
                pote.deposita(pote.maximo) 
                valor-=pote.maximo  
            else:
                pote.deposita(valor)
                valor = 0

    def total(self):
        return sum([pote.get_saldo() for pote in self.potes])
    
    def status(self):
        print(self.potes[0].get_heading())
        for pote in self.potes:
            print (pote)
        print(self)

    def amostra(self):
        contas_amostra = Potes(2018,4)

        potes_spec_list=[('luz',200, 1),
            ('Faculdade Fa',600, 4),
            ('aluguel',2200, 7),
            ('academia',90, 8),
            ('agua',50, 2),
            ('telefone',150, 3),
            ('supermercado',800, 5),
            ('TV',100, 6),
            ('Faculdade Gu',3800, 9),
            ('restaurante',800, 10),
            ('carro',1500, 11),
            ('IPTU',500, 12),
            ('Gasto',2000,13),
            ('Poupanca', 9999.99, 99)
            ]

        contas_amostra.cria_potes(potes_spec_list)
        salario = 16000
        contas_amostra.distribue_valor(salario, contas_amostra.get_potes())
        contas_amostra.status()
        return contas_amostra

ps=Potes()
p1=Pote('Natação', 200,5)
p2=Pote('Faculdade', 1500,1)
contas_amostra = ps.amostra()
contas_amostra.adiciona_potes([p1,p2])
contas_amostra.amostra()