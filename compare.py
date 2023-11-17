import numpy as np
import cv2
import warnings

warnings.filterwarnings('ignore')

# Declaracion de variables que determionan el rango minimo 
# y maximo de colores
white = np.array([
  [0, 0, 125],
  [179, 85, 255]
])
black = np.array([
  [0, 0, 0],
  [179, 65, 90]
])
pink = np.array([
  [150, 110, 100],
  [174, 255, 255]
])
purple = np.array([
  [127, 110, 100],
  [151, 255, 255]
])
blue = np.array([
  [90, 110, 100],
  [127, 255, 255]
])
green = np.array([
  [90, 110, 100],
  [38, 255, 255]
])
yellow = np.array([
  [90, 110, 100],
  [16, 255, 255]
])
orange = np.array([
  [5, 110, 100],
  [16, 255, 255]
])
red = np.array([
  [173, 110, 100],
  [179, 255, 255]
])

# Compara los pixeles de una foto que coinciden con el color 
# del filameto y los compara con el modelo
def compare (reference, model):
  flag = 0
  for row in range(reference.shape[0]):
    for column in range(reference.shape[1]):
      if reference[row, column] == 255 and model[row, column] == 0:
        flag = flag + 1
  return flag

# Obtiene los pixeles del rango de color del material
def get_piece (reference, clr_range, name):
  mask = cv2.inRange(reference, clr_range[0,:], clr_range[1,:])
  # kernel = np.ones((2,1), np.uint8)
  # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
  # mask = cv2.morphologyEx(mask_v, cv2.MORPH_OPEN, kernel)
  cv2.imwrite(f'images/mask_{name}.jpg', mask)
  return mask

def toHSV (file):
  img = cv2.imread({file})
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  return hsv

# Itera una mascara y retorna el primer pixel blanco que encuentre
def buscar_px (mask):
  for row in range(len(mask)):
    for column in range(len(mask[row])):
      if mask[row, column] == 255:
        pixel = [row, column]
        break
  return pixel

def match_sz (reference, match):
  reference_invx = reference[::-1]
  reference_invxy = reference_invx[:,::-1]
  px_l = buscar_px(reference_invx)
  px_r = len(reference[0]) - buscar_px(reference_invxy)
  ref_sz = px_l - px_r
  match_invx = match[::-1]
  match_invxy = match_invx[:,::-1]
  px_l = buscar_px(match_invx)
  px_r = len(match[0]) - buscar_px(match_invxy)
  match_sz = px_l - px_r

  if (ref_sz - match_sz) < 4:
    return match
  
  if ref_sz > match_sz:
    diff = ref_sz/match_sz
    nw_sz = cv2.resize(match, None, fx=diff, fy=diff)

# Crea una imagen que representa los bordes de otra imagen 
# pasada como parametro
def bordes (img, name):
  bd = np.empty((len(img), len(img[0]), 3))
  for row in range(len(img)):
    if row == len(img)-1:
      break
    for column in range(len(img[row])):
      if column == len(img[row])-1:
        bd[row, column, :] = 0
        break

      [b,g,r] = img[row, column] # Pixel actual
      [br,gr,rr] = img[row, column+1] # Pixel derecho
      [bu,gu,ru] = img[row+1, column] # Pixel de abajo

      # Calcular gris
      here = (b + g + r)/3
      right = (br + gr + rr)/3
      button = (bu + gu + ru)/3
      # Calcular diferencia de color
      diff_here = abs(here - right)
      diff_button = abs(here - button)
      # Definicion de los bordes de acuerdo a un umbral
      if (diff_here + diff_button) < 25:
        bd[row, column, :] = 0
      else:
        bd[row, column, :] = 255
  cv2.imwrite(f'images/{name}_bd.jpg', bd)

# bordes(model, 'model')

def init (photo, stl_img, color):
  reference = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
  piece_ref = get_piece(reference, color, 'ref')
  model = cv2.cvtColor(stl_img, cv2.COLOR_BGR2HSV)
  piece_mod = get_piece(model, color, 'mod')

  error = compare(piece_ref, piece_mod)
  print(error)
  diff = cv2.subtract(piece_ref, piece_mod)
  cv2.imwrite('images/ref_diff.jpg', diff)

photo = cv2.imread('images/foto.png')
render = cv2.imread('images/render.png')
init(photo, render, white)
