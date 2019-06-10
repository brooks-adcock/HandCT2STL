import urllib.request


data_sets = {
	"Shoulder": {
		min: 1051,
		max: 1500
	},
	"Pelvis": {
		'min': 901,
		'max': 1050
	}
}
url = "https://mri.radiology.uiowa.edu/VHDicom/VHFCT1mm/%(dataset)s/vhf.%(index)s.dcm"

dataset = "Pelvis"

for index in range(data_sets[dataset]['min'], data_sets[dataset]['max']+1):
	print("Downloading %s" % index)
	str_obj = {
		'dataset': dataset,
		'index': index
	}
	urllib.request.urlretrieve(url % str_obj, "./VisibleHuman/vhf.%(index)s.dcm" % str_obj)
