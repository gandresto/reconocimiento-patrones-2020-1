# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:52:03 2019

@author: Andres
"""
#%%
import rasterio
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import glob
#from tqdm import tqdm
from funciones import predecir

#%%
path_datos_prueba = glob.glob('./Dataset/Test/*data.tif')
datos_prueba  = np.array([np.dstack(np.array(rasterio.open(path).read())) for path in path_datos_prueba])
datos_prueba = datos_prueba[:,:,:,0:5]/65536.0
#%%
imgs = np.flip(datos_prueba[:,:,:,1:4], 3)
img_ir = datos_prueba[:,:,:,0]
#%%
modelo = np.load('./modelo.npy', allow_pickle=True).item()

#%%
pred_y = np.zeros_like(datos_prueba[:,:,:,0]).astype(np.uint8)
#tqdm.write('Predicción de resultados...')
for i, datos_x in enumerate(datos_prueba):
    pred_y[i] = predecir(datos_x, modelo)

#%%
# Value / Interpretation
# 0    Shadow
# 1    Shadow over Water
# 2    Water
# 3    Snow
# 4    Land
# 5    Cloud
clases = modelo['clases']
n_clases = len(clases)

sombra = np.array([0., 0., 0., 1.])
sombra_sa = np.array([0., 0., 0.5, 1.])
agua = np.array([0., 0., 1., 1.])
nieve = np.array([0., 1., 1., 1.])
tierra = np.array([0.5, 0.5, 0.5, 1.])
nube = np.array([1., 1., 1., 1.])

#nuevos_colores = np.zeros(shape=(256, 4))
#div = 256/6.
#nuevos_colores[:np.round(div), :]=sombra
#nuevos_colores[np.round(div)+1:np.round(div*2), :]=sombra_sa
#nuevos_colores[np.round(div*2)+1:np.round(div*3), :]=nieve
#nuevos_colores[np.round(div*3)+1:np.round(div*4), :]=tierra
#nuevos_colores[np.round(div*4+1):, :]=tierra
nuevos_colores = np.zeros(shape=(n_clases, 4))
div = 256/6.
nuevos_colores[0, :]=sombra
nuevos_colores[1, :]=sombra_sa
nuevos_colores[2, :]=agua
nuevos_colores[3, :]=nieve
nuevos_colores[4, :]=tierra
nuevos_colores[5, :]=nube
custom_cm = ListedColormap(nuevos_colores) 

#%%
for i, img in enumerate(imgs):
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(imgs[i])
    imsh = axs[1].imshow(pred_y[i], cmap=custom_cm, vmin=0, vmax=6)
    axs[0].axis('off')
    axs[1].axis('off')
    axs[0].set_title('Imagen %d' %i)
    axs[1].set_title('Resultados')
    patches = [ mpatches.Patch(color=nuevos_colores[i], label=clases[i]) for i in range(len(clases)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
    #cbar = fig.colorbar(imsh, ticks=list(modelo['clases'].keys()))
    #cbar.ax.set_yticklabels(list(modelo['clases'].values())) 
    plt.show()

#%%
np.save('./Dataset/test/predicciones', pred_y)
#%%
for i, path in enumerate(path_datos_prueba):
    plt.imsave(path[:-9]+'pred.png', pred_y[i], cmap=custom_cm, vmin=0, vmax=6)
#%%
#for i, img in enumerate(imgs):
#    fig, axs = plt.subplots(2,2)
#    for b1 in range(2):
#        for b2 in range(2):
#            axs[b1, b2].imshow(datos_prueba[i,:,:,b1+b2], cmap='gray')
#            axs[b1, b2].axis('off')
#            axs[b1, b2].set_title('Banda %d' % (b1+b2))
#    plt.show()