import tkinter as tk
from tkinter import font, filedialog, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageChops  # adicionei ImageChops aqui
import numpy as np
import cv2
from scipy.signal import convolve2d

janela = tk.Tk()
janela.title("Processador de Imagens")
janela.geometry("600x550")
janela.configure(bg="#2E4053")

# customizar botao
fonte_botoes = font.Font(family="Helvetica", size=10, weight="bold")

frame_esquerda = tk.Frame(janela, bg="#2E4053")
frame_esquerda.pack(side='left', fill='y', padx=15, pady=15)

frame_direita = tk.Frame(janela, bg="#2E4053")
frame_direita.pack(side='right', fill='y', padx=15, pady=15, anchor='ne')

# variavel global
imagem_tk = None
imagem_original = None  
imagem_processada = None

# exibir imagem esquerda
imagem_label = tk.Label(frame_esquerda, bg="#2E4053")
imagem_label.pack(pady=10)

# funcoes
def carregar_imagem():
    global imagem_tk, imagem_original, imagem_processada

    caminho = filedialog.askopenfilename(
        filetypes=[("arquivos de imagem", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )

    if caminho:
        imagem_original = Image.open(caminho).convert("RGB")  # garante formato RGB
        imagem_processada = imagem_original.copy()
        imagem_redimensionada = imagem_processada.resize((400, 400))
        imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
        imagem_label.config(image=imagem_tk)

def atualizar_imagem():
    global imagem_tk, imagem_processada
    if imagem_processada:
        imagem_redimensionada = imagem_processada.resize((400, 400))
        imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
        imagem_label.config(image=imagem_tk)

def voltar_imagem_original():
    global imagem_tk, imagem_processada, imagem_original

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    imagem_processada = imagem_original.copy()
    atualizar_imagem()
    print("imagem original restaurada.")

def escala_de_cinza():
    global imagem_processada

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # usando metodo mais eficiente do pillow
    imagem_processada = imagem_original.convert('L').convert('RGB')
    atualizar_imagem()
    print("imagem convertida para escala de cinza.")

def limiarizacao():
    global imagem_tk, imagem_original

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza)

    # definir um limiar fixo, por exemplo 128
    limiar = 128
    img_limiar = (img_array > limiar) * 255
    img_limiar = img_limiar.astype(np.uint8)

    # criar imagem pil a partir do array
    imagem_resultado = Image.fromarray(img_limiar)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)
    print("limiarização aplicada com threshold =", limiar)

def passa_alta_basico():
    global imagem_tk, imagem_original

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza, dtype=int)

    # máscara passa-alta básica (realce de bordas)
    kernel = np.array([[-1/9, -1/9, -1/9],
                       [-1/9, 8/9, -1/9],
                       [-1/9, -1/9, -1/9]])

    # aplicar convolução
    img_passa_alta = convolve2d(img_array, kernel, mode='same', boundary='symm')

    # normalizar para 0-255
    img_passa_alta = np.clip(img_passa_alta, 0, 255).astype(np.uint8)

    imagem_resultado = Image.fromarray(img_passa_alta)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)
    print("filtro passa-alta básico aplicado.")

def passa_alta_reforco():
    global imagem_tk, imagem_original

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza, dtype=int)

    # máscara passa-alta com reforço (sharpen)
    kernel = np.array([[0, -1/4, 0],
                       [-1/4, +2, -1/4],
                       [0, -1/4, 0]])

    img_passa_alta_reforco = convolve2d(img_array, kernel, mode='same', boundary='symm')

    # normalizar para 0-255
    img_passa_alta_reforco = np.clip(img_passa_alta_reforco, 0, 255).astype(np.uint8)

    imagem_resultado = Image.fromarray(img_passa_alta_reforco)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)
    print("filtro passa-alta com reforço aplicado.")

def passa_baixa_media():
    global imagem_processada

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    try:
        # pedir ao usuário o tamanho do kernel
        tamanho = simpledialog.askinteger("passa-baixa média", 
                                         "Digite o tamanho do kernel (3, 5, 7, etc.):",
                                         minvalue=3, maxvalue=15, initialvalue=3)
        if tamanho is None:  # usuário cancelou
            return
            
        # aplicar filtro de média
        imagem_processada = imagem_original.filter(ImageFilter.BoxBlur(tamanho//2))
        atualizar_imagem()
        print(f"filtro passa-baixa média aplicado (kernel {tamanho}x{tamanho})")
    except Exception as e:
        print(f"erro no passa-baixa média: {e}")

def passa_baixa_mediana():
    global imagem_processada

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    try:
        # pedir ao usuário o tamanho do kernel
        tamanho = simpledialog.askinteger("passa-baixa mediana", 
                                         "Digite o tamanho do kernel (3, 5, 7, etc.):",
                                         minvalue=3, maxvalue=15, initialvalue=3)
        if tamanho is None:  # usuário cancelou
            return
            
        # aplicar filtro de mediana
        imagem_processada = imagem_original.filter(ImageFilter.MedianFilter(tamanho))
        atualizar_imagem()
        print(f"filtro passa-baixa mediana aplicado (kernel {tamanho}x{tamanho})")
    except Exception as e:
        print(f"erro no passa-baixa mediana: {e}")

def operador_roberts():
    global imagem_tk, imagem_original, imagem_label

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza, dtype=int)

    # máscaras do operador de roberts
    kernel_x = np.array([[1, 0],
                         [0, -1]])
    kernel_y = np.array([[0, 1],
                         [-1, 0]])

    # aplicar convolução para detectar bordas
    gx = convolve2d(img_array, kernel_x, mode='same', boundary='symm')
    gy = convolve2d(img_array, kernel_y, mode='same', boundary='symm')

    # calcular magnitude do gradiente
    gradiente = np.sqrt(gx**2 + gy**2)

    # normalizar para 0-255 e converter para uint8
    gradiente = np.clip(gradiente, 0, 255).astype(np.uint8)

    # criar imagem pil a partir do array resultante
    imagem_resultado = Image.fromarray(gradiente)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)

    print("operador de roberts aplicado.")

def operador_prewitt():
    global imagem_tk, imagem_original, imagem_label

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza (se ainda não estiver)
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza, dtype=int)

    # máscaras do operador de prewitt
    kernel_x = np.array([[-1, 0, 1],
                         [-1, 0, 1],
                         [-1, -1, -1]])
    kernel_y = np.array([[1, 1, 1],
                         [0, 0, 0],
                         [-1, -1, -1]])

    # aplicar convolução para detectar bordas horizontais e verticais
    gx = convolve2d(img_array, kernel_x, mode='same', boundary='symm')
    gy = convolve2d(img_array, kernel_y, mode='same', boundary='symm')

    # calcular magnitude do gradiente
    gradiente = np.sqrt(gx**2 + gy**2)

    # normalizar para 0-255 e converter para uint8
    gradiente = np.clip(gradiente, 0, 255).astype(np.uint8)

    imagem_resultado = Image.fromarray(gradiente)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)

    print("operador de prewitt aplicado.")

def operador_sobel():
    global imagem_tk, imagem_original, imagem_label

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    # converter para escala de cinza
    imagem_cinza = imagem_original.convert("L")
    img_array = np.array(imagem_cinza, dtype=int)

    # máscaras do operador de sobel
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    kernel_y = np.array([[1, 2, 1],
                         [0, 0, 0],
                         [-1, -2, -1]])

    # aplicar convolução para detectar bordas horizontais e verticais
    gx = convolve2d(img_array, kernel_x, mode='same', boundary='symm')
    gy = convolve2d(img_array, kernel_y, mode='same', boundary='symm')

    # calcular magnitude do gradiente
    gradiente = np.sqrt(gx**2 + gy**2)

    # normalizar para 0-255 e converter para uint8
    gradiente = np.clip(gradiente, 0, 255).astype(np.uint8)

    imagem_resultado = Image.fromarray(gradiente)
    imagem_redimensionada = imagem_resultado.resize((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    imagem_label.config(image=imagem_tk)

    print("operador de sobel aplicado.")

def transformacao_logaritmica():
    global imagem_processada

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    try:
        # converter para escala de cinza
        img_cinza = imagem_original.convert('L')
        img_array = np.array(img_cinza, dtype=np.float32)

        # aplicar transformação logarítmica
        c = 255 / np.log(1 + np.max(img_array))
        img_log = c * np.log(1 + img_array)

        # normalizar e converter para imagem
        img_log = np.clip(img_log, 0, 255).astype(np.uint8)
        imagem_processada = Image.fromarray(img_log).convert('RGB')

        atualizar_imagem()
        print("transformação logarítmica aplicada.")
    except Exception as e:
        print(f"erro na transformação logarítmica: {e}")

def operacoes_aritmeticas():
    global imagem_processada, imagem_original

    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return

    try:
        operacao = simpledialog.askstring("operações aritméticas", 
                                          "Digite a operação (soma, subtracao, multiplicacao, divisao):")
        if operacao is None:
            return

        valor = simpledialog.askfloat("valor", "Digite o valor (ex: 50 para soma):")
        if valor is None:
            return

        img_array = np.array(imagem_original.convert("L"), dtype=np.float32)

        if operacao == "soma":
            resultado = img_array + valor
        elif operacao == "subtracao":
            resultado = img_array - valor
        elif operacao == "multiplicacao":
            resultado = img_array * valor
        elif operacao == "divisao":
            resultado = img_array / (valor if valor != 0 else 1)
        else:
            print("operação inválida.")
            return

        resultado = np.clip(resultado, 0, 255).astype(np.uint8)
        imagem_processada = Image.fromarray(resultado).convert("RGB")
        atualizar_imagem()
        print(f"operação aritmética '{operacao}' aplicada com valor {valor}.")

    except Exception as e:
        print(f"erro nas operações aritméticas: {e}")

def mostrar_histograma():
    global imagem_processada
    
    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return
    
    try:
        # converter para escala de cinza
        img_cinza = imagem_original.convert('L')
        img_array = np.array(img_cinza)
        
        # calcular histograma
        hist = cv2.calcHist([img_array], [0], None, [256], [0, 256])
        
        # criar imagem do histograma
        hist_img = np.zeros((256, 256), dtype=np.uint8)
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist))
        
        for i in range(256):
            cv2.line(hist_img, (i, 255), (i, 255 - hist[i]), 255, 1)
        
        # mostrar histograma em uma nova janela
        hist_img = Image.fromarray(hist_img).convert('RGB')
        hist_img.show()
        print("histograma mostrado em nova janela.")
    except Exception as e:
        print(f"erro ao mostrar histograma: {e}")

def equalizar_histograma():
    global imagem_processada
    
    if imagem_original is None:
        print("nenhuma imagem carregada!")
        return
    
    try:
        # converter para escala de cinza
        img_cinza = imagem_original.convert('L')
        img_array = np.array(img_cinza)
        
        # equalizar histograma
        img_eq = cv2.equalizeHist(img_array)
        
        imagem_processada = Image.fromarray(img_eq).convert('RGB')
        atualizar_imagem()
        print("histograma equalizado.")
    except Exception as e:
        print(f"erro na equalização do histograma: {e}")

# estilizar botoes
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

# botao carregar imagem
criar_botao(frame_esquerda, "Carregar Imagem", carregar_imagem).pack(pady=10)
criar_botao(frame_esquerda, "Voltar à Imagem Original", voltar_imagem_original).pack(pady=5)

# botoes de operacoes
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
