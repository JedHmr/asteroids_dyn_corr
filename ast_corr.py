# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 20:31:41 2019

@author: jedhm
"""


from astropy.io import fits 
import numpy as np
import matplotlib.pyplot as plt
import glob
import h5py

# fits files lists
flatfield_list = sorted(glob.glob('04_04_ast/*f.fit'))
darkframe_list = sorted(glob.glob('04_04_ast/*d.fit'))
asteroid_list = sorted(glob.glob('04_04_ast/*l5.fit'))

# dimensions of stacked raw fits
NAXIS1 = 695
NAXIS2 = 519
NAXIS3 = 50
NAXIS3_ast = 309

# initialising image stacks
img_stack_ff = np.zeros((NAXIS3, NAXIS2, NAXIS1), dtype=np.float32)
img_stack_df = np.zeros((NAXIS3, NAXIS2, NAXIS1), dtype=np.float32)
img_stack_ast = np.zeros((NAXIS3_ast, NAXIS2, NAXIS1), dtype=np.float32)

# flatfield/darkframe stacks
for i in range(NAXIS3):
    hdul = fits.open(flatfield_list[i], memmap=False)
    hdul2 = fits.open(darkframe_list[i], memmap=False)
    img_stack_ff[i, :, :] = hdul[0].data
    img_stack_df[i, :, :] = hdul2[0].data

# flatfield normalisation and darkframe averaging
ff_norm = (1/50)*np.sum(img_stack_ff, axis = 0)/np.amax((1/50)*np.sum(img_stack_ff, axis = 0))
df_av = (1/50)*np.sum(img_stack_df, axis = 0)

# create corrected stack of asteroid images
for j in range(NAXIS3_ast):
     hdul = fits.open(asteroid_list[j], memmap=False)
     img_stack_ast[j, :, :] = hdul[0].data/ff_norm - df_av

# create datacube files for ff, df & asteroids
ff = h5py.File('flatfields.hdf5', 'w')
ff.create_dataset("DataCube", data=img_stack_ff)
ff.close()

df = h5py.File('darkframes.hdf5', 'w')
df.create_dataset("DataCube", data=img_stack_df)
df.close()

ast = h5py.File('asteroids.hdf5', 'w')
ast.create_dataset("DataCube", data=img_stack_ast)
ast.close()


plt.figure(1)
plt.imshow(img_stack_ast[20, :, :], cmap='hot')