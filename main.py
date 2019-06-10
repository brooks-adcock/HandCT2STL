import vtk
from vtk.util import numpy_support


def getNumpyArrayFromDataset(path):



	# Load dimensions using `GetDataExtent`
	_extent = reader.GetDataExtent()
	const_pixel_dims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
	print(const_pixel_dims)

	# Load spacing values
	ConstPixelSpacing = reader.GetPixelSpacing()

	# Get the 'vtkImageData' object from the reader
	vtk_image_data = reader.GetOutput()

	# Get the 'vtkPointData' object from the 'vtkImageData' object
	vtk_point_data = vtk_image_data.GetPointData()

	# Ensure that only one array exists within the 'vtkPointData' object
	assert (vtk_point_data.GetNumberOfArrays()==1)

	# Get the `vtkArray` (or whatever derived type) which is needed for the `numpy_support.vtk_to_numpy` function
	array_data = vtk_point_data.GetArray(0)

	# Convert the `vtkArray` to a NumPy array
	numpy_array = numpy_support.vtk_to_numpy(array_data)

	# Reshape the NumPy array to 3D using 'ConstPixelDims' as a 'shape'
	numpy_array = numpy_array.reshape(const_pixel_dims, order='F')

	return numpy_array, const_pixel_dims

threshold = 400

path = "./VisibleHuman/"
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(path)
reader.Update()

vtk_voi = vtk.vtkExtractVOI()
vtk_voi.SetInputConnection(reader.GetOutputPort())
vtk_voi.SetVOI(312, 511, 168, 432, 0, 598)
vtk_voi.Update()

vtk_threshold = vtk.vtkImageThreshold ()
vtk_threshold.SetInputConnection(vtk_voi.GetOutputPort())
vtk_threshold.ThresholdByLower(threshold)  # remove all soft tissue
vtk_threshold.ReplaceInOn()
vtk_threshold.SetInValue(0)  # set all values below 400 to 0
vtk_threshold.ReplaceOutOn()
vtk_threshold.SetOutValue(1)  # set all values above 400 to 1
vtk_threshold.Update()

dmc = vtk.vtkDiscreteMarchingCubes()
dmc.SetInputConnection(vtk_threshold.GetOutputPort())
dmc.GenerateValues(2, 1, 3)
dmc.Update()

#smooth = vtk.vtkSmoothPolyDataFilter()
#smooth.SetInputData(dmc.GetOutput())
#smooth.SetRelaxationFactor(0.001)
#smooth.SetNumberOfIterations(1)

# Write the stl file to disk
stlWriter = vtk.vtkSTLWriter()
stlWriter.SetFileName("arm.stl")
stlWriter.SetInputConnection(dmc.GetOutputPort())
stlWriter.Write()