menu = """
[1] Depósito
[2] Saque
[3] Extrato
[4] Sair

Qual opção deseja? 
"""

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Qual valor deseja depositar: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Quanto deseja sacar? "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saque >= LIMITE_SAQUE

        if excedeu_saldo:
            print("Não possui saldo suficiente.")
        elif excedeu_limite:
            print("Excedeu o limite de saque.")
        elif excedeu_saques:
            print("Excedeu a quantidade de saques.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque += 1
        else:
            print("Valor informado é inválido.")

    elif opcao == "3":
        print("\n========== EXTRATO ==========")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=============================\n")

    elif opcao == "4":
        print("Muito prazer em te atender. Volte sempre!")
        break

    else:
        print("Opção inválida.")