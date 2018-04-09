#-*- encoding:utf-8 -*-
class Pote:
    """
    This class models a money reserve
    Um pote pode ficar negativo?
    """
    def get_pote(self, nome, maximo, prioridade=1, saldo=0.0, moeda='R$'):
        self.nome = nome
        self.saldo = saldo
        self.maximo = maximo
        self.moeda = moeda
        self.prioridade = prioridade
        return self

    def __str__(self):
        # '{0} \n limite \n {moeda}{limite:0.2f} \n saldo \n {moeda}{saldo:0.2f} \n ({porc})'.format(self.nome, limite=self.maximo, moeda=self.moeda, saldo=self.get_saldo(), porc=self.get_porcentagem() )
        return '{nome:<20} {moeda}{limite:8.2f}     {moeda}{saldo:8.2f}       {porc:6}'.format(nome=self.nome, limite=self.maximo, moeda=self.moeda, saldo=self.get_saldo(), porc=self.get_porcentagem() )

    def get_heading(self):
        return '{nome:<20} {limite:<8}       {saldo:<8}       {porc:<6}'.format(nome='NOME', limite='LIMITE', saldo='SALDO', porc='PORCENTAGEM' )

    def get_porcentagem(self):
        return '{perc:0.1f}%'.format(perc = self.saldo / self.maximo * 100)

    def deposita(self, valor):
        r"""
        Deposita o valor passado e retorna uma tupla
		com o valor extornado e o saldo.

		Cria pote
		>>> p = Pote().get_pote('conta de luz', 200.5)

		Deposita valor menor que o máximo
		>>> p.deposita(100)
		(0.0, 100.0)

		Deposita valor maior que o máximo
		>>> p.deposita(200)
		(99.5, 200.5)
		
        """

        saldo = self.saldo
        maximo = self.maximo
        extorno = 0.0
        deposito_maximo = (maximo-saldo)
		
        # Valor passado é menor que o depósito máximo
        if valor < deposito_maximo:
            self.saldo+=valor
		# Valor passado é maior que o depósito máximo
        else:
            extorno = valor - deposito_maximo
            self.saldo+=valor-extorno
			
        return (extorno, self.saldo)

    def retira(self, valor): 
        r"""
        Retira o valor passado e retorna o saldo.
        Se o valor passado é maior do que o saldo, 
        retira o saldo.
		Retorna uma tupla com o valor sacado e o saldo.

        Cria pote
        >>> p = Pote().get_pote('conta de luz',200.5)

        Enche o pote
        >>> p.deposita(p.maximo)
        (0.0, 200.5)

        Retira valor menor que o saldo
        >>> p.retira(100)
        (100, 100.5)

        Retira valor maior que o saldo
        >>> p.retira(200.5)
        (100.5, 0.0)
    	"""

        saldo = self.saldo
        if valor<saldo:
            self.saldo -= valor
        else:
            valor = saldo
            self.saldo = 0.0
        
        return (valor ,self.saldo)

    def get_saldo(self):
        """
        Mostra estado da conta

        Cria pote
        >>> p=Pote().get_pote('conta de luz',200.5)

        Enche o pote
        >>> p.deposita(p.maximo)
        (0.0, 200.5)

        Representação em string do pote
		>>> print(p)
		conta de luz tem limite de R$200.50 e saldo de R$200.50 (100.0%)

        >>> p.get_saldo()
        200.5
        """
        return self.saldo

