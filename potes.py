#-*- encoding:utf-8 -*-

from pote import Pote

class Potes:

    def __init__(self, ano, mes):
        """
        Conjunto de potes para um ano e mês específicos.
        """
        self.potes = []
        self.ano = ano
        self.mes = mes

    def __str__(self):
        return '{0} potes, totalizando R$ {total:0.2f} de saldo'.format(len(self.potes), total=self.get_total())

    def cria_potes(self, potes_spec):
        """
        Cria os potes conforme especificação informada (Nome, Limite, Prioridade)
        e retorna-os em uma lista.
        """
        
        for p in sorted(potes_spec, key=lambda x: x[2]):
            self.potes.append(Pote().get_pote(*p))
        return self.potes

    def add_potes(self, potes):
        self.potes.append(potes)
        return len(potes)

    def get_potes(self):
        return self.potes

    def distribue_salario(self, salario, potes):
        """
        Distribue salário nos potes por ordem de prioridade.
        """
        for pote in potes:
            if salario > pote.maximo:
                pote.deposita(pote.maximo) 
                salario-=pote.maximo  
            else:
                pote.deposita(salario)
                salario = 0

    def get_total(self):
        return sum([pote.get_saldo() for pote in self.potes])
    
    def show_all(self):
        print(self.potes[0].get_heading())
        for pote in self.potes:
            print (pote)
      


contas_rogerio = Potes(2018,4)

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
            ]

contas_rogerio.cria_potes(potes_spec_list)

salario = 6000

contas_rogerio.distribue_salario(salario, contas_rogerio.get_potes())

contas_rogerio.show_all()
print(contas_rogerio)
