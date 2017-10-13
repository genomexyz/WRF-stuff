#!/bin/bash

sudo apt update
sudo apt install gcc g++ m4 csh openjdk-7-jre gfortran unzip

#setting WRF
export DIR=~/WRF/LIBRARIES
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS=-m64
export F77=gfortran
export FFLAGS=-m64
export PATH=$DIR/netcdf/bin:$PATH
export NETCDF=$DIR/netcdf
export PATH=$DIR/mpich/bin:$PATH
export LDFLAGS=-L$DIR/grib2/lib
export CPPFLAGS=-I$DIR/grib2/include
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include


#install netcdf
tar xzvf netcdf-4.1.3.tar.gz     #or just .tar if no .gz present
cd netcdf-4.1.3
./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared
make
make install
cd ..

#install mpich
tar xzvf mpich-3.0.4.tar.gz     #or just .tar if no .gz present
cd mpich-3.0.4
./configure --prefix=$DIR/mpich
make
make install
cd ..

#install zlib
tar xzvf zlib-1.2.7.tar.gz     #or just .tar if no .gz present
cd zlib-1.2.7
./configure --prefix=$DIR/grib2
make
make install
cd ..

#install libpng
tar xzvf libpng-1.2.50.tar.gz     #or just .tar if no .gz present
cd libpng-1.2.50
./configure --prefix=$DIR/grib2
make
make install
cd ..

#install jasper
tar xzvf jasper-1.900.1.tar.gz     #or just .tar if no .gz present
cd jasper-1.900.1
./configure --prefix=$DIR/grib2
make
make install
cd ..

#install WRF
gunzip WRFV3.8.TAR.gz
tar -xf WRFV3.8.TAR
cd WRFV3
./configure
./compile em_real
cd ..

#install WPS
gunzip WPSV3.8.TAR.gz
tar -xf WPSV3.8.TAR
cd WPS
./clean
./configure
./compile
cd ..

#install WRFDomainWizard
unzip WRFDomainWizard.zip -d WRFDomainWizard
cd WRFDomainWizard
sudo chmod 777 run_DomainWizard

#extract geog
tar xvjf geog_complete.tar.bz2

#install WRFDA
tar xfvz WRFDA_V3.7.1.tar.gz
cd WRFDA
./configure wrfda
./compile all_wrfvar

#save all setting
echo '#setting WRF' >> ~/.bashrc
echo 'export DIR=~/WRF/LIBRARIES' >> ~/.bashrc
echo 'export CC=gcc' >> ~/.bashrc
echo 'export CXX=g++' >> ~/.bashrc
echo 'export FC=gfortran' >> ~/.bashrc
echo 'export FCFLAGS=-m64' >> ~/.bashrc
echo 'export F77=gfortran' >> ~/.bashrc
echo 'export FFLAGS=-m64' >> ~/.bashrc
echo 'export PATH=$DIR/netcdf/bin:$PATH' >> ~/.bashrc
echo 'export NETCDF=$DIR/netcdf' >> ~/.bashrc
echo 'export PATH=$DIR/mpich/bin:$PATH' >> ~/.bashrc
echo 'export LDFLAGS=-L$DIR/grib2/lib' >> ~/.bashrc
echo 'export CPPFLAGS=-I$DIR/grib2/include' >> ~/.bashrc
echo 'export JASPERLIB=$DIR/grib2/lib' >> ~/.bashrc
echo 'export JASPERINC=$DIR/grib2/include' >> ~/.bashrc
