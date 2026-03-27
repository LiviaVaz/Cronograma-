import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

#1- Criação da Lista Vazia
#2- Ordenação dos dias da semana
#3- Criar uma função para inserir os dados {3.1, 3;2, 3.3, 3.4 e 3.5}
#4- Criar uma função para limpar a tabela e atualizar os dados
#5- Criar uma função para salvar o cronograma em um formato de texto {5.1 e 5.2}
#6- Design da interface 
#7-Estilização da Tabela
#8- Definição do título
#9- Container de Inputs
#10- Criação dos seletores {10.1, 10.2. 10.3. 10.4, 10.5 e 10.6}

#1- Criação da Lista Vazia
lista_estudos = []

#2- Ordenação dos dias da semana
ordem_semana = {"Segunda": 1, "Terça": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5, "Sábado": 6, "Domingo": 7} #Atribuindo valor de importância

#3- Criar uma função para inserir os dados
def adicionar_tarefa():
    materia = ent_materia.get().strip() #Variável matéria
    dia = var_dia.get()                 #Variável dia
    horario = var_horario.get()         #Variável horário
    
    #3.1- Validação para impedir o salvamento sem o devido preenchimento
    if dia == "--" or horario == "--":
        messagebox.showwarning("Inválido!", "Por favor, selecione um dia e um horário!")
        return
    
    #3.2- Validação para impedir o salvamento de campos vazios ou inválidos
    if not materia:
        messagebox.showwarning("Inválido!", "Digite o nome da disciplina!")
        return
    
    #3.3- Laço de repetição para impedir sobreposição de horário
    for tarefa in lista_estudos:
        if tarefa["dia"] == dia and tarefa["horario"] == horario:
            messagebox.showerror("Conflito", f"Já existe a matéria '{tarefa['materia']}' neste horário!")
            return

    #3.4- Alocação e organização dos dados
    lista_estudos.append({"dia": dia, "horario": horario, "materia": materia})
    lista_estudos.sort(key=lambda x: ordem_semana.get(x["dia"], 99)) #Ordenar pela ordem do número atribuído ao dia
    
    atualizar_tabela_visual()
    
    #3.5- Reset de Interface: limpa as caixas de texto e seletores para o próximo uso
    ent_materia.delete(0, tk.END)
    var_dia.set("--")
    var_horario.set("--")

#4- Criar uma função para limpar a tabela e atualizar os dados
def atualizar_tabela_visual():
    for i in tabela.get_children(): 
        tabela.delete(i)            #Limpa a tabela
    for item in lista_estudos:
        tabela.insert("", tk.END, values=(item["dia"], item["horario"], item["materia"])) #Redesenha a tabela 

#5- Criar uma função para salvar o cronograma em um formato de texto
def salvar_txt():
    if not lista_estudos: #Se não encontra informações preenchidas, retorna um erro
        messagebox.showwarning("Erro","O cronograma está vazio!")
        return
    
    #5.1- Abre uma janela para escolher local de armazenamento
    caminho_arquivo = filedialog.asksaveasfilename(
        initialfile="meu_cronograma.txt",
        defaultextension=".txt",
        filetypes=[("Arquivos de Texto", "*.txt")]
    )
    
    #5.2- Exportação do arquivo
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo: #"encoding="utf-8"" para também ler acentos 
                arquivo.write("Meu cronograma de estudos\n\n")
                for item in lista_estudos:
                    arquivo.write(f"[{item['dia']}] {item['horario']} - {item['materia']}\n") #Coloca os itens em uma coluna
            messagebox.showinfo("Sucesso!", "Cronograma salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro!", f"Não foi possível salvar: {e}")

#6- Design da interface 
app = tk.Tk()                       #Janela principal do programa
app.title("Cronograma PRO")         #Título da janela
app.geometry("500x650")             #Tamanho da janela
app.configure(bg="#F8F9FA")         #Cor cinza

#7-Estilização da Tabela
style = ttk.Style()                                                #Classe para personalizar widgets
style.theme_use("clam")                                            #Troca o tema padrão do Tkinter para o estilo clam
style.configure("Treeview", rowheight=25, font=("Segoe UI", 10))   #Ajuste de tabela e definição de fonte
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold")) #Deixa o cabeçalho em negrito

#8- Definição do título
tk.Label(app, text="Cronograma de estudos", font=("Segoe UI", 16, "bold"), 
         bg="#F8F9FA", fg="#333").pack(pady=20)

#9- Container de Inputs
frame_inputs = tk.Frame(app, bg="#F8F9FA") #Cria uma subjanela
frame_inputs.pack(pady=10, padx=20)        #MCor de fundo igual a da interface

#10- Criação dos seletores 
#10.1- Disciplina
tk.Label(frame_inputs, text="Disciplina:", bg="#F8F9FA", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
ent_materia = tk.Entry(frame_inputs, font=("Segoe UI", 11), width=25, relief="flat", highlightthickness=1)
ent_materia.grid(row=0, column=1, pady=10, padx=10)

#10.2- Dia da Semana
dias_lista = ["--"] + list(ordem_semana.keys())
var_dia = tk.StringVar(app, value="--")
tk.Label(frame_inputs, text="Dia:", bg="#F8F9FA", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w") #Sistema de linhas e colunas e alinhamento do texto à esquerda (w)
opt_dia = tk.OptionMenu(frame_inputs, var_dia, *dias_lista) #*dias = opção clicável
opt_dia.config(bg="white", relief="flat")                   #Características do estilo do seletor
opt_dia.grid(row=1, column=1, sticky="ew", padx=10)         #Definição da posição e centralização

#10.3- Horário
horarios_lista = ["--", "08h-09h", "09h-10h", "10h-11h", "11h-12h", "14h-15h", "15h-16h", "16h-17h"]
var_horario = tk.StringVar(app, value="--")
tk.Label(frame_inputs, text="Hora:", bg="#F8F9FA", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w")
opt_horario = tk.OptionMenu(frame_inputs, var_horario, *horarios_lista)
opt_horario.config(bg="white", relief="flat")
opt_horario.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

#10.4- Botão Adicionar
btn_add = tk.Button(app, text="Adicionar à tabela", command=adicionar_tarefa, 
                    bg="#2ECC71", fg="white", font=("Segoe UI", 10, "bold"), 
                    relief="flat", pady=8, cursor="hand2")
btn_add.pack(pady=15, fill="x", padx=60)

#10.5- Tabela
colunas = ("dia", "horario", "disciplina")
tabela = ttk.Treeview(app, columns=colunas, show="headings", height=8) #Exibe apenas minhas colunas
tabela.heading("dia", text="Dia")
tabela.heading("horario", text="Horário")
tabela.heading("disciplina", text="Disciplina")
tabela.column("dia", width=100, anchor="center")
tabela.column("horario", width=100, anchor="center")
tabela.column("disciplina", width=200, anchor="w")
tabela.pack(pady=10, padx=20, fill="both")

#10.6- Botão Salvar (em formato .txt)
btn_save = tk.Button(app, text="Salvar cronograma (.txt)", command=salvar_txt, 
                     bg="#3498DB", fg="white", font=("Segoe UI", 10, "bold"), 
                     relief="flat", pady=10, cursor="hand2")
btn_save.pack(pady=20, fill="x", padx=60)

app.mainloop()