# coding: utf-8

import geopandas as gpd
import geolib


@geolib.autoargs
def do(df_left: gpd.GeoDataFrame, df_right: gpd.GeoDataFrame, left_on=None, right_on=None, columns=None, how='inner'):
	joined_df = df_left.merge(df_right, left_on=left_on, right_on=right_on)

	if columns:
		cnames = [cname.split(':') for cname in columns.split(';')]
		subset = [c[0] for c in cnames]
		rename = dict(c for c in cnames if len(c) == 2)

		joined_df = joined_df[subset]
		joined_df.rename(columns=rename, inplace=True)

	return joined_df
