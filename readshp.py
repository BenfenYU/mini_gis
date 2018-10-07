import os
from osgeo import ogr

daShapefile = r"./sh.shp"

driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(daShapefile, 0) # 0 means read-only. 1 means writeable.
print(dataSource)

# Check to see if shapefile is found.
if dataSource is None:
    print( 'Could not open %s',(daShapefile))
else:
    print ('Opened %s',(daShapefile))
    layer = dataSource.GetLayer()
    featureCount = layer.GetFeatureCount()
    print("Number of features in %s: %d",(os.path.basename(daShapefile),featureCount))
