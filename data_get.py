from osgeo import gdal
import os
import random

def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "failed")
    return dataset


Landset_Path = "/data.tif"
LabelPath = "/label.tif"
txt_Path = "/data.csv"

dataset = readTif(Landset_Path)
Tif_width = dataset.RasterXSize
Tif_height = dataset.RasterYSize
Tif_bands = dataset.RasterCount
Tif_geotrans = dataset.GetGeoTransform()
Landset_data = dataset.ReadAsArray(0, 0, Tif_width, Tif_height)
dataset = readTif(LabelPath)
Tif_width = dataset.RasterXSize
Tif_height = dataset.RasterYSize
Tif_bands = dataset.RasterCount
Tif_geotrans = dataset.GetGeoTransform()
Label_data = dataset.ReadAsArray(0, 0, Tif_width, Tif_height)



if os.path.exists(txt_Path):
    os.remove(txt_Path)

file_write_obj = open(txt_Path, 'w')

count = 0
for i in range(Label_data.shape[0]):
    for j in range(Label_data.shape[1]):

        if (Label_data[i][j] == 1):
            var = ""
            for k in range(Landset_data.shape[0]):
                var = var + str(Landset_data[k][i][j]) + ","
            var = var + "yes"
            file_write_obj.writelines(var)
            file_write_obj.write('\n')
            count = count + 1

Threshold = count
count = 0
for i in range(10000000):
    X_random = random.randint(0, Label_data.shape[0] - 1)
    Y_random = random.randint(0, Label_data.shape[1] - 1)
    if (Label_data[X_random][Y_random] == 0):
        var = ""
        for k in range(Landset_data.shape[0]):
            var = var + str(Landset_data[k][X_random][Y_random]) + ","
        var = var + "no"
        file_write_obj.writelines(var)
        file_write_obj.write('\n')
        count = count + 1
    if (count == Threshold):
        break

file_write_obj.close()