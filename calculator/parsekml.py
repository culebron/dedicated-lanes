
import geolib
import geopandas as gpd
from fastkml import kml

@geolib.autoargs
def main(kmlfile, outfile):
	k = kml.KML()
	# open & encoding - для декодирования файлов при открытии, потому что в системе по умолчанию может стоять кодировка ascii
	with open(kmlfile, encoding='utf-8') as f:
		# а плагин сам ещё раскодирует utf-8, поэтому закодировать обратно
		k.from_string(f.read().encode('utf-8'))

	data = []
	for f in list(k.features())[0].features():
		if f.name == 'односторонние сущ.':
			for f2 in f.features():
				data.append({'lanes': 1, 'geometry': f2.geometry})

		if f.name == 'двусторонние сущ.':
			for f2 in f.features():
				data.append({'lanes': 2, 'geometry': f2.geometry})

	return gpd.GeoDataFrame(data)
