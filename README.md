# SITSVisualization

This graphical user interface for SITS visualization was written using the following Python libraries: python=3.11, matplotlib=3.7, pandas=1.5, scipy, rasterio, tkinter, and spyder.

This is the code for the prototype of the Python GUI described in _A. Griparis et al., "Visual exploration of satellite image time series," IGARSS 2023 - 2023 IEEE International Geoscience and Remote Sensing Symposium, Pasadena, USA, 2023_.

It is entirely implemented in Tkinter, the standard Python interface to the Tcl/Tk GUI toolkit, and, it includes four areas:
- the first one serves the data loading
- the second one is for choosing the temporal evolution
- displayed in the third area, while
- the fourth area enables visual exploration of the loaded SITS on each of the three axes of the related data cube (time, rows, and columns /spatial coordinates).

In the data loading area, the user can load three grey level SITS with dimensions Rows × Columns × Time, and SITS metadata including the acquisition date of each image. The file format for the loaded SITS can be _.npy_, _.mat_, and _.tif_, while _.csv_ and _.pkl_ are used for metadata.

Displaying the images requires loading the series related to each band.

The _.mat_ file must have version v4 and contain only one array variable.

The header for the _.csv_ and _.pkl_ files must be: name, day, month, year. 

__If you use this code, please cite our paper:__
-  _A. Griparis, A. Radoi, D. Faur, M. Datcu., "Visual exploration of satellite image time series," IGARSS 2023 - 2023 IEEE International Geoscience and Remote Sensing Symposium, Pasadena, USA, 2023_
