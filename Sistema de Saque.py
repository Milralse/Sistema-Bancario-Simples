from datetime import datetime

usuarios = []
contas = []
LIMITE_OPERACOES = 10
LIMITE_VALOR_SAQUE = 500


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
    contas.append({
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": [],
        "operacoes": 0
    })

    print(f"✅ Conta criada com sucesso! Agência: 0001 | Conta: {numero_conta}")


def depositar(conta):
    if conta["operacoes"] >= LIMITE_OPERACOES:
        print("❌ Limite de 10 operações atingido.")
        return

    valor = float(input("Valor do depósito: "))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"].append(f"{datetime.now()} - Depósito: R$ {valor:.2f}")
        conta["operacoes"] += 1
        print("✅ Depósito realizado.")
    else:
        print("❌ Valor inválido.")


def sacar(conta):
    if conta["operacoes"] >= LIMITE_OPERACOES:
        print("❌ Limite de 10 operações atingido.")
        return

    valor = float(input("Valor do saque: "))

    if valor <= 0:
        print("❌ Valor inválido.")
    elif valor > conta["saldo"]:
        print("❌ Saldo insuficiente.")
    elif valor > LIMITE_VALOR_SAQUE:
        print(f"❌ Saque máximo por operação é R$ {LIMITE_VALOR_SAQUE:.2f}")
    else:
        conta["saldo"] -= valor
        conta["extrato"].append(f"{datetime.now()} - Saque: R$ {valor:.2f}")
        conta["operacoes"] += 1
        print("✅ Saque realizado.")


def exibir_extrato(conta):
    print("\n========== EXTRATO ==========")
    if not conta["extrato"]:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in conta["extrato"]:
            print(operacao)
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print(f"Operações realizadas: {conta['operacoes']}/10")
    print("=============================\n")


def selecionar_conta():
    cpf = input("Informe o CPF do titular: ")
    contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]

    if not contas_usuario:
        print("❌ Nenhuma conta encontrada para esse CPF.")
        return None

    for i, conta in enumerate(contas_usuario, 1):
        print(f"[{i}] Agência: {conta['agencia']} | Conta: {conta['numero_conta']}")

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
                    depositar(conta)
                elif opcao_conta == "2":
                    sacar(conta)
                elif opcao_conta == "3":
                    exibir_extrato(conta)
                elif opcao_conta == "4":
                    break
                else:
                    print("❌ Opção inválida.")

    elif opcao == "4":
        print("✅ Obrigado por usar o sistema bancário! Até logo.")
        break

    else:
        print("❌ Opção inválida.")
