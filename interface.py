import tkinter as tk
from tkinter import messagebox
from sistema import dados_carregados, usuarios, registrar_log, fazer_backup, salvar_dados

def tentar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        messagebox.showinfo("Sucesso!", "Login realizado com sucesso!")
        botao_carregar.config(state=tk.NORMAL)
        botao_cadastrar.config(state=tk.NORMAL)
        botao_alterar_preco.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Erro!", "Usuário ou senha incorretos!")
        registrar_log(f"Falha de autenticação para o usuário: {usuario}.")
        campo_senha.delete(0, tk.END)

def exibir_estoque():
    caixa_texto.delete("1.0", tk.END)
    caixa_texto.insert(tk.END, "==ESTOQUE DE VEÍCULOS ATUAL==\n\n")

    if not dados_carregados:
        caixa_texto.insert(tk.END, "Nenhum veículo foi encontrado.\n")
        return

    for index, carro in enumerate(dados_carregados, start=1):
        if isinstance(carro, dict):
            texto_carro = f"{index:02d}. {carro['nome']} | Preço: {carro['preco']:,.2f} | Qtd: {carro['estoque']}\n"
        else:
            texto_carro = f"{index:02d}. {carro}\n"
        caixa_texto.insert(tk.END, texto_carro)

    registrar_log(f"Estoque exibido com sucesso ({len(dados_carregados)} veículos).")

def fechar_sistema():
    salvar_dados()
    fazer_backup()
    registrar_log("Sistema encerrado e backup automático realizado com sucesso!")
    janela.destroy()

def adicionar_veiculos():
    nome = campo_nome.get().strip().upper()
    marca = campo_marca.get().strip().upper()

    if not nome or not marca:
        messagebox.showerror("Erro de validação!", "Preencha todos os campos para continuar!")
        return

    try:
        texto_preco = campo_preco.get().strip().replace(",", ".")
        preco = float(texto_preco)
        if preco < 0:
            messagebox.showerror("Erro de validação!", "O preço não pode ser negativo!")
            return
    except ValueError:
        messagebox.showerror("Erro de validação!", "No campo de preço, digite apenas números!")
        return

    try:
        estoque = int(campo_estoque.get().strip())
        if estoque < 0:
            messagebox.showerror("Erro de validação!", "O estoque não pode ser negativo!")
            return
    except ValueError:
        messagebox.showerror("Erro de validação!", "No campo de estoque, digite apenas números inteiros.")
        return

    novo_veiculo = {"marca": marca, "nome": nome, "preco": preco, "estoque": estoque}
    dados_carregados.append(novo_veiculo)
    
    salvar_dados()
    fazer_backup()
    registrar_log(f"Veículo cadastrado: {novo_veiculo}")

    messagebox.showinfo("Sucesso!", "Novo veículo cadastrado com sucesso!")

    campo_nome.delete(0, tk.END)
    campo_marca.delete(0, tk.END)
    campo_preco.delete(0, tk.END)
    campo_estoque.delete(0, tk.END)

    exibir_estoque()

def alterar_precos():
    termo_busca = campo_veiculo.get().strip()
    entrada_preco = campo_novo_preco.get().strip()

    if not termo_busca or not entrada_preco:
        messagebox.showwarning("Aviso", "Preencha o veículo (nome ou índice) e o novo preço!")
        return

    try:
        novo_preco = float(entrada_preco.replace(",", "."))
        if novo_preco < 0:
            messagebox.showerror("Erro de validação!", "O preço deve ser um valor positivo!")
            return
    except ValueError:
        messagebox.showerror("Erro de validação!", "No campo do preço, digite apenas números!")
        return

    carro_encontrado = None

    if termo_busca.isdigit():
        index = int(termo_busca) - 1
        if 0 <= index < len(dados_carregados):
            carro_encontrado = dados_carregados[index]

    if not carro_encontrado:
        termo_lower = termo_busca.lower()
        for carro in dados_carregados:
            if isinstance(carro, dict):
                if termo_lower in carro['nome'].lower():
                    carro_encontrado = carro
                    break

    if carro_encontrado and isinstance(carro_encontrado, dict):
        preco_antigo = carro_encontrado['preco']
        carro_encontrado['preco'] = novo_preco
        salvar_dados()
        exibir_estoque()
        campo_veiculo.delete(0, tk.END)
        campo_novo_preco.delete(0, tk.END)
        msg_sucesso = f"Preço do {carro_encontrado['nome']} alterado de {preco_antigo:,.2f} para {novo_preco:,.2f}"
        registrar_log(msg_sucesso)
        messagebox.showinfo("Sucesso", msg_sucesso)
    else:
        messagebox.showerror("Erro!", f"Nenhum veículo foi encontrado com o termo: '{termo_busca}'")

janela = tk.Tk()
janela.title("SISTEMA DE ESTOQUE - LOJA DE CARROS")
janela.geometry("700x680")
janela.minsize(700, 680)
janela.protocol("WM_DELETE_WINDOW", fechar_sistema)

titulo = tk.Label(
    janela,
    text="BEM-VINDO AO SISTEMA DE ESTOQUE!",
    font=("Arial", 18, "bold"),
    fg="#1e88e5"
)
titulo.pack(pady=15)

frame_login = tk.LabelFrame(
    janela,
    text="Autenticação",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=10,
)
frame_login.pack(pady=5)

lbl_usuario = tk.Label(frame_login, text="Usuário:", font=("Arial", 10))
lbl_usuario.grid(row=0, column=0, sticky="e", padx=5, pady=5)
campo_usuario = tk.Entry(frame_login, font=("Arial", 10), width=25)
campo_usuario.grid(row=0, column=1, sticky="e", padx=5, pady=5)

lbl_senha = tk.Label(frame_login, text="Senha:", font=("Arial", 10))
lbl_senha.grid(row=1, column=0, sticky="e", padx=5, pady=5)
campo_senha = tk.Entry(frame_login, font=("Arial", 10), width=25, show="*")
campo_senha.grid(row=1, column=1, sticky="e", padx=5, pady=5)

botao_login = tk.Button(
    frame_login,
    text="Entrar",
    font=("Arial", 10, "bold"),
    bg="#4caf50",
    fg="white",
    command=tentar_login
)
botao_login.grid(row=2, column=0, columnspan=2, pady=5)

frame_texto = tk.Frame(janela)
frame_texto.pack(pady=5)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

caixa_texto = tk.Text(
    frame_texto,
    width=70,
    height=10,
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set
)
caixa_texto.pack(side=tk.LEFT)
scrollbar.config(command=caixa_texto.yview)

botao_carregar = tk.Button(
    janela,
    text="Carregar estoque de carros",
    font=("Arial", 11, "bold"),
    bg="#1e88e5",
    fg="white",
    state=tk.DISABLED,
    command=exibir_estoque
)
botao_carregar.pack(pady=10, ipady=3, ipadx=10)

frame_cadastro = tk.LabelFrame(
    janela,
    text="Cadastrar novo veículo",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=10
)
frame_cadastro.pack(pady=5)

tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
campo_nome = tk.Entry(frame_cadastro, width=30)
campo_nome.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_cadastro, text="Marca:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
campo_marca = tk.Entry(frame_cadastro, width=15)
campo_marca.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_cadastro, text="Preço:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
campo_preco = tk.Entry(frame_cadastro, width=30)
campo_preco.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_cadastro, text="Estoque:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
campo_estoque = tk.Entry(frame_cadastro, width=15)
campo_estoque.grid(row=1, column=3, padx=5, pady=2)

botao_cadastrar = tk.Button(
    frame_cadastro,
    text="Cadastrar veículo",
    bg="#4caf50",
    fg="white",
    font=("Arial", 9, "bold"),
    state=tk.DISABLED,
    command=adicionar_veiculos
)
botao_cadastrar.grid(row=2, column=0, columnspan=4, pady=8)

frame_preco = tk.LabelFrame(
    janela,
    text="Alterar preço de veículo",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=10
)
frame_preco.pack(pady=5)

tk.Label(frame_preco, text="Veículo (Nome ou Nº):").grid(row=0, column=0, sticky="e", padx=5, pady=2)
campo_veiculo = tk.Entry(frame_preco, width=25)
campo_veiculo.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_preco, text="Novo Preço:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
campo_novo_preco = tk.Entry(frame_preco, width=15)
campo_novo_preco.grid(row=0, column=3, padx=5, pady=2)

botao_alterar_preco = tk.Button(
    frame_preco,
    text="Atualizar Preço",
    bg="#ff9800",
    fg="white",
    font=("Arial", 9, "bold"),
    state=tk.DISABLED,
    command=alterar_precos
)
botao_alterar_preco.grid(row=1, column=0, columnspan=4, pady=8)

janela.mainloop()