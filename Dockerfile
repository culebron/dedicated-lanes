FROM ubuntu:18.04
MAINTAINER Dmitri Lebedev <dl@peshemove.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt update \
	&& apt install -y --no-install-recommends \
	build-essential \
	libspatialindex-dev \
	libgdal-dev \
	libgeos-dev \
	locales \
	python3-pip \
	python3-dev \
	python3.6-dev \
	python3-setuptools \
	unzip \
	wget

RUN pip3 install wheel

RUN ldconfig && pip3 install -U \
	argh \
	decorator \
	fastkml \
	geojson \
	geopandas \
	Jinja2 \
	lxml \
	polyline \
	psycopg2 \
	pyproj \
	requests_cache \
	rtree \
	shapely

RUN ldconfig && pip3 install -U \
	ipdb

RUN mkdir /calc /aqtash
COPY calc /calc

RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN echo "cd calc && python3 main.py" > /make-rating.sh
RUN echo "cd calc && python3.6 render.py html/index.template.html build/bus-lanes.geojson build/bus-lanes.csv build/index.html" > /render.sh

COPY aqtash /aqtash
RUN cd aqtash && python3 setup.py install
