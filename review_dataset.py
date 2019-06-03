import vtk
from vtk.util import numpy_support
import numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


def getNumpyArrayFromDataset(path):

	reader = vtk.vtkDICOMImageReader()
	reader.SetDirectoryName(path)
	reader.Update()

	# Load dimensions using `GetDataExtent`
	_extent = reader.GetDataExtent()
	const_pixel_dims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
	print(const_pixel_dims)

	# Load spacing values
	ConstPixelSpacing = reader.GetPixelSpacing()

	threshold = vtk.vtkImageThreshold()
	threshold.SetInputConnection(reader.GetOutputPort())
	threshold.ThresholdByLower(400)  # remove all soft tissue
	threshold.ReplaceInOn()
	threshold.SetInValue(0)  # set all values below 400 to 0
	threshold.ReplaceOutOn()
	threshold.SetOutValue(1)  # set all values above 400 to 1
	threshold.Update()

	# Get the 'vtkImageData' object from the reader
	vtk_image_data = threshold.GetOutput()
	#vtk_image_data = reader.GetOutput()

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


path = "./Dataset/"

numpy_data, const_pixel_dims = getNumpyArrayFromDataset(path)


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
l = plt.imshow(numpy_data[:, 200, :])

axcolor = 'lightgoldenrodyellow'
ax_slice_slider = plt.axes([0.25, 0.1, 0.5, 0.03], facecolor=axcolor)

slice_slider = Slider(ax_slice_slider, 'Slice #', 0, const_pixel_dims[1]-1, valinit=0, valstep=1)


def update(val):
	slice_index = slice_slider.val
	print("Update %s" % slice_index)
	l.set_data(numpy_data[:, int(slice_index), :])
	fig.canvas.draw_idle()

slice_slider.on_changed(update)

ax_colorbar = plt.axes([0.75, 0.25, 0.05, 0.5], facecolor=axcolor)
plt.colorbar(cax=ax_colorbar)
plt.show()


