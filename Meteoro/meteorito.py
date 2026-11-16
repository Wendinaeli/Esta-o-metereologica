import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial 
import time

def retangulo_arredondado(cv, x1, y1, x2, y2, r=20, **kw):
    pontos = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
              x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
              x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    return cv.create_polygon(pontos, smooth=True, **kw)


def criar_entry_arredondado(x, y, r=30):
    entrada = tk.Entry(janela, font=("Comic Sans MS", 60), bg="#f0f0f0", width=8, justify='center')
    entrada.update_idletasks()

    w = entrada.winfo_reqwidth()
    h = entrada.winfo_reqheight()

    retangulo_arredondado(canvas, x, y, x+w, y+h, r=r,
                          fill="#f0f0f0", outline="#070707", width=2)

    entrada.config(bd=0, highlightthickness=0)
    canvas.create_window(x+w/2, y+h/2, window=entrada,
                         width=w - 2*r, height=h - 8)
    return entrada


janela = tk.Tk()
janela.title("Estação Meteorológica!")
janela.geometry("600x700")
janela.resizable(False, False)
janela.configure(bg="#81A1EA")

canvas = tk.Canvas(janela, width=600, height=700,
                   highlightthickness=0, bg="#81A1EA")
canvas.pack()  

# Exemplo de uso do entry arredondado
entrada_temp = criar_entry_arredondado(107, 80)

janela.mainloop()