# trabalhopid

import tkinter as tk
from tkinter import font, filedialog
from PIL import Image, ImageTk

janela = tk.Tk()
janela.title("Processador de Imagens")
janela.geometry("600x550")
janela.configure(bg="#2E4053")

#customizar botao
fonte_botoes = font.Font(family="Helvetica", size=10, weight="bold")

frame_esquerda = tk.Frame(janela, bg="#2E4053")
frame_esquerda.pack(side='left', fill='y', padx=15, pady=15)

frame_direita = tk.Frame(janela, bg="#2E4053")
frame_direita.pack(side='right', fill='y', padx=15, pady=15, anchor='ne')

#variavel global
imagem_tk = None
imagem_original = None  

#exibir imagem esquerda
imagem_label = tk.Label(frame_esquerda, bg="#2E4053")
imagem_label.pack(pady=10)

#funções
def carregar_imagem():
    global imagem_tk, imagem_original

    caminho = filedialog.askopenfilename(
        filetypes=[("Arquivos de Imagem", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )

    if caminho:
        imagem_original = Image.open(caminho).convert("RGB")  # garante formato RGB
        imagem_redimensionada = imagem_original.resize((400, 400))
        imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
        imagem_label.config(image=imagem_tk)

def voltar_imagem_original():
    global imagem_tk, imagem_original

    if imagem_original is None:
        print("Nenhuma imagem carregada!")
        return

    imagem_redimensionada = imagem_original.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)
    print("Imagem original restaurada.")

def escala_de_cinza():
    global imagem_tk, imagem_original

    if imagem_original is None:
        print("Nenhuma imagem carregada!")
        return

    imagem_cinza = Image.new("RGB", imagem_original.size)
    for x in range(imagem_original.width):
        for y in range(imagem_original.height):
            r, g, b = imagem_original.getpixel((x, y))
            cinza = int(0.299 * r + 0.587 * g + 0.114 * b)
            imagem_cinza.putpixel((x, y), (cinza, cinza, cinza))

    imagem_redimensionada = imagem_cinza.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)
    print("Imagem convertida para escala de cinza (manual).")

def limiarizacao():
    print("Função: Limiarização (Threshold)")

def passa_alta_basico():
    print("Função: Passa-Alta Básico")

def passa_alta_reforco():
    print("Função: Passa-Alta com Reforço")

def passa_baixa_media():
    print("Função: Passa-Baixa Média")

def passa_baixa_mediana():
    print("Função: Passa-Baixa Mediana")

def operador_roberts():
    print("Função: Operador de Roberts")

def operador_prewitt():
    print("Função: Operador de Prewitt")

def operador_sobel():
    print("Função: Operador de Sobel")

def transformacao_logaritmica():
    print("Função: Transformação Logarítmica")

def operacoes_aritmeticas():
    print("Função: Operações Aritméticas (Soma, Subtração, Multiplicação, Divisão)")

def mostrar_histograma():
    print("Função: Mostrar Histograma (Escala de Cinza)")

def equalizar_histograma():
    print("Função: Equalização de Histograma")

#estilizar botões
def criar_botao(frame, texto, comando):
    return tk.Button(
        frame,
        text=texto,
        width=25,
        command=comando,
        bg="#34495E",
        fg="white",
        font=fonte_botoes,
        relief="raised",
        borderwidth=3,
        activebackground="#5D6D7E",
        activeforeground="white",
        cursor="hand2",
        pady=5
    )

#botao carregar imagem
criar_botao(frame_esquerda, "Carregar Imagem", carregar_imagem).pack(pady=10)
criar_botao(frame_esquerda, "Voltar à Imagem Original", voltar_imagem_original).pack(pady=5)

#botoes
criar_botao(frame_direita, "Escala de Cinza", escala_de_cinza).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Limiarização", limiarizacao).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Passa-Alta Básico", passa_alta_basico).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Passa-Alta com Reforço", passa_alta_reforco).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Passa-Baixa Média", passa_baixa_media).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Passa-Baixa Mediana", passa_baixa_mediana).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Operador de Roberts", operador_roberts).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Operador de Prewitt", operador_prewitt).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Operador de Sobel", operador_sobel).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Transformação Logarítmica", transformacao_logaritmica).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Operações Aritméticas", operacoes_aritmeticas).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Histograma (Escala de Cinza)", mostrar_histograma).pack(anchor='e', pady=3)
criar_botao(frame_direita, "Equalização de Histograma", equalizar_histograma).pack(anchor='e', pady=3)

janela.mainloop()
