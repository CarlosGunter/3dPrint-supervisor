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
  mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
  cv2.imwrite(f'images/mask_{name}.png', mask_bgr)
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

def limits (mask):
  top = len(mask) - buscar_px(np.fliplr(mask))[0]
  button = buscar_px(mask)[0]
  left = len(mask[0]) - buscar_px(np.rot90(mask, 1))[0]
  right = buscar_px(np.rot90(mask, -1))[0]
  return top, button, left, right

# Iguala el tamaño y posicion de la pieza del render respecto a la
# pieza de la referencia
def match (reference, match):
  model = np.zeros((np.shape(reference)[0], np.shape(reference)[1]), dtype='uint8')
  ref_t, ref_b, ref_l, ref_r = limits(reference)
  print(ref_t, ref_b, ref_l, ref_r)
  ref_h = ref_b - ref_t # Alto
  ref_w = ref_r - ref_l # Ancho
  
  mch_t, mch_b, mch_l, mch_r = limits(match)
  print(mch_t, mch_b, mch_l, mch_r)
  mch_h = mch_b - mch_t # Alto
  mch_w = mch_r - mch_l # Ancho

  # Tolerancia de 4px
  if abs(ref_w - mch_w) < 4:
    print('Igual')
    return match
  
  # if ref_w > mch_w:
  diff_w = ref_w/mch_w
  diff_h = ref_h/mch_h
  nw_sz = cv2.resize(match, None, fx=diff_w, fy=diff_h)

  nw_t, nw_b, nw_l, nw_r = limits(nw_sz)
  nw_h = nw_b - nw_t
  nw_w = nw_r - nw_l
  print(nw_t, nw_b, nw_l, nw_r)
  # if len(nw_sz) <= len(reference) or len(nw_sz[0]) <= len(reference[0]):
  model[ref_t:(ref_t + nw_h), ref_l:(ref_l + nw_w)] = nw_sz[nw_t:nw_b, nw_l:nw_r]
  a = nw_sz[nw_t:nw_b, nw_l:nw_r]
  a_bgr = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
  cv2.imwrite('images/piece.png', a_bgr)

  model_bgr = cv2.cvtColor(model, cv2.COLOR_GRAY2BGR)
  cv2.imwrite('images/mask_match.png', model_bgr)
  return model

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

  bd_bgr = cv2.cvtColor(bd, cv2.COLOR_GRAY2BGR)
  cv2.imwrite(f'images/{name}_bd.png', bd_bgr)

def init (photo, stl_img, color=white):
  # Cambiar el formato a HSV
  reference = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
  # Obtiene la mascara de color del filamento
  piece_ref = get_piece(reference, color, 'ref')
  # Cambiar el formato a HSV
  model = cv2.cvtColor(stl_img, cv2.COLOR_BGR2HSV)
  # Obtiene la mascara de color del render
  piece_mod = get_piece(model, color, 'mod')
  # Se iguala el tamaño y posicion de la pieza en la imagen del
  # render, asi como el tamaño de imagen respecto a la fotografia
  piece_mod = match(piece_ref, piece_mod)
  # Obtiene graficemente las diferencias
  diff = cv2.subtract(piece_ref, piece_mod)
  # Obtiene las diferencias entre el modelo y la fotografia
  error = compare(piece_ref, piece_mod)
  # Calcula el porcentaje de error
  percent = round((error*100)/(np.shape(piece_ref)[0]*np.shape(piece_ref)[1]), 2)

  diff_bgr = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
  cv2.imwrite('images/ref_diff.png', diff_bgr)
  
  return percent

# photo = cv2.imread('images/foto.png')
# render = cv2.imread('images/render.png')
# init(photo, render, white)
