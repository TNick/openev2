# - Try to find GDAL library
# Once done this will define
#  GDAL_FOUND - System has GDAL
#  GDAL_INCLUDE_DIRS - The GDAL include directories
#  GDAL_LIBRARIES - The libraries needed to use GDAL
#  GDAL_DLLS - Dinamic Link Libraries that are needed by an executable
#  GDAL_BINARY_DIR - location of the bin directory for gdal
#  GDAL_DEFINITIONS - Compiler switches required for using GDAL
#
#    References:
#        http://svn.osgeo.org/qgis/trunk/qgis/cmake/FindGDAL.cmake
#
include(FindPackageHandleStandardArgs)

find_package(PkgConfig QUIET)
pkg_check_modules(PC_GDAL QUIET gdal)
set (GDAL_DEFINITIONS ${PC_GDAL_CFLAGS_OTHER})

find_path(
    GDAL_INCLUDE_DIR gdal.h
    HINTS ${PC_GDAL_INCLUDEDIR} ${PC_GDAL_INCLUDE_DIRS} 
    PATH_SUFFIXES gdal)

find_library(
    GDAL_LIBRARY NAMES GDal_1_11_0 gdal_i gdal
    HINTS ${PC_GDAL_LIBDIR} ${PC_GDAL_LIBRARY_DIRS} )

find_path(
    GDAL_BINARY_DIR GDal_1_11_0.dll gdal.dll
    PATHS
        "${GDAL_INCLUDE_DIR}/../bin"
        "${GDAL_INCLUDE_DIR}/../../bin")

find_file(
    GDAL_DLL NAMES GDal_1_11_0.dll gdal.dll
    PATHS "${GDAL_BINARY_DIR}")

find_package(PROJ4 QUIET)
find_package(ECW QUIET)

find_file (HDF5_DLL NAMES hdf5.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (EXPAT_DLL NAMES libexpat.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (SPATIALITE_DLL NAMES spatialite.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (GEOS_C_DLL NAMES geos_c.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (GEOS_DLL NAMES geos.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (ICONV_DLL NAMES iconv.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (SZIP_DLL NAMES szip.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
find_file (PROJ4_DLLS NAMES proj.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)
#find_file (ECW_DLLS NAMES NCSEcw.dll PATHS "${GDAL_BINARY_DIR}" PATH_SUFFIXES bin)


find_path(
    GDAL_PROJ_SHARE_DIR nad.lst
    PATH_SUFFIXES
        proj/share
        share/proj
        bin/proj/share
        lib/proj/share)

get_filename_component (GDAL_GUESSED_PLUGINS_DIR ${GDAL_LIBRARY} PATH)
set (OGR_GUESSED_PLUGINS_DIR "${GDAL_GUESSED_PLUGINS_DIR}/ogr-plugins")
set (GDAL_GUESSED_PLUGINS_DIR "${GDAL_GUESSED_PLUGINS_DIR}/gdal-plugins")

find_path(
    GDAL_PLUGINS_DIR
    NAMES
        gdal_ECW_JP2ECW.dll
        libgdal_ECW_JP2ECW.so
    PATHS ${GDAL_GUESSED_PLUGINS_DIR}
    PATH_SUFFIXES
        lib/gdal-plugins)

find_path(
    OGR_PLUGINS_DIR
    NAMES
        ogr-placeholder.dll
        libogr-placeholder.so
    PATHS ${OGR_GUESSED_PLUGINS_DIR}
    PATH_SUFFIXES
        lib/gdal-plugins)

find_path(
    GDAL_DATA_DIR
    NAMES
        gcs.csv
        datum_shift.csv
    PATHS ${OGR_GUESSED_PLUGINS_DIR}
    PATH_SUFFIXES
        gdal-data
        share/gdal-data
        bin/gdal-data)


# file(GLOB GDAL_DLLS "${GDAL_BINARY_PATH}/*.dll")
file(GLOB GDAL_DATA "${GDAL_DATA_DIR}/*")
file(GLOB GDAL_PLUGINS "${GDAL_PLUGINS_DIR}/*.dll")
file(GLOB GDAL_OGR_PLUGINS "${OGR_PLUGINS_DIR}/*.dll")
file(GLOB GDAL_PROJ "${GDAL_PROJ_SHARE_DIR}/*")

set (GDAL_DEBUG_VARIABLES ON)
if (GDAL_DEBUG_VARIABLES)
    message (STATUS "GDAL_INCLUDE_DIR = ${GDAL_INCLUDE_DIR}")
    message (STATUS "GDAL_LIBRARY = ${GDAL_LIBRARY}")
    message (STATUS "GDAL_BINARY_DIR = ${GDAL_BINARY_DIR}")
    message (STATUS "GDAL_DLL = ${GDAL_DLL}")
    message (STATUS "HDF5_DLL = ${HDF5_DLL}")
    message (STATUS "EXPAT_DLL = ${EXPAT_DLL}")
    message (STATUS "SPATIALITE_DLL = ${SPATIALITE_DLL}")
    message (STATUS "GDAL_PROJ_SHARE_DIR = ${GDAL_PROJ_SHARE_DIR}")
    message (STATUS "GDAL_GUESSED_PLUGINS_DIR = ${GDAL_GUESSED_PLUGINS_DIR}")
    message (STATUS "GDAL_PLUGINS_DIR = ${GDAL_PLUGINS_DIR}")
    message (STATUS "OGR_GUESSED_PLUGINS_DIR = ${OGR_GUESSED_PLUGINS_DIR}")
    message (STATUS "OGR_PLUGINS_DIR = ${OGR_PLUGINS_DIR}")
    message (STATUS "GDAL_DATA_DIR = ${GDAL_DATA_DIR}")
    message (STATUS "ECW_DLLS = ${ECW_DLLS}")
endif (GDAL_DEBUG_VARIABLES)

set(GDAL_LIBRARIES ${GDAL_LIBRARY} )
set(GDAL_INCLUDE_DIRS ${GDAL_INCLUDE_DIR} )
set(GDAL_DLLS
    ${GDAL_DLL}
    ${HDF5_DLL}
    ${EXPAT_DLL}
    ${SPATIALITE_DLL}
    ${GEOS_C_DLL}
    ${GEOS_DLL}
    ${ICONV_DLL}
    ${SZIP_DLL}
    ${PROJ4_DLLS}
    ${ECW_DLLS})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
    GDAL DEFAULT_MSG
    GDAL_LIBRARY GDAL_INCLUDE_DIR)

mark_as_advanced(GDAL_INCLUDE_DIR GDAL_LIBRARY GDAL_DLL)
