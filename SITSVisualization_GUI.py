# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 23:56:18 2023

@author: andre
"""

import os
import scipy.io
import rasterio
import numpy as np
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

#--- functii frame RGB  
def griscale(x,pmin,pmax): #https://youtu.be/zusDevq6ggs?t=607
    x = x.astype(float)
    return((x-np.nanpercentile(x, pmin))/(np.nanpercentile(x, pmax)
                                         -np.nanpercentile(x, pmin)))

def open_info():
    global info
    t3.delete('1.0',tk.END)
        
    filepath = tk.filedialog.askopenfilename(title='select', 
                                             filetypes= [("pkl, csv", [".pkl",".csv"]),
                                                         ("pkl", ".pkl"),
                                                         ("csv",".csv")]) 
   # t1.insert(tk.END,filepath.split('/')[-1])
    if filepath[-4:] == '.pkl':
        info = pd.read_pickle(filepath)
    else:
        info = pd.read_csv(filepath, dtype = 'object')
        
    start = info.loc[0].day + '.' + info.loc[0].month + '.'+info.loc[0].year
    stop = info.loc[len(info)-1].day + '.' + info.loc[len(info)-1].month + '.'+info.loc[len(info)-1].year
    t3.insert(tk.END, 'dd.mm.yyyy \n start: ' + start +
              '\n stop: ' + stop )
    
def open_red():
    global red, s_red,red_name
    t1_red.delete('1.0',tk.END)
        
    filepath = tk.filedialog.askopenfilename(title='select', 
                                             filetypes= [("npy, mat, tif", 
                                                          [".npy",".mat",".tif"])]) 
    if filepath[-4:] == '.npy':
        red = np.load(filepath)
        s_red = red.shape
    elif filepath[-4:] == '.mat':
        mat = scipy.io.loadmat(filepath)
        red = mat[list(mat.keys())[0]]
        s_red = red.shape
    else:
        img1 = rasterio.open(filepath)
        red = img1.read()
        img1.close()
        del img1
        red = red.transpose(1,2,0) #rows,cols,time
        red = np.nan_to_num(red)
        red = np.clip(griscale(red,2,98),0,1)
        red = ((red-np.min(red))/(np.max(red)-np.min(red)))*255
        s_red = red.shape
    
    red_name = filepath.split('/')[-2] +'\\' + filepath.split('/')[-1]
    t1_red.insert(tk.END, 'filename: ' + red_name +
              '\n shape: ' + str(s_red) )
    
def open_green():
    global green, s_green, green_name
    t1_green.delete('1.0',tk.END)
        
    filepath = tk.filedialog.askopenfilename(title='select', 
                                             filetypes= [("npy, mat, tif", 
                                                          [".npy",".mat",".tif"])]) 
    if filepath[-4:] == '.npy':
        green = np.load(filepath)
        s_green = green.shape
    elif filepath[-4:] == '.mat':
        mat = scipy.io.loadmat(filepath)
        green = mat[list(mat.keys())[0]]
        s_green = green.shape
    else:
        img1 = rasterio.open(filepath)
        green = img1.read()
        img1.close()
        del img1
        green = green.transpose(1,2,0) #rows,cols,time
        green = np.nan_to_num(green)
        green = np.clip(griscale(green,2,98),0,1)
        green = ((green-np.min(green))/(np.max(green)-np.min(green)))*255
        s_green = green.shape
        
    green_name = filepath.split('/')[-2] +'\\' + filepath.split('/')[-1]
    t1_green.insert(tk.END, 'filename: ' + green_name +#os.path.basename(filepath) +
              '\n shape: ' + str(s_green) )
    
def open_blue():
    global blue, s_blue, blue_name
    t1_blue.delete('1.0',tk.END)
        
    filepath = tk.filedialog.askopenfilename(title='select', 
                                             filetypes= [("npy, mat, tif", 
                                                          [".npy",".mat",".tif"])])
    
    if filepath[-4:] == '.npy':
        blue = np.load(filepath)
        s_blue = blue.shape
    elif filepath[-4:] == '.mat':
        mat = scipy.io.loadmat(filepath)
        blue = mat[list(mat.keys())[0]]
        s_blue = blue.shape
    else:
        img1 = rasterio.open(filepath)
        blue = img1.read()
        img1.close()
        del img1
        blue = blue.transpose(1,2,0) #rows,cols,time
        blue = np.nan_to_num(blue)
        blue = np.clip(griscale(blue,2,98),0,1)
        blue = ((blue-np.min(blue))/(np.max(blue)-np.min(blue)))*255
        s_blue = blue.shape
    
    blue_name = filepath.split('/')[-2] +'\\' + filepath.split('/')[-1]
    t1_blue.insert(tk.END, 'filename: ' + blue_name +#os.path.basename(filepath) +
              '\n shape: ' + str(s_blue) )

#----- afiseaza cub
def afiseaza_cub():
    pass
    max_row, max_col, max_time = np.ceil(np.array(s_red)/10).astype('int')
    
    
    shw_time = e1_value_rgb.get()
    if shw_time == '':
          shw_time = 0
          e1_value_rgb.set('0')
    else:
        shw_time = int(e1_value_rgb.get())
        
    shw_row = e1_value_row.get()
    if shw_row == '':
          shw_row = 0
          e1_value_row.set('0')
    else:
        shw_row = int(e1_value_row.get())

    shw_col = e1_value_col.get()
    if shw_col == '':
          shw_col = 0
          e1_value_col.set('0')
    else:
        shw_col = int(e1_value_col.get())
    
    
    
    idx_time = shw_time//max_time
    idx_row = shw_row//max_row
    idx_col = shw_col//max_col
        #crearea figurii care va contine graficul semnalului
    fig = Figure(figsize = (4, 4), dpi = 60)
    
        # adaugarea subgraficului
    plot1 = fig.add_subplot(111, projection = '3d')
      
        # Create axis
    #axes = [s_red[2], s_red[1], s_red[0]]
    axes = [10, 10, 10]    
        # Create Data
    data = np.ones(axes, dtype= bool)
 
    # Control Transparency
    alpha = 0.9
     
    # Control colour
    colors = np.empty(axes + [4], dtype=np.float32)
    gri = [1,1,1,alpha]
    colors = np.tile(gri,(axes[0],axes[1], axes[2],1))
    # for i in range(axes[0]):
    #     colors[i] = [1, 1, 1, alpha]
    
    
    colors[idx_time,:,:,:] = [0, 1, 0, alpha]  # green for time
    colors[:,idx_col,:,:] = [0, 0, 1, alpha]  # blue for column
    colors[:,:,idx_row,:] = [1, 1, 0, alpha]  # yellow for row
    
    
     
       
    # Voxels is used to customizations of
    # the sizes, positions and colors.
    plot1.voxels(data, facecolors=colors, edgecolors='grey')
    plot1.set_xlabel('time: idx = ' + str(shw_time))
    plot1.set_ylabel('columns: idx = ' + str(shw_col))
    plot1.set_zlabel('rows: idx = ' + str(shw_row))
    plot1.view_init(elev = 23, azim = -142)    
    plot1.set_title('Current exploration')
    
    # plot1.set_xticks(range(0,max_time,10))
    # plot1.set_yticks(range(0,max_col,10))
    # plot1.set_zticks(range(0,max_row,10))
    
    plot1.set_xticks(range(10),np.arange(0,max_time*10,max_time).astype(str))
    plot1.set_yticks(range(10),np.arange(0,max_col*10,max_col).astype(str))
    plot1.set_zticks(range(10),np.arange(0,max_row*10,max_row).astype(str))    
  
    # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_cube)
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 10)

#----- functii explorarea pe randuri

def afiseaza_row():
    global rgb_row
    idx = e1_value_row.get()
    if idx == '':
         idx = 0
         e1_value_row.set('0')
         afiseaza_cub()
    else:
        idx = int(e1_value_row.get())
        afiseaza_cub()
    
           
            
    #crearea figurii care va contine graficul semnalului
    fig = Figure(figsize = (4, 4), dpi = 60)

    # adaugarea subgraficului
    plot1 = fig.add_subplot(111)
  
    # formare rgb
    rgb_row  = np.zeros((s_red[2],s_red[1],3))
    if np.sum(np.abs(np.array(s_red)-np.array(s_green))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    elif np.sum(np.abs(np.array(s_red)-np.array(s_blue))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    else:
        rgb_row[:,:,0] = red[idx,:,:].transpose(1,0)
        rgb_row[:,:,1] = green[idx,:,:].transpose(1,0)
        rgb_row[:,:,2] = blue[idx,:,:].transpose(1,0)
    #print(rgb_row.shape)
    
    
    
    plot1.imshow(rgb_row.astype('uint8'), aspect = 'auto')
           
    #print(date)
    plot1.set_title('Row: ' + str(idx))
    plot1.set_xlabel('Column')
    plot1.set_ylabel('Time')
  
    # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_explrow)
  
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 2, column = 0, columnspan = 10)
  
    #plt.figure(), plt.imshow(rgb_row.astype('uint8')), plt.title(str(idx))
    #canvas.get_tk_widget().destroy() # pt distrugere canvas
    
def afiseaza_up_row():
    e1_value_row.set(str((int(e1_value_row.get())+1)%s_red[0]))
    afiseaza_row()
    
def afiseaza_down_row():
    e1_value_row.set(str((int(e1_value_row.get())-1)%s_red[0]))
    afiseaza_row()
    
    
#----- functii explorarea pe coloane

def afiseaza_col():
    global rgb_col
    idx = e1_value_col.get()
    if idx == '':
         idx = 0
         e1_value_col.set('0')
         afiseaza_cub()
    else:
        idx = int(e1_value_col.get())
        afiseaza_cub()      
            
    #crearea figurii care va contine graficul semnalului
    fig = Figure(figsize = (4, 4), dpi = 60)

    # adaugarea subgraficului
    plot1 = fig.add_subplot(111)
  
    # formare rgb
    rgb_col  = np.zeros((s_red[0],s_red[2],3))
    if np.sum(np.abs(np.array(s_red)-np.array(s_green))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    elif np.sum(np.abs(np.array(s_red)-np.array(s_blue))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    else:
        rgb_col[:,:,0] = red[:,idx,:]
        rgb_col[:,:,1] = green[:,idx,:]
        rgb_col[:,:,2] = blue[:,idx,:]
    print(rgb_col.shape)
    
    
    
    plot1.imshow(rgb_col.astype('uint8'), aspect = 'auto')
           
    #print(date)
    plot1.set_title('Column: ' + str(idx))
    plot1.set_xlabel('Time')
    plot1.set_ylabel('Row')
  
    # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_explcol)
  
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 2, column = 0, columnspan = 10)
  
    #plt.figure(), plt.imshow(rgb_col.astype('uint8')), plt.title(str(idx))
    #canvas.get_tk_widget().destroy() # pt distrugere canvas
    
def afiseaza_up_col():
    e1_value_col.set(str((int(e1_value_col.get())+1)%s_red[1]))
    afiseaza_col()
    
def afiseaza_down_col():
    e1_value_col.set(str((int(e1_value_col.get())-1)%s_red[1]))
    afiseaza_col()


#---- functii explorarea in timp

def afiseaza_rgb():
    global rgb
    idx = e1_value_rgb.get()
    if idx == '':
         idx = 0
         e1_value_rgb.set('0')
         afiseaza_cub()
    else:
        idx = int(e1_value_rgb.get())
        afiseaza_cub()       
            
    #crearea figurii care va contine graficul semnalului
    fig = Figure(figsize = (4, 4), dpi = 60)

    # adaugarea subgraficului
    plot1 = fig.add_subplot(111)
  
    # formare rgb
    rgb  = np.zeros((s_red[0],s_red[1],3))
    if np.sum(np.abs(np.array(s_red)-np.array(s_green))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    elif np.sum(np.abs(np.array(s_red)-np.array(s_blue))) != 0:
        print('benzile alese pentru formarea imaginii color trebuie sa aiba aceleasi dimensiuni !')
    else:
        rgb[:,:,0] = red[:,:,idx]
        rgb[:,:,1] = green[:,:,idx]
        rgb[:,:,2] = blue[:,:,idx]
    
    
    
    plot1.imshow(rgb.astype('uint8'), aspect = 'auto')
    date = ' no info' 
    if 'info' in globals():
        date = info.loc[idx].day + '.' + info.loc[idx].month + '.'+info.loc[idx].year
    else:
      date = ' no info'            
    #print(date)
    plot1.set_title('Datetime: ' + date)
    plot1.set_xlabel('Column')
    plot1.set_ylabel('Row')
  
    # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_expltime)
  
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 2, column = 0, columnspan = 10)
  
    #canvas.get_tk_widget().destroy() # pt distrugere canvas
    
def afiseaza_up_rgb():
    e1_value_rgb.set(str((int(e1_value_rgb.get())+1)%s_red[2]))
    afiseaza_rgb()
    
def afiseaza_down_rgb():
    e1_value_rgb.set(str((int(e1_value_rgb.get())-1)%s_red[2]))
    afiseaza_rgb()
    
def clicked(): 
    if r.get() == 1:
       show_frame1pix()
       hide_frame4pix()
       rb_opt.configure(text = "Shows the temporal evolution of the chosen pixel's values through \n the three loaded SITS (Red, Green, Blue).")
       
    if r.get() == 2:
        show_frame4pix()
        hide_frame1pix()
        rb_opt.configure(text = "Shows the temporal evolution of the chosen four pixels \n value through the chosen loaded SITS.")
     
        
def show_frame1pix():
    frame_4pix.pack_forget()
    frame_1pix.pack()
def hide_frame1pix():
   frame_1pix.pack_forget()
   frame_4pix.pack()
   
def show_frame4pix():
    frame_1pix.pack_forget()
    frame_4pix.pack()
def hide_frame4pix():
   frame_4pix.pack_forget()
   frame_1pix.pack()
   
   
def afiseaza_4pix():
    xy = list()
    xy.append(e11_xy.get().replace(' ','').replace('(','').replace(')','').split(','))
    xy.append(e2_xy.get().replace(' ','').replace('(','').replace(')','').split(','))
    xy.append(e3_xy.get().replace(' ','').replace('(','').replace(')','').split(','))
    xy.append(e4_xy.get().replace(' ','').replace('(','').replace(')','').split(','))
    #print('xy' ,xy)
    xy = np.array(xy).astype(int)
    #print(xy1)
    #!!! functioneaza doar daca are x,y introdus pentru toti pixelii
    
    
    # crearea figurii care va contine graficul semnalului
    #fig = Figure(figsize = (6, 4), dpi = 100)
    fig = Figure(figsize = (6, 4), dpi = 60)
    # adaugarea subgraficului
    plot1 = fig.add_subplot(111)
  
    # afisarea semnaturii temporale
    if rband.get() == 2:
        for i in range(len(xy)):        
            plot1.plot(green[xy[i,1],xy[i,0],:], label = 'pixel ' + str(i))
        plot1.set_title(green_name + ' evolution')
    elif rband.get() == 3:
        for i in range(len(xy)):
            plot1.plot(blue[xy[i,1],xy[i,0],:], label = 'pixel ' + str(i))
        plot1.set_title(blue_name + ' evolution')
    else:
        for i in range(len(xy)):
            plot1.plot(red[xy[i,1],xy[i,0],:], label = 'pixel ' + str(i)) 
        plot1.set_title(red_name + ' evolution')
        
    plot1.legend()        
    plot1.set_aspect('auto')
    plot1.set_xlabel('time')
#     # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_explpix)  
    canvas.draw()
  
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 10)
    
def afiseaza_1pix():
    xy = e1_xy.get().replace(' ','').replace('(','').replace(')','').split(',')
    #print('xy' ,xy)
    xy = np.array(xy).astype(int)
    #print(xy1)
    
    # crearea figurii care va contine graficul semnalului
    fig = Figure(figsize = (6, 4), dpi = 60)

    # adaugarea subgraficului
    plot1 = fig.add_subplot(111)
  
    # afisarea semnaturii temporale
    plot1.plot(red[xy[1],xy[0],:], label = red_name)
    plot1.plot(green[xy[1],xy[0],:], label = green_name)
    plot1.plot(blue[xy[1],xy[0],:], label = blue_name)
    
   
    
    plot1.legend()
    plot1.set_title('pixel evolution')
    plot1.set_aspect('auto')
    plot1.set_xlabel('time')
#     # crearea panzei (canvas) care va contine figura
    canvas = FigureCanvasTkAgg(fig, master = frame_explpix)  
    canvas.draw()
  
    # pozitionarea panzei
    canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 10)
    
    #%% definirea campurilor din interfata

#creare fereastra goala
window1 = tk.Tk()
  
# denumirea interfetei
window1.title('Color Image Cube Visual Exploration')
  
# dimensiunile interfetei
#window1.geometry("500x700")

'''
Crearea celor 3 frame-uri in care se vor face afisarile:
    frame1 incarcarea/afisarea unei singure benzi
        - afisare si harta de culoare si posibilitatea alegerii hartii de culoare folosita
    frame2 crearea imaginii RGB - selectarea oricaror 3 benzi/indici spectrali
    frame3 evolutia temporala pixeli
        - evolutia intensitatii a 4 pixeli la alegere, pe o anumita banda/indice spectral
        sau
        - evolutia intensitatii pe 4 benzi/indici pentru un anumit pixel
'''
screen_width = window1.winfo_screenwidth()
screen_height = window1.winfo_screenheight()

frame_top = tk.Frame(window1)
frame_bottom = tk.Frame(window1)


frame_top.grid(row=0,column = 0)
frame_bottom.grid(row = 1, column = 0)

#%%
frame_load = tk.Frame(frame_top)
frame_load.pack(side = 'left')#.grid(row = 0, column = 0) #.pack(side= 'left')

# frame_cube = tk.Frame(frame_top)
# frame_cube.pack(side='left')#.grid(row = 0, column = 2) #pack(side= 'left')

frame_pix = tk.Frame(frame_top)
frame_pix.pack(side = 'left')#.grid(row = 0, column = 1) #.pack(side= 'left')

frame_explpix = tk.Frame(frame_top)
frame_explpix.pack(side = 'left')#.grid(row = 0, column = 3)
#%%
#!!!! dDaca scriu grid/pack pe acelasi rand are efect diferit fata de cand il scriu pe randuri separate


#frame_explbutton = tk.Frame(frame_bottom).grid(row = 0, column = 0)
frame_expltime = tk.Frame(frame_bottom)
frame_expltime.pack(side = 'left')#.grid(row = 0, column = 0)

frame_explrow = tk.Frame(frame_bottom)
frame_explrow.pack(side = 'left')#.grid(row = 0, column = 1)

frame_explcol = tk.Frame(frame_bottom)
frame_explcol.pack(side = 'left')#.grid(row = 0, column = 2)

frame_cube = tk.Frame(frame_bottom)
frame_cube.pack(side='left')

# frame_explpix = tk.Frame(frame_bottom)
# frame_explpix.pack(side = 'left')#.grid(row = 0, column = 3)

#%%  continutului frame-ului pentru incarcare

rgb_title = tk.Label(frame_load, text = '------- Load Color Data -------')
rgb_title.grid(row = 0, column = 0, columnspan = 6)

#----- red
btn_red = tk.Button(frame_load, text ='Load Red', command = open_red)
btn_red.grid( row = 1, column = 0, columnspan = 2)

t1_red = tk.Text(frame_load, height = 2, width = 30)
t1_red.grid(row = 1, column = 2, columnspan = 3) 

#---- green

btn_green = tk.Button(frame_load, text ='Load Green', command = open_green)
btn_green.grid( row = 2, column = 0, columnspan = 2)

t1_green = tk.Text(frame_load, height = 2, width = 30)
t1_green.grid(row = 2, column = 2, columnspan = 3) 


#---- blue
btn_blue = tk.Button(frame_load, text ='Load Blue', command = open_blue)
btn_blue.grid( row = 3, column = 0, columnspan = 2)


t1_blue = tk.Text(frame_load, height = 2, width = 30)
t1_blue.grid(row = 3, column = 2, columnspan = 3) 


#-- info
btn_info = tk.Button(frame_load, text ='Load info', command = open_info)
btn_info.grid(row = 4, column = 0, columnspan = 2, rowspan = 2)

t3 = tk.Text(frame_load, height = 3, width = 30)
t3.grid(row = 4, column = 2, columnspan = 3, rowspan = 2) 





#%%  continutului frame-ului pentru explorarea in timp

rgb_title = tk.Label(frame_expltime, text = '------- Time Exploration -------')
rgb_title.grid(row = 0, column = 0, columnspan = 6)

w_rgb = tk.Label(frame_expltime, text = 'idx: ')
w_rgb.grid(row = 1, column = 0) 

e1_value_rgb = tk.StringVar()
e1_rgb = tk.Entry(frame_expltime, textvariable = e1_value_rgb, width = 10)
e1_rgb.grid(row = 1, column = 1)  

btn_show_rgb = tk.Button(master = frame_expltime, command = afiseaza_rgb,
                        height = 1, width = 10, text = "Show")
btn_show_rgb.grid(row = 1,column = 2, columnspan = 1)

btn_up_rgb = tk.Button(master = frame_expltime, command = afiseaza_up_rgb,
                        height = 1, width = 10, text = "Up")
btn_up_rgb.grid(row = 1, column = 3, columnspan = 1)

btn_down_rgb = tk.Button(master = frame_expltime, command = afiseaza_down_rgb,
                        height = 1, width = 10, text = "Down")
btn_down_rgb.grid(row = 1, column = 4, columnspan = 1)



#%%  continutului frame-ului pentru explorarea pe linie

#!!! primele linii au mult negru deoarece in primele imagini au doar cativa pixeli diferiti de 0

row_title = tk.Label(frame_explrow, text = '------- Row Exploration -------')
row_title.grid(row = 0, column = 0, columnspan = 6)

w_row = tk.Label(frame_explrow, text = 'idx: ')
w_row.grid(row = 1, column = 0) 

e1_value_row = tk.StringVar()
e1_row = tk.Entry(frame_explrow, textvariable = e1_value_row, width = 10)
e1_row.grid(row = 1, column = 1)  

btn_show_row = tk.Button(master = frame_explrow, command = afiseaza_row,
                        height = 1, width = 10, text = "Show")
btn_show_row.grid(row = 1,column = 2, columnspan = 1)

btn_up_row = tk.Button(master = frame_explrow, command = afiseaza_up_row,
                        height = 1, width = 10, text = "Up")
btn_up_row.grid(row = 1, column = 3, columnspan = 1)

btn_down_row = tk.Button(master = frame_explrow, command = afiseaza_down_row,
                        height = 1, width = 10, text = "Down")
btn_down_row.grid(row = 1, column = 4, columnspan = 1)


#%%  continutului frame-ului pentru explorarea pe coloana

#!!! primele coloane au mult negru deoarece in primele imagini au doar cativa pixeli diferiti de 0

col_title = tk.Label(frame_explcol, text = '------- Column Exploration -------')
col_title.grid(row = 0, column = 0, columnspan = 6)

w_col = tk.Label(frame_explcol, text = 'idx: ')
w_col.grid(row = 1, column = 0) 

e1_value_col = tk.StringVar()
e1_col = tk.Entry(frame_explcol, textvariable = e1_value_col, width = 10)
e1_col.grid(row = 1, column = 1)  

btn_show_col = tk.Button(master = frame_explcol, command = afiseaza_col,
                        height = 1, width = 10, text = "Show")
btn_show_col.grid(row = 1,column = 2, columnspan = 1)

btn_up_col = tk.Button(master = frame_explcol, command = afiseaza_up_col,
                        height = 1, width = 10, text = "Up")
btn_up_col.grid(row = 1, column = 3, columnspan = 1)

btn_down_col = tk.Button(master = frame_explcol, command = afiseaza_down_col,
                        height = 1, width = 10, text = "Down")
btn_down_col.grid(row = 1, column = 4, columnspan = 1)


#%% continute pixul frame-ului pentru evolutia pixelilor


frame_rb = tk.Frame(frame_pix)
frame_1pix = tk.Frame(frame_pix)
frame_4pix = tk.Frame(frame_pix)
frame_rb.pack()
#frame_1pix.pack()
#frame_4pix.pack()

pix_title = tk.Label(frame_rb, text = '------- Pixel temporal values -------')
pix_title.grid(row = 0, column = 0, columnspan = 6)


r = tk.IntVar()
rb1 = tk.Radiobutton(frame_rb, text = '1pix4bands', variable = r, 
                     value = 1, command = clicked )
rb1.grid(row = 1, column = 0)

rb2 = tk.Radiobutton(frame_rb, text = '4pix1band', variable = r, 
                     value = 2, command = clicked )
rb2.grid(row = 1, column = 1)

rb_opt = tk.Label(frame_rb)
rb_opt.grid(row = 2, column = 0, columnspan = 6)

#-----4pixeli

rband = tk.IntVar()
#rband.set(1)
rb_red = tk.Radiobutton(frame_4pix, text = 'Red', variable = rband, 
                        value = 1, command = afiseaza_4pix)
rb_red.grid(row = 2, column = 0)

rb_green = tk.Radiobutton(frame_4pix, text = 'Green', variable = rband, 
                          value = 2, command = afiseaza_4pix)
rb_green.grid(row = 2, column = 1)

rb_blue = tk.Radiobutton(frame_4pix, text = 'Blue', variable = rband, 
                         value = 3, command = afiseaza_4pix)
rb_blue.grid(row = 2, column = 2)


pix1 = tk.Label(frame_4pix, text="Pixel1 (x,y)")
pix1.grid(row = 0, column = 0, columnspan = 1)

e11_xy = tk.StringVar()
pix11_xy = tk.Entry(frame_4pix, textvariable = e11_xy, width = 12)
pix11_xy.grid(row = 0, column = 1)  


pix2 = tk.Label(frame_4pix, text="Pixel2 (x,y)")
pix2.grid(row = 0, column = 2, columnspan = 1)

e2_xy = tk.StringVar()
pix2_xy = tk.Entry(frame_4pix, textvariable = e2_xy, width = 12)
pix2_xy.grid(row = 0, column = 3)  

pix3 = tk.Label(frame_4pix, text="Pixel3 (x,y)")
pix3.grid(row = 1, column = 0, columnspan = 1)

e3_xy = tk.StringVar()
pix3_xy = tk.Entry(frame_4pix, textvariable = e3_xy, width = 12)
pix3_xy.grid(row = 1, column = 1)  


pix4 = tk.Label(frame_4pix, text="Pixel4 (x,y)")
pix4.grid(row = 1, column = 2, columnspan = 1)

e4_xy = tk.StringVar()
pix4_xy = tk.Entry(frame_4pix, textvariable = e4_xy, width = 12)
pix4_xy.grid(row = 1, column = 3) 

btn_4pix = tk.Button(master = frame_4pix, command = afiseaza_4pix,
                        height = 1, width = 10, text = "Show")
btn_4pix.grid(row = 2,column = 3, columnspan = 1) 

#---- 1pixel

pix1 = tk.Label(frame_1pix, text="Pixel1 (x,y)")
pix1.grid(row = 0, column = 0, columnspan = 1)

e1_xy = tk.StringVar()
pix1_xy = tk.Entry(frame_1pix, textvariable = e1_xy, width = 12)
pix1_xy.grid(row = 0, column = 2)  

btn_1pix = tk.Button(master = frame_1pix, command = afiseaza_1pix,
                        height = 1, width = 10, text = "Show")
btn_1pix.grid(row = 2,column = 0, columnspan = 5) 


window1.mainloop()