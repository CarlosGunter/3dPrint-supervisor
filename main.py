from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from compare import init
from PIL import ImageTk, Image

path_photo = None
path_render = None

def main ():

  root = Tk()
  root.geometry("1000x800")

  def run ():
    label_result.config(text='Calculando...')
    label_result.text = 'Calculando...'
    photo = cv2.imread(path_photo)
    stl_img = cv2.imread(path_render)
    error = init(photo, stl_img)

    result = Image.open('images/ref_diff.png')
    result = result.resize((300,180))
    result_img = ImageTk.PhotoImage(result)
    label_result.config(image=result_img, text='')
    label_result.image = result_img

    label_error.config(text=f'Porcentaje de error: {error}%')
    label_error.text = f'Porcentaje de error: {error}%'

  def img_load ():
    if path_photo is not None and path_render is not None:
      butt_run = Button(label_run, command=run, text="Comparar")
      butt_run.pack()

  def get_photo ():
    global path_photo, photo
    path_photo = filedialog.askopenfilename(title="Fotografia", initialdir='F:/Bibliotecas/Documents/Programacion/Python/proyectoIA', filetypes=(("Imagen","*.png"), ("Imagen","*.jpg")))
    
    photo = Image.open(path_photo)
    photo = photo.resize((300,180))
    photo_img = ImageTk.PhotoImage(photo)
    label_ph.config(image=photo_img)
    label_ph.image = photo_img
    img_load()

  def get_render ():
    global path_render, render
    path_render = filedialog.askopenfilename(title="Render", initialdir='F:/Bibliotecas/Documents/Programacion/Python/proyectoIA', filetypes=(("Imagen","*.png"), ("Imagen","*.jpg")))

    render = Image.open(path_render)
    render = render.resize((300,180))
    render_img = ImageTk.PhotoImage(render)
    label_ren.config(image=render_img)
    label_ren.image = render_img
    img_load()

  sel_photo = Button(root, command=get_photo, text="Fotografia")
  sel_photo.grid(row=0, column=0)
  sel_render = Button(root, command=get_render, text="Render")
  sel_render.grid(row=0, column=2)

  label_ph = Label(root)
  label_ph.grid(row=1, column=0)
  
  label_ren = Label(root)
  label_ren.grid(row=1, column=2)

  label_run = Label(root)
  label_run.grid(row=2, column=1)

  label_result = Label(root)
  label_result.grid(row=3, column=1)

  label_error = Label(root)
  label_error.grid(row=4, column=1)

  root.mainloop()

main()
