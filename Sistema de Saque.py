from abc import ABC, abstractmethod
from datetime import datetime

usuarios = []
contas = []
LIMITE_OPERACOES = 10
LIMITE_VALOR_SAQUE = 500


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transacoes.append(f"{data_hora} - {descricao}")

    def listar(self):
        if not self.transacoes:
            print("Nenhuma transação registrada.")
        else:
            print("\n===== EXTRATO =====")
            for transacao in self.transacoes:
                print(transacao)
            print("===================\n")


class Conta(ABC):
    def __init__(self, agencia, numero, usuario):
        self.agencia = agencia
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0
        self.historico = Historico()
        self.operacoes = 0

    @abstractmethod
    def sacar(self, valor):
        pass

    def depositar(self, valor):
        if self.operacoes >= LIMITE_OPERACOES:
            print("❌ Limite de operações atingido.")
            return

        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
            self.operacoes += 1
            print("✅ Depósito realizado.")
        else:
            print("❌ Valor inválido.")

    def extrato(self):
        print(f"Conta: {self.numero} | Agência: {self.agencia}")
        self.historico.listar()
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print(f"Operações realizadas: {self.operacoes}/{LIMITE_OPERACOES}")


class ContaCorrente(Conta):
    def sacar(self, valor):
        if self.operacoes >= LIMITE_OPERACOES:
            print("❌ Limite de operações atingido.")
            return

        if valor <= 0:
            print("❌ Valor inválido.")
        elif valor > self.saldo:
            print("❌ Saldo insuficiente.")
        elif valor > LIMITE_VALOR_SAQUE:
            print(f"❌ Limite máximo por saque é R$ {LIMITE_VALOR_SAQUE:.2f}")
        else:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            self.operacoes += 1
            print("✅ Saque realizado.")


def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    if buscar_usuario(cpf):
        print("❌ Usuário já cadastrado.")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nasc": data_nasc,
        "endereco": endereco
    })

    print("✅ Usuário criado com sucesso!")


def buscar_usuario(cpf):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    usuario = buscar_usuario(cpf)

    if not usuario:
        print("❌ Usuário não encontrado. Deseja criar um novo usuário? (s/n)")
        if input().lower() == 's':
            criar_usuario()
            usuario = buscar_usuario(cpf)
        else:
            return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(agencia="0001", numero=numero_conta, usuario=usuario)
    contas.append(conta)

    print(f"✅ Conta criada com sucesso! Agência: 0001 | Conta: {numero_conta}")


def selecionar_conta():
    cpf = input("Informe o CPF do titular: ")
    contas_usuario = [conta for conta in contas if conta.usuario["cpf"] == cpf]

    if not contas_usuario:
        print("❌ Nenhuma conta encontrada para esse CPF.")
        return None

    for i, conta in enumerate(contas_usuario, 1):
        print(f"[{i}] Agência: {conta.agencia} | Conta: {conta.numero}")

    opcao = int(input("Selecione o número da conta: ")) - 1
    return contas_usuario[opcao] if 0 <= opcao < len(contas_usuario) else None


def menu_principal():
    menu = """
========== MENU PRINCIPAL ==========
[1] Criar usuário
[2] Criar conta bancária
[3] Acessar conta
[4] Sair
"""
    return input(menu)


def menu_conta():
    menu = """
--- MENU CONTA ---
[1] Depositar
[2] Sacar
[3] Extrato
[4] Voltar ao menu principal
"""
    return input(menu)


# Execução principal
while True:
    opcao = menu_principal()

    if opcao == "1":
        criar_usuario()

    elif opcao == "2":
        criar_conta()

    elif opcao == "3":
        conta = selecionar_conta()
        if conta:
            while True:
                opcao_conta = menu_conta()

                if opcao_conta == "1":
                    valor = float(input("Valor do depósito: "))
                    conta.depositar(valor)
                elif opcao_conta == "2":
                    valor = float(input("Valor do saque: "))
                    conta.sacar(valor)
                elif opcao_conta == "3":
                    conta.extrato()
                elif opcao_conta == "4":
                    break
                else:
                    print("❌ Opção inválida.")

    elif opcao == "4":
        print("✅ Obrigado por usar o sistema bancário! Até logo.")
        break

    else:
        print("❌ Opção inválida.")