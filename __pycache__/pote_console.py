#-*- encoding:utf-8 -*-

class Pote:
    """
    This class models a money reserve.
    """

    def __init__(self, nome = 'Sem Nome', limite = 100.0, prioridade=1):
        self.cria_pote(nome = nome, limite = limite, prioridade = prioridade)

    def cria_pote(self, nome = 'Sem Nome', limite = 100.0, prioridade=1, saldo=0.0, moeda='R$'):
        self._nome = nome
        self._saldo = saldo
        self._limite = limite
        self._moeda = moeda
        self._prioridade = prioridade
        return self

    def mostra(self): # Somente para console
        print(self.cabecalho())
        print(str(self))

    def __str__(self):
        return '{0} {nome:20} {moeda}{limite:8.2f}     {moeda}{saldo:8.2f}       {porc:6}'.format(self.prioridade(), nome=self.nome(), limite=self.limite(), moeda=self.moeda(), saldo=self.saldo(), porc=self.porcentagem() )

    def status(self): # Somente para console
        return '{nome} tem limite de {moeda}{limite:.2f} e saldo de {moeda}{saldo:.2f} ({porc:6})'.format(nome=self.nome(), limite=self.limite(), moeda=self.moeda(), saldo=self.saldo(), porc=self.porcentagem() )

    def nome(self): # Somente para console
        return self._nome

    def prioridade(self): # Somente para console
        return self._prioridade

    def moeda(self): # Somente para console  
        return self._moeda

    def limite(self): # Somente para console
        return self._limite

    def saldo(self): # Somente para console
        """
        Mostra saldo da conta.

        Cria pote
        >>> p=Pote().cria_pote('conta de luz',200.5)

        Enche o pote
        >>> p.deposita(p.limite())
        (0.0, 200.5)

        Representação em string do pote
	>>> print(p.status())
	conta de luz tem limite de R$200.50 e saldo de R$200.50 (100.0%)

        >>> p.saldo()
        200.5
        """
        return self._saldo


    def cabecalho(self): # Somente para console
        return '  {nome:20} {limite:14} {saldo:16} {porc:6}'.format(nome='NOME', limite='LIMITE', saldo='SALDO', porc='PORCENTAGEM' )

    def porcentagem(self): 
        return '{perc:0.1f}%'.format(perc = self.saldo() / self.limite() * 100)

    def deposita(self, valor): # rest action
        """
        Deposita o valor passado e retorna uma tupla
		com o valor extornado e o saldo.

		Cria pote
		>>> p = Pote().cria_pote('conta de luz', 200.5)

		Deposita valor menor que o máximo
		>>> p.deposita(100)
		(0.0, 100.0)

		Deposita valor maior que o máximo
		>>> p.deposita(200)
		(99.5, 200.5)
		
        """

        saldo = self.saldo()
        limite = self.limite()
        extorno = 0.0
        deposito_maximo = (limite-saldo)
		
        # Valor passado é menor que o depósito máximo
        if valor < deposito_maximo:
            self._saldo+=valor
		# Valor passado é maior que o depósito máximo
        else:
            extorno = valor - deposito_maximo
            self._saldo+=valor-extorno
			
        return (extorno, self.saldo())

    def retira(self, valor): # rest action
        """
        Retira o valor passado e retorna o saldo.
        Se o valor passado é maior do que o saldo, 
        retira o saldo.
	Retorna uma tupla com o valor sacado e o saldo.

        Cria pote
        >>> p = Pote().cria_pote('conta de luz',200.5)

        Enche o pote
        >>> p.deposita(p.limite())
        (0.0, 200.5)

        Retira valor menor que o saldo
        >>> p.retira(100)
        (100, 100.5)

        Retira valor maior que o saldo
        >>> p.retira(200.5)
        (100.5, 0.0)
    	"""

        saldo = self.saldo()
        if valor<saldo:
            self._saldo -= valor
        else:
            valor = saldo
            self._saldo = 0.0
        
        return (valor ,self.saldo())
    
    def transfere_para(self, pote, valor): # rest action
        """
        Transfere um valor para outro pote, passando pote e valor
        como parâmetros.Retorna uma tupla com o valor transferido
        e o saldo do pote de origem.

        Cria potes
        >>> p1 = Pote().cria_pote('conta de luz',200.0)
        >>> p2 = Pote().cria_pote('conta de agua',100.0)
        
        Enche o pote1
        >>> p1.deposita(p1.limite())
        (0.0, 200.0)

        Transfere valor menor que o saldo
        >>> p1.transfere_para(p2, 50.0)
        (50.0, 150.0)
        
        >>> p1.saldo()
        150.0
        >>> p2.saldo()
        50.0

        Retira valor maior que o saldo
        >>> p1.transfere_para(p2, 200.0)
        (50.0, 100.0)

        >>> p1.saldo()
        100.0
        
        >>> p2.saldo()
        100.0
        """
        retirado = self.retira(valor)
        valor_retirado = retirado[0]
        saldo = retirado[1]
        depositado = pote.deposita(valor_retirado)
        extorno = depositado[0]
        self._saldo += extorno
        return (valor_retirado - extorno, self.saldo())


        

