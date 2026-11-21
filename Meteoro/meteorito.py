import tkinter as tk
import os
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw

LIMIAR_LUZ = 400
LUZ_INVERTIDA = False
TEMP_MIN, TEMP_MAX = 0, 50
TOLERANCIA_FUNDO = 80

VINHO = "#85001A"

TEMAS = {
    "claro":  {"fundo": "#81A1EA", "cor_hora": "#4040C8", "cor_texto": "#2A4A7A"},
    "escuro": {"fundo": "#2F4B6E", "cor_hora": "#2A4A6A", "cor_texto": "#2A4A6A"},
}

dados = {"temp": 25.0, "umid": 50, "luz": 700}
estado = {"conectado": True}

PASTA = os.path.dirname(os.path.abspath(__file__))
imagens = {}


def atualizar_dados(temp, umid, luz):
    dados["temp"] = temp
    dados["umid"] = umid
    dados["luz"] = luz


def conectar():
    pass


def interromper_conexao():
    pass

# ------------------------------botoes--------------------------------------
def atualizar_botao():
    if estado["conectado"]:
        botao.config(text="Interromper conexão",
                     bg="#C0392B", activebackground="#922B21")
    else:
        botao.config(text="Conectar",
                     bg="#27AE60", activebackground="#1E8449")


def definir_conectado(valor):
    estado["conectado"] = valor
    atualizar_botao()


def alternar_conexao():
    if estado["conectado"]:
        interromper_conexao()
        definir_conectado(False)
    else:
        conectar()
        definir_conectado(True)

#--------------------------------------imagens----------------------------------------

def remover_fundo(img, tolerancia=TOLERANCIA_FUNDO):
    img = img.convert("RGBA")
    w, h = img.size
    for canto in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if img.getpixel(canto)[3] == 255:
            ImageDraw.floodfill(img, canto, (0, 0, 0, 0), thresh=tolerancia)
    return img


def carregar_imagem(nome, tamanho):
    caminho = os.path.join(PASTA, nome)
    img = remover_fundo(Image.open(caminho))
    img = img.resize(tamanho, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def carregar_imagens():
    imagens["sol"] = carregar_imagem("sol.jpeg", (130, 130))
    imagens["lua"] = carregar_imagem("lua.jpeg", (130, 130))

#-----------------------------------------------------------------------

def retangulo_arredondado(cv, x1, y1, x2, y2, r=20, **kw):
    pontos = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
              x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
              x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    return cv.create_polygon(pontos, smooth=True, **kw)


def caixa_texto(y, texto, cor):
    retangulo_arredondado(canvas, 50, y, 550, y + 70, r=20,
                          fill="white", outline="white")
    canvas.create_text(75, y + 35, text=texto, anchor="w", width=450,
                       font=("Comic Sans MS", 14), fill=cor)

#----------------------------------------termometro da Mari--------------------------------
def termometro(y, temp):
    x1, x2 = 85, 395
    altura = 60
    cy = y + altura / 2

    canvas.create_rectangle(x1, y, x2, y + altura, fill="#81A1EA",
                            outline="white", width=4)

    frac = (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)
    frac = max(0, min(1, frac))
    canvas.create_rectangle(x2 - (x2 - x1) * frac, y + 3, x2, y + altura - 3,
                            fill=VINHO, outline=VINHO)

    for i in range(1, 5):
        mx = x2 - 70 * i
        canvas.create_line(mx, y + altura - 22, mx, y + altura, fill="white", width=3)

    canvas.create_oval(x2 - 15, cy - 65, x2 + 115, cy + 65, fill=VINHO,
                       outline="white", width=4)
    canvas.create_text(x2 + 50, cy, text=f"{temp:.1f}°C",
                       font=("Comic Sans MS", 20, "bold"), fill="white")
#---------------------------------------------------------------------------------

def desenhar():
    canvas.delete("all")

    claro = dados["luz"] >= LIMIAR_LUZ
    if LUZ_INVERTIDA:
        claro = not claro
    tema = TEMAS["claro" if claro else "escuro"]
    canvas.configure(bg=tema["fundo"])

    retangulo_arredondado(canvas, 160, 40, 560, 150, r=40,
                          fill="white", outline="white")
    hora = datetime.now().strftime("%H:%M:%S")
    canvas.create_text(360, 95, text=hora,
                       font=("Comic Sans MS", 40), fill=tema["cor_hora"])

    astro = imagens["sol" if claro else "lua"]
    canvas.create_image(20, 20, image=astro, anchor="nw")

    if claro:
        txt_luz = "Alta luminosidade -> dia claro / tempo ensolarado"
    else:
        txt_luz = "Baixa luminosidade -> escuro (noite ou tempo nublado)"

    cor = tema["cor_texto"]
    caixa_texto(240, txt_luz, cor)
    caixa_texto(340, f"Umidade do ar em {dados['umid']:.0f}%", cor)
    termometro(490, dados["temp"])

    canvas.create_window(300, 655, window=botao)


def atualizar():
    desenhar()
    janela.after(1000, atualizar)


janela = tk.Tk()
janela.title("Estação Meteorológica!")
janela.geometry("600x700")
janela.resizable(False, False)

canvas = tk.Canvas(janela, width=600, height=700, highlightthickness=0)
canvas.pack()

botao = tk.Button(janela, font=("Comic Sans MS", 12), fg="white",
                  activeforeground="white", bd=0, padx=20, pady=6,
                  command=alternar_conexao)
atualizar_botao()

carregar_imagens()
atualizar()
janela.mainloop()