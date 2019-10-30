# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 20:27:07 2019

@author: jedhm
"""


from astropy.io import fits 
import numpy as np
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
ff = h5py.File('datasets/flatfields.hdf5', 'w')
ff.create_dataset("ff_set", data=img_stack_ff)
ff.close()

df = h5py.File('datasets/darkframes.hdf5', 'w')
df.create_dataset("df_set", data=img_stack_df)
df.close()

ast = h5py.File('datasets/asteroids.hdf5', 'w')
ast.create_dataset("ast_set", data=img_stack_ast)
ast.close()

# %% function approach

def import_files(path, frame_type):
    """ import files into datacubes by type  
        flatfield (ff), darkframe (df), asteroid (ast)
    """
    from astropy.io import fits 
    import numpy as np
    import glob
    import h5py
    
    # dimensions of stacked raw fits
    NAXIS1, NAXIS2, NAXIS3 = 695, 519, 50
    NAXIS3_ast = 309

    if frame_type == 'ff':
        flatfield_list = sorted(glob.glob(path + '/*f.fit'))
        img_stack_ff = np.zeros((NAXIS3, NAXIS2, NAXIS1), dtype=np.float32)

        for i in range(0,NAXIS3):
            hdul = fits.open(flatfield_list[i], memmap=False)
            img_stack_ff[i, :, :] = hdul[0].data
            ff_norm = (1/50)*np.sum(img_stack_ff, axis = 0)/np.amax((1/50)*np.sum(img_stack_ff, axis = 0))

        ff = h5py.File('datasets/flatfields.hdf5', 'w')
        ff.create_dataset("DataCube", data=img_stack_ff)
        ff.close()

    if frame_type == 'df':
        darkframe_list = sorted(glob.glob('04_04_ast/*d.fit'))
        img_stack_df = np.zeros((NAXIS3, NAXIS2, NAXIS1), dtype=np.float32)

        for i in range(0,NAXIS3):
            hdul = fits.open(darkframe_list[i], memmap=False)
            img_stack_df[i, :, :] = hdul[0].data
            df_av = (1/50)*np.sum(img_stack_df, axis = 0)

        df = h5py.File('datasets/darkframes.hdf5', 'w')
        df.create_dataset("df_set", data=img_stack_df)
        df.close()

    if frame_type == 'ast':
        asteroid_list = sorted(glob.glob('04_04_ast/*l5.fit'))
        img_stack_ast = np.zeros((NAXIS3_ast, NAXIS2, NAXIS1), dtype=np.float32)

        for j in range(NAXIS3_ast):
            hdul = fits.open(asteroid_list[j], memmap=False)
            img_stack_ast[j, :, :] = hdul[0].data/ff_norm - df_av
        # create datacube files for ff, df & asteroids

        ast = h5py.File('datasets/asteroids.hdf5', 'w')
        ast.create_dataset("ast_set", data=img_stack_ast)
        ast.close()