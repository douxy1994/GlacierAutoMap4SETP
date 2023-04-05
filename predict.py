import numpy as np
from osgeo import gdal
import pickle

def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "failed")
    return dataset


def writeTiff(im_data, im_geotrans, im_proj, path):
    global im_width, im_height, im_bands
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset

model_path =  r"E:\StudyCareer\Tibetan_Plateau\SETP\Data4RF\SC_SETP2_10.pickle"
Landset_Path = r"E:\StudyCareer\Tibetan_Plateau\SETP\RunImage\Slack_2.tif"
SavePath = r"E:\StudyCareer\Tibetan_Plateau\SETP\result_RF\SC_2.tif"

dataset = readTif(Landset_Path)
Tif_width = dataset.RasterXSize
Tif_height = dataset.RasterYSize
Tif_geotrans = dataset.GetGeoTransform()
Tif_proj = dataset.GetProjection()
Landset_data = dataset.ReadAsArray(0, 0, Tif_width, Tif_height)

print(Landset_data.shape[0], Landset_data.shape[1] * Landset_data.shape[2])
file = open(model_path, "rb")
model = pickle.load(file)
file.close()
data = np.zeros((Landset_data.shape[0], Landset_data.shape[1] * Landset_data.shape[2]))

for i in range(Landset_data.shape[0]):
    data[i] = Landset_data[i].flatten()
data = data.swapaxes(0, 1)

print(data)
print(data.shape)
pred = model.predict(data)


pred = pred.reshape(Landset_data.shape[1], Landset_data.shape[2]) * 255

pred = pred.astype(np.uint8)

pred = pred.astype(np.uint8)
writeTiff(pred, Tif_geotrans, Tif_proj, SavePath)