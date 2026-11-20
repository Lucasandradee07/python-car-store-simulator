import json
import os
import shutil
from datetime import datetime

usuarios = {
    "admin": {
        "senha": "123",
        "cargo": "gerente"
    },
    "pedro": {
        "senha": "456",
        "cargo": "vendedor"
    }
}

def realizar_login():
    limpar_tela()
    while True:
        print("\n---SISTEMA DE LOGIN---")
        usuario = input("Usuário: ").strip().lower()
        senha = input("Senha: ").strip()
        if usuario in usuarios:
            if usuarios[usuario]["senha"] == senha:
                usuario_cargo = usuarios[usuario]["cargo"]
                print(f"\n Login realizado com sucesso! Bem-vindo, {usuario.capitalize()}")
                input("\n Pressione enter para continuar.")
                return usuario_cargo
            else:
                print("\n Senha inválida! Tente novamente.")
        else:
            print("\n Usuário não encontrado! Tente novamente.")
        input("Pressione enter para tentar novamente...")

arquivo_json = "estoque.json"

def registrar_log(mensagem):
    horario_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("estoque.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{horario_atual}] {mensagem}\n")

def fazer_backup():
    try:
        shutil.copy("estoque.json", "estoque_backup.json")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"ocorreu um erro ao gerar backup de segurança: {e}")

try:
    with open("estoque.json", "r", encoding="utf-8") as arquivo:
        dados_carregados = json.load(arquivo)
except FileNotFoundError:
    dados_carregados = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else "clear")

def salvar_dados():
    with open("estoque.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_carregados, arquivo, indent=4, ensure_ascii=False)

def cadastrar_veículos(cargo_atual):
    limpar_tela()
    print("\n--- CADASTRO DE VEÍCULO ---")
    nome = input("digite o nome no novo veículo: ").strip().upper()
    marca = input("digite o nome da marca do novo veículo: ").strip().upper()
    while True:
        try:
            preco = float(input("digite o preço do novo veículo: ").replace(",", "."))
            if preco < 0:
                print("o valor não pode ser negativo.")
                continue
            break
        except ValueError:
            print("digite apenas números e utilize pontos como vírgulas.")
    while True:
        try:
            estoque = int(input("digite o estoque do novo veículo: "))
            if estoque < 0:
                print("o estoque não pode ser negativo.")
                continue
            break
        except ValueError:
            print("utilize apenas números inteiros.")
            
    novo_veículo = {"marca": marca, "nome": nome, "preco": preco, "estoque": estoque}
    dados_carregados.append(novo_veículo)
    fazer_backup()
    salvar_dados()
    registrar_log(f"Úsuario {cargo_atual} cadastrou o veículo {novo_veículo}")
    print("novo veículo cadastrado com sucesso.")
    input("\n Pressione enter para voltar ao menu inícial...")

def alterar_precos(cargo_atual):
    limpar_tela()
    print("\n--- ALTERACÃO DE PREÇOS ---")
    veiculo_preco = input("digite o nome do modelo procurado para a alteração: ").lower().strip()
    encontrou = False
    for carro in dados_carregados:
        if carro['nome'].lower() == veiculo_preco:
            encontrou = True
            while True:
                try:
                    novo_preco = float(input("digite o novo preço do veículo: ").replace(",", "."))
                    break
                except ValueError:
                    print("digite apenas números e use pontos para vírgulas. ex: 10.000")
            carro['preco'] = novo_preco
            break
            
    if not encontrou:
        print("nenhum veículo correspondente foi encontrado.")
    else:
        fazer_backup()
        salvar_dados()
        registrar_log(f"Úsuario {cargo_atual} alterou o preço do {veiculo_preco} para {novo_preco}")
        print("os preços foram atualizados com sucesso.")
    input("\n Pressione enter para voltar ao menu inícial...")

def acessar_estoque():
    limpar_tela()
    if not dados_carregados:
        print("\n--------------------------------------------------")
        print(f"\n{'MODELO':<40} | {'ESTOQUE':<8} | {'PREÇO':<12}")
        print("\n--------------------------------------------------")
        print("\n o estoque está vazio")
        input("\n Pressione enter para voltar ao menu inícial...")
        return
    
    print("\nCOMO DESEJA VIZUALIZAR O ESTOQUE?")
    print("\n1. por ordem alfabética (A-Z)")
    print("2. menor preço primeiro")
    print("3. maior preço primeiro")
    print("4. padrão (ordem de cadastro)")

    opcao_ordem = input("\nescolha uma opção: ").strip()
    lista_para_exibir = dados_carregados

    if opcao_ordem == "1":
        lista_para_exibir = sorted(dados_carregados, key=lambda carro: carro['nome'].lower())
    elif opcao_ordem == "2":
        lista_para_exibir = sorted(dados_carregados, key=lambda carro: carro['preco'])
    elif opcao_ordem == "3":
        lista_para_exibir = sorted(dados_carregados, key=lambda carro: carro['preco'], reverse=True)

    limpar_tela()
    print("\n--------------------------------------------------")
    print(f"\n{'MODELO':<40} | {'ESTOQUE':<8} | {'PREÇO':<12}")
    print("\n--------------------------------------------------")

    for carro in lista_para_exibir:
        nome = carro['nome']
        estoque = f"{carro['estoque']} un"
        preco = f"{carro['preco']:,.2f}"

        print(f"{nome:<40} | {estoque:<8} | {preco:<12}")
    input("\n Pressione enter para voltar ao menu inícial...")

def alterar_estoque(cargo_atual):
    limpar_tela()
    print("\n--- ALTERAÇÃO DE ESTOQUE ---")
    veiculo_estoque = input("digite o nome do veículo para realizar a alteração: ").lower().strip()
    encontrouu = False
    for carro in dados_carregados:
        if carro['nome'].lower() == veiculo_estoque:
            encontrouu = True
            while True:
                try:
                    novo_estoque = int(input("digite o novo estoque do veículo: "))
                    if novo_estoque < 0:
                        print("o valor não pode ser negativo.")
                        continue
                    break
                except ValueError:
                    print("digite apenas números inteiros. ex: 1 10 100")
            carro['estoque'] = novo_estoque
            break

    if not encontrouu:
        print("nenhum veículo correspondente foi encontrado.")
    else:
        fazer_backup()
        salvar_dados()
        registrar_log(f"Úsuario {cargo_atual} alterou o estoque de {veiculo_estoque} para {novo_estoque}")
        print("estoque atualizado com sucesso.")
    input("\n Pressione enter para voltar ao menu inícial...")

def calcular_estoque(cargo_atual):
    limpar_tela()
    total_estoque = 0
    for carro in dados_carregados:
        total_lote = carro['preco'] * carro['estoque']
        total_estoque += total_lote
        print(f"{carro['nome']} | Total em estoque: {total_lote:,.2f}")
    print("-" * 50)
    print(f"VALOR TOTAL DO ESTOQUE: {total_estoque:,.2f}")
    print("-" * 50)
    input("\n Pressione enter para voltar ao menu inícial...")

def pesquisar_veiculo():
    limpar_tela()
    veiculo_pesquisa = input("digite o nome do veículo que você procura: ").lower().strip()
    encontrou = False
    for carro in dados_carregados:
        if veiculo_pesquisa in carro['nome'].lower():
            if not encontrou:
                print("\n-------------------------------------------------")
                print("\n Veículo Encontrado:")
                print(f"\n{'MODELO':<40} | {'ESTOQUE':<8} | {'PREÇO':<12}")
                print("\n-------------------------------------------------")
                encontrou = True
            
            nome = carro['nome']
            estoque = f"{carro['estoque']} un"
            preco = f"{carro['preco']:,.2f}"

            print(f"{nome:<40} | {estoque:<8} | {preco:<12}")

    if encontrou:
        input("\n Pressione enter para voltar ao menu inícial...")
    else:
        print("\n Nenhum veículo correspondente foi encontrado.")
        input("\n Pressione enter para voltar ao menu inícial...")

def filtrar_por_preco():
    limpar_tela()
    print("\n ---FILTRAR POR PREÇO---")
    try:
        valor_maximo = float(input("Digite o valor máximo do veículo para a exibição: "))
        encontrados = []
        for carro in dados_carregados:
            if carro['preco'] <= valor_maximo:
                encontrados.append(carro)
        if not encontrados:
            print(f"\n Não foi encontrado nenhum veículo até o valor de {valor_maximo:,.2f}")
            input("\n Pressione enter para voltar ao menu inícial...") 
        else:
            print(f"\n {len(encontrados)} veículos foram encontrados até a faixa de {valor_maximo:,.2f}")
            print("-" * 50)
            for carro in encontrados:
                print(f"modelo: {carro['nome']} | estoque: {carro['estoque']} un | preço: {carro['preco']:,.2f}")
                print("-" * 50)
            input("\n Pressione enter para voltar ao menu inícial.") 
    except ValueError:
        print("Digite apenas números e utilize pontos como vírgulas (ex:50.000).")

def alterar_nomes(cargo_atual):
    limpar_tela()
    print("\n ---ALTERAÇÃO DE NOMES--- ")
    veiculo_nome = input("Digite o nome do veículo para realizar a alteração: ").lower().strip()
    encontrou = False
    for carro in dados_carregados:
        if carro['nome'].lower() == veiculo_nome:
            novo_nome = input("Digite o novo nome do veículo: ").strip().upper()
            carro['nome'] = novo_nome
            encontrou = True
            break
            
    if not encontrou:
        print("\n Veículo não encontrado.")
    else:
        fazer_backup()
        salvar_dados()
        registrar_log(f"Úsuario {cargo_atual} mudou o nome de {veiculo_nome} para {novo_nome}")
        print("Os nomes foram alterados com sucesso.")
    input("\n Pressione enter para voltar ao menu inícial.")

def deletar_carro(cargo_atual):
    limpar_tela()
    print("\n---REMOVER VEÍCULO DO ESTOQUE---")
    if not dados_carregados:
        print("O estoque está vazio. Não há veículos para deletar.")
        input("\n Pressione enter para voltar ao menu inícial...")
        return
    
    veiculo_deletar = input("Digite o nome do veículo para DELETAR: ").lower().strip()
    carro_encontrado = None

    for carro in dados_carregados:
        if carro['nome'].lower() == veiculo_deletar:
            carro_encontrado = carro
            break
    
    if carro_encontrado is None:
        print(f"\n O veículo {veiculo_deletar} não foi encontrado no estoque.")
        input("\n Pressione enter para voltar ao menu inícial...")
        return
    
    limpar_tela()
    print("\n VEÍCULO ENCONTRADO!:")
    print(f"\n modelo: {carro_encontrado['nome']}")
    print(f"\n estoque: {carro_encontrado['estoque']} un")
    print(f"\n preço: {carro_encontrado['preco']:,.2f}")
    print("-" * 40)

    confirmacao = input("\n Tem certeza que deseja DELETAR o veículo? (S/N): ").strip().upper()

    if confirmacao == "S":
        dados_carregados.remove(carro_encontrado)
        salvar_dados()
        print("\n O veículo foi deletado com sucesso.")
    else:
        print("\n Operação cancelada. O veículo permanece no estoque.")
    input("\n Pressione enter para voltar ao menu inícial...")

def relatorio_por_marca():
    limpar_tela()
    print("\n ---QUANTIDADE DE VEÍCULOS POR MARCA---")
    if not dados_carregados:
        print("\n O estoque está vazio. Não há marcas para fazer o relatório.")
        input("\n Pressione enter para voltar ao menu inícial...")
        return
    
    contagem_marca = {}

    for carro in dados_carregados:
        marca = carro.get('marca', 'Não Informado').strip().upper()
        estoque = carro.get('estoque',1)

        if marca in contagem_marca:
            contagem_marca[marca] += estoque
        else:
            contagem_marca[marca] = estoque

    print(f"\n{'MARCA':<25} | {'TOTAL DE VEÍCULOS':<15}")
    print("-" * 40)
    total_geral = 0
    for marca,total in contagem_marca.items():
        print(f"{marca:<25} | {total:<15}")
        total_geral += total
     
    print(f"\n{'TOTAL NO ESTOQUE':<25} | {total_geral:<15}")
    print("-" * 40)
    input("\n Pressione enter para voltar ao menu inícial...")

if __name__ == "__main__":
 
 cargo_atual = realizar_login()

 while True:
    limpar_tela()
    print("\n --- MENU PRINCIPAL --")
    print("1. pesquisar veículos")
    print("2. acessar estoque de veículos")
    print("3. filtrar veículos por preço")
    print("4. relatório por marca")
    print("\n --- OPÇÕES DO GERENTE ---")
    print("5. acessar valor total em estoque")
    print("6. cadastrar veículos")
    print("7. alterar preços de veículos")
    print("8. alterar estoque de veículos")
    print("9. alterar nomes de veículos")
    print("10. deletar veículos")
    print("11. sair")
    opcao = input("escolha uma opção: ")
    
    if opcao == "1":
        pesquisar_veiculo()   
    elif opcao == "2":
        acessar_estoque()
    elif opcao == "3":
        filtrar_por_preco()
    elif opcao == "4":
        relatorio_por_marca()
    elif opcao == "5":
        if cargo_atual == "gerente":
            calcular_estoque(cargo_atual)
        else:
            print("\n Acesso negado! Esta área só pode ser acessada por gerentes.")
            input("\n Pressione enter para voltar ao menu inícial...")
    elif opcao == "6":
        if cargo_atual == "gerente":
            cadastrar_veículos(cargo_atual)
        else:
            print("\n Acesso negado! Veículos só pode ser cadastrados por gerentes.")  
            input("\n Pressione enter para voltar ao menu inícial...")      
    elif opcao == "7":
        if cargo_atual == "gerente":
            alterar_precos(cargo_atual)
        else:
            print("\n Acesso negado! Apenas gerentes podem alterar o preço de veículos.")
            input("\n Pressione enter para voltar ao menu inícial...") 
    elif opcao == "8":
        if cargo_atual == "gerente":
            alterar_estoque(cargo_atual)
        else:
            print("\n Acesso negado! Apenas gerentes podem alterar o estoque de veículos.")
            input("\n Pressione enter para voltar ao menu inícial...") 
    elif opcao == "9":
        if cargo_atual == "gerente":
            alterar_nomes(cargo_atual)
        else:
            print("\n Acesso negado! Apenas gerentes podem alterar nomes de veículos.")
            input("\n Pressione enter para voltar ao menu inícial...") 
    elif opcao == "10":
        if cargo_atual == "gerente":
            deletar_carro(cargo_atual)
        else:
            print("\n Acesso negado! Apenas gerentes podem deletar carro do sistema.")
            input("\n Pressione enter para voltar ao menu inícial...")
    elif opcao == "11":
        print("Saindo do sistema...até logo!")
        break
    else:
        print("opção inválida.")
