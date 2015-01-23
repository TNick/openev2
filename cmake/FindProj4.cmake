# - Try to find proj4 library
# Once done this will define
#  PROJ4_FOUND - System has PROJ4
#  PROJ4_INCLUDE_DIRS - The PROJ4 include directories
#  PROJ4_LIBRARIES - The libraries needed to use PROJ4
#  PROJ4_DEFINITIONS - Compiler switches required for using PROJ4
#  PROJ4_DLLS - Dinamic Link Libraries that are needed by an executable

find_package(PkgConfig QUIET)
pkg_check_modules(PC_PROJ4 QUIET proj4)
set(PROJ4_DEFINITIONS ${PC_PROJ4_CFLAGS_OTHER})

find_path(PROJ4_INCLUDE_DIR proj_api.h
          HINTS ${PC_PROJ4_INCLUDEDIR} ${PC_PROJ4_INCLUDE_DIRS} 
          PATHS ENV PROJ4_INC )

find_library(PROJ4_LIBRARY NAMES proj proj_i
             HINTS ${PC_PROJ4_LIBDIR} ${PC_PROJ4_LIBRARY_DIRS} 
             PATHS ENV PROJ4_BINARY )

find_file(PROJ4_DLL proj.dll
          PATHS 
			${PROJ4_INCLUDE_DIR}/../bin
			${PROJ4_INCLUDE_DIR}/../../bin)
			 
set (PROJ4_DEBUG_VARIABLES ON)
if (PROJ4_DEBUG_VARIABLES)
	message (STATUS "PROJ4_INCLUDE_DIR = ${PROJ4_INCLUDE_DIR}")
	message (STATUS "PROJ4_LIBRARY = ${PROJ4_LIBRARY}")
	message (STATUS "PROJ4_DLL = ${PROJ4_DLL}")
endif (PROJ4_DEBUG_VARIABLES)
		 
set(PROJ4_LIBRARIES ${PROJ4_LIBRARY} )
set(PROJ4_INCLUDE_DIRS ${PROJ4_INCLUDE_DIR} )
set(PROJ4_DLLS ${PROJ4_DLL} )

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
	PROJ4 DEFAULT_MSG
    PROJ4_LIBRARY PROJ4_INCLUDE_DIR PROJ4_DLL)

mark_as_advanced(PROJ4_INCLUDE_DIR PROJ4_LIBRARY)
