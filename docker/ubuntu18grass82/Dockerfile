ARG UBUNTU_VERSION=18.04
FROM ubuntu:${UBUNTU_VERSION}

ENV LIBK4_VERSION=1.4.1
ENV ARCH=amd64
ENV NUMCORES=18
ENV PCL_VERSION=1.11.1
ENV XERCES_VERSION=3.2.3
ENV LIBGEOTIFF_VERSION=1.7.1
ENV PROJ_VERSION=9.1.0
ENV GEOS_VERSION=3.9.3
ENV GDAL_VERSION=3.5.2
ENV PDAL_VERSION=2.4.2
ENV GRASS_VERSION=8.2.0
ENV TL_VERSION=1.2.0

# Set the working directory to /app
WORKDIR /app

ADD setup-ubuntu.sh /app
ADD sources.list /app

# Tell Ubuntu non-interactive install
ARG DEBIAN_FRONTEND=noninteractive

RUN bash setup-ubuntu.sh ${ARCH}

RUN apt update
RUN apt install -y ca-certificates
RUN update-ca-certificates
RUN mkdir /tmp/src

# set python3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 #\
	# && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# install Azure Kinect SDK
RUN apt install git -y
RUN git clone https://github.com/microsoft/Azure-Kinect-Sensor-SDK.git
RUN cd Azure-Kinect-Sensor-SDK && mkdir build && cd build && cmake ..
RUN cd Azure-Kinect-Sensor-SDK && \
	cd build && \
	make -j$NUMCORES
RUN cd Azure-Kinect-Sensor-SDK && \
	cd build && \
	make install

# install libk4
RUN apt install curl libcurl4-openssl-dev -y
RUN curl -sSL https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4/libk4a1.4_${LIBK4_VERSION}_${ARCH}.deb > /tmp/src/libk4a1.4_${LIBK4_VERSION}_${ARCH}.deb
RUN curl -sSL https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4-dev/libk4a1.4-dev_${LIBK4_VERSION}_${ARCH}.deb > /tmp/src/libk4a1.4-dev_${LIBK4_VERSION}_${ARCH}.deb
RUN ACCEPT_EULA=Y dpkg -i /tmp/src/libk4a1.4_${LIBK4_VERSION}_${ARCH}.deb
RUN dpkg -i /tmp/src/libk4a1.4-dev_${LIBK4_VERSION}_${ARCH}.deb

ENV LD_LIBRARY_PATH=/usr/local/lib/:/usr/lib/x86_64-linux-gnu/libk4a1.4/:$LD_LIBRARY_PATH

# install PCL
RUN apt install libboost-all-dev libeigen3-dev libflann-dev -y
RUN git clone --depth=1 --branch pcl-$PCL_VERSION https://github.com/PointCloudLibrary/pcl.git /tmp/src/pcl
RUN cd /tmp/src/pcl && \
	mkdir build && \
	cd build && \
	cmake -DCMAKE_BUILD_TYPE=Release .. && \
    	make -j$NUMCORES && \
    	make install

# install Blender and download BlenderGIS addon
RUN apt install blender -y
RUN wget https://github.com/domlysz/BlenderGIS/archive/refs/tags/228.zip -P /blender_gis/

# install PROJ
RUN apt install -y sqlite3 libsqlite3-dev
RUN cd /tmp/src && \
    wget https://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz && \
    tar -zvxf proj-${PROJ_VERSION}.tar.gz && \
    cd proj-${PROJ_VERSION} && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . && \
    cmake --build . --target install

# install xerces
RUN apt install -y m4 automake
RUN cd /tmp/src && \
    wget https://github.com/apache/xerces-c/archive/v${XERCES_VERSION}.tar.gz -O xerces-c-${XERCES_VERSION}.tar.gz && \
    tar -zxvf xerces-c-${XERCES_VERSION}.tar.gz && \
    cd xerces-c-${XERCES_VERSION} && \
    ./reconf && \
    ./configure && \
    make -j${CPU_NR} && \
    make install

# install geotiff
RUN cd /tmp/src && \
    wget -q https://github.com/OSGeo/libgeotiff/releases/download/${LIBGEOTIFF_VERSION}/libgeotiff-${LIBGEOTIFF_VERSION}.tar.gz && \
    tar -xzf libgeotiff-${LIBGEOTIFF_VERSION}.tar.gz && \
    cd libgeotiff-${LIBGEOTIFF_VERSION} && \
    ./configure --prefix=/usr/local --with-libtiff=/usr/local && \
    make -j${CPU_NR} && \
    make install

# install geos
RUN cd /tmp/src && \
    wget http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 && \
    bunzip2 geos-${GEOS_VERSION}.tar.bz2 && \
    tar xvf  geos-${GEOS_VERSION}.tar && \
    cd geos-${GEOS_VERSION} && \
    ./configure && \
    make -j${CPU_NR} && \
    make install

# install GDAL
RUN apt install -y python3-setuptools
RUN cd /tmp/src && \
    wget http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar -zvxf gdal-${GDAL_VERSION}.tar.gz && \
    cd gdal-${GDAL_VERSION} && \
    ./configure --prefix=/usr/local --with-threads \
    --with-libtiff=/usr/local --with-geotiff=/usr/local --with-jpeg=internal --with-sqlite3 \
    --with-gif=internal --with-png=internal --with-libz=/usr --with-python -with-proj=/usr/local \
    --with-xerces --with-geos --with-curl=/usr/bin/curl-config && \
    make -j${CPU_NR} && \
    make install && \
    ldconfig

# install PDAL
RUN apt install -y unzip
ENV PDAL_VERSION=2.3.0
RUN cd /tmp/src && \
	wget https://github.com/PDAL/PDAL/archive/refs/tags/${PDAL_VERSION}.zip && \
	unzip -x ${PDAL_VERSION} && \
	cd PDAL-${PDAL_VERSION} && \
	mkdir build && \
	cd build && \
	cmake -DGDAL_CONFIG=/usr/local/bin/gdal-config -G Ninja .. && \
	ninja && \
	ninja install


# install GRASS
RUN apt install \
	build-essential \
	flex make bison ccache \
	python3 python3-dev \
	python3-opengl \
	python-wxversion python-wxtools python-wxgtk3.0 python3-wxgtk4.0 \
	python3-dateutil libgsl-dev python3-numpy \
	wx3.0-headers wx-common libwxgtk3.0-dev \
	libwxbase3.0-dev   \
	libncurses5-dev \
	libbz2-dev \
	zlib1g-dev gettext \
	libpnglite-dev \
	libcairo2-dev \
	libpq-dev \
	libreadline6-dev libfreetype6-dev \
	libfftw3-3 libfftw3-dev \
	# liblas-c-dev \
	subversion libzstd-dev \
	checkinstall \
	libglu1-mesa-dev libxmu-dev \
	ghostscript wget \
	-y
RUN cd /tmp/src && \
	wget https://github.com/OSGeo/grass/archive/refs/tags/${GRASS_VERSION}.zip && \
	unzip -x ${GRASS_VERSION}.zip
RUN cd /tmp/src/grass-${GRASS_VERSION} && \
	MYCFLAGS='-O2 -fPIC -fno-common -fexceptions -std=gnu99 -fstack-protector -m64' && \
	MYLDFLAGS='-Wl,--no-undefined -Wl,-z,now' && \
	LDFLAGS="$MYLDFLAGS" CFLAGS="$MYCFLAGS" CXXFLAGS="$MYCXXFLAGS" ./configure \
		--with-cxx \
		--enable-largefile \
		# --with-proj --with-proj-share=/usr/share/proj \
		--with-proj --with-proj-share=/usr/share/proj --with-proj-libs=/usr/local/lib \
		--with-gdal=/usr/local/bin/gdal-config \
		--with-python \
		--with-geos \
		--with-sqlite \
		--with-nls \
		--with-zstd \
		# --with-liblas \
		--with-pdal \
		--with-cairo --with-cairo-ldflags=-lfontconfig \
		--with-freetype=yes --with-freetype-includes="/usr/include/freetype2/" \
		--with-wxwidgets \
		--with-fftw \
		--with-motif \
		--with-opengl-libs=/usr/include/GL \
		--with-postgres=yes --with-postgres-includes="/usr/include/postgresql" \
		--without-netcdf \
		--without-mysql \
		--without-odbc \
		--without-openmp \
		--without-ffmpeg && \
	make -j$NUMCORES && \
	make install

# install Tangible Python dependencies
RUN apt install -y python3-pip
RUN pip3 install watchdog

# install Tangible Landscape
RUN cd /tmp/src && \
	wget https://github.com/tangible-landscape/grass-tangible-landscape/archive/refs/tags/v${TL_VERSION}.zip && \
	unzip -x v${TL_VERSION}.zip && \
	cd grass-tangible-landscape-${TL_VERSION} && \
	make MODULE_TOPDIR=../grass-${GRASS_VERSION} && \
	make install MODULE_TOPDIR=../grass-${GRASS_VERSION}

# install r.in.kinect (official packages currently not working -> git clone)
RUN cd /tmp/src && \
	git clone --single-branch --branch k4a https://github.com/tangible-landscape/r.in.kinect.git && \
	cd r.in.kinect && \
	make MODULE_TOPDIR=../grass-${GRASS_VERSION} && \
	make install MODULE_TOPDIR=../grass-${GRASS_VERSION}
