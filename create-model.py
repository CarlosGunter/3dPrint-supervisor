import numpy as np
from skimage import io
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

## Guardar el modelo como imagen
# Se crea el espacio de renderizado
figure = pyplot.figure()
axes = figure.add_subplot(projection='3d')
axes.grid(visible=None)
axes.set_axis_off()
axes.view_init(0,-20)

# Se carga el STL
your_mesh = mesh.Mesh.from_file('stl/utahteapot_ws.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
scale = your_mesh.points.flatten() 
axes.auto_scale_xyz(scale, scale, scale)

# Se guarda el modelo
pyplot.savefig('images/model.jpg', format='jpg', bbox_inches='tight', pad_inches=0)
pyplot.close()

## Convertir imagen del modelo a escala de grises
model = pyplot.imread('images/model.jpg')
model_gray = []
for i in range(len(model)):
  model_gray.append([])
  for j in range(len(model[i])):
    [b,g,r] = model[i][j]
    if b == 255 or g == 255 or r == 255:
      model_gray[i].append([255,255,255])
    else:
      model_gray[i].append([0,0,0])
pyplot.imshow(model_gray, cmap="grey")
pyplot.axis('off')
pyplot.savefig('images/model_g.jpg', format='jpg', bbox_inches='tight', pad_inches=0)
pyplot.close()