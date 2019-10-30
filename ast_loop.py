# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 20:18:51 2019

@author: jedhm
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

# initial asteroid coordinates
L = 20
xa = 274
ya = 290


for i in range(1,309):
    
    if i == 1: 
        # for first asteroid
        raw = (img_stack_ast[1, :, :] - np.mean(img_stack_ast[1, :, :]))/np.max(img_stack_ast[1, :, :])
        ast_template = np.copy(img_stack_ast[1, :, :][(ya-L):(ya+L), (xa-L):(xa+L)])
        ast_template_c = (ast_template - np.mean(ast_template))/np.max(ast_template)
        
        corr = signal.correlate2d(raw, ast_template_c, boundary='symm', mode='same')
        np.place(corr, corr > 1, [0])
        ya, xa = np.unravel_index(np.argmax(corr), corr.shape) # find the match
        
    elif i > 1:
        
        # for next asteroid
        # i'th sky image
        raw = (img_stack_ast[i, :, :] - np.mean(img_stack_ast[i, :, :]))/np.max(img_stack_ast[i, :, :])
        
        # i'th correlation of i'th sky with i-1'th asteroid template
        corr = signal.correlate2d(raw, ast_template_c, boundary='symm', mode='same')
        #np.place(corr, corr > 1, [0])
        ya, xa = np.unravel_index(np.argmax(corr), corr.shape) # find the match
        
        # update asteroid template
        ast_template = np.copy(img_stack_ast[i, :, :][(ya-L):(ya+L), (xa-L):(xa+L)])
        ast_template_c = (ast_template - np.mean(ast_template))/np.max(ast_template)
    
        # copy i'th asteroid (raw but corrected)
        ast_template_crop = np.copy(img_stack_ast[i, :, :][(ya-L):(ya+L), (xa-L):(xa+L)])
        
        # write template to folder
        asteroids = h5py.File('asteroids/asteroid%.hdf5' %i, 'w')
        asteroids.create_dataset("DataCube", data=ast_template_crop)
        asteroids.close()

    # plot raw image, asteroid template and correlation map
    fig, (ax_raw, ax_asteroid, ax_corr) = plt.subplots(1, 3)
    ax_raw.imshow(img_stack_ast[i, :, :], cmap='hot')
    ax_raw.set_title('raw')
    rect = patches.Rectangle((xa-L,ya-L),2*L,2*L,linewidth=0.5,edgecolor='b',facecolor='none')
    ax_raw.add_patch(rect)
    ax_asteroid.imshow(ast_template_c, cmap='hot')
    ax_asteroid.set_title('located asteroid')
    ax_corr.imshow(corr, cmap ='gray')
    rect = patches.Rectangle((xa-L,ya-L),2*L,2*L,linewidth=0.5,edgecolor='b',facecolor='none')
    ax_corr.add_patch(rect)
    ax_corr.set_title('correlation')
    plt.ion()
    plt.show()

    plt.pause(0.01)
    plt.draw()

def ast_img_corr(img_stack, init_xy):

    for i in range(1,len(data)):
    
    if i == 1: 
        # for first asteroid
        raw = (img_stack_ast[1, :, :] - np.mean(img_stack_ast[1, :, :]))/np.max(img_stack_ast[1, :, :])
        ast_template = np.copy(img_stack_ast[1, :, :][(init_xy[1]-L):(init_xy[1]+L), (init_xy[0]-L):(init_xy[0]+L)])
        # corrected asteroid template
        ast_template_c = (ast_template - np.mean(ast_template))/np.max(ast_template)
        
        corr = signal.correlate2d(raw, ast_template_c, boundary='symm', mode='same')
        np.place(corr, corr > 1, [0])
        ya, xa = np.unravel_index(np.argmax(corr), corr.shape) # find the match
        
    elif i > 1:
        
        # for next asteroid
        # i'th sky image
        raw = (img_stack_ast[i, :, :] - np.mean(img_stack_ast[i, :, :]))/np.max(img_stack_ast[i, :, :])
        
        # i'th correlation of i'th sky with i-1'th asteroid template
        corr = signal.correlate2d(raw, ast_template_c, boundary='symm', mode='same')
        #np.place(corr, corr > 1, [0])
        ya, xa = np.unravel_index(np.argmax(corr), corr.shape) # find the match
        
        # update asteroid template
        ast_template = np.copy(img_stack_ast[i, :, :][(ya-L):(ya+L), (xa-L):(xa+L)])
        ast_template_c = (ast_template - np.mean(ast_template))/np.max(ast_template)
    
        # copy i'th asteroid (raw but corrected)
        ast_template_crop = np.copy(img_stack_ast[i, :, :][(ya-L):(ya+L), (xa-L):(xa+L)])
        
        # write template to folder
        asteroids = h5py.File('asteroids/asteroid%.hdf5' %i, 'w')
        asteroids.create_dataset("DataCube", data=ast_template_crop)
        asteroids.close()

    # plot raw image, asteroid template and correlation map
    fig, (ax_raw, ax_asteroid, ax_corr) = plt.subplots(1, 3)
    ax_raw.imshow(img_stack_ast[i, :, :], cmap='hot')
    ax_raw.set_title('raw')
    rect = patches.Rectangle((xa-L,ya-L),2*L,2*L,linewidth=0.5,edgecolor='b',facecolor='none')
    ax_raw.add_patch(rect)
    ax_asteroid.imshow(ast_template_c, cmap='hot')
    ax_asteroid.set_title('located asteroid')
    ax_corr.imshow(corr, cmap ='gray')
    rect = patches.Rectangle((xa-L,ya-L),2*L,2*L,linewidth=0.5,edgecolor='b',facecolor='none')
    ax_corr.add_patch(rect)
    ax_corr.set_title('correlation')
    plt.ion()
    plt.show()

    plt.pause(0.01)
    plt.draw()