# - Try to find geos library
# Once done this will define
#  GEOS_FOUND - System has GEOS
#  GEOS_INCLUDE_DIRS - The GEOS include directories
#  GEOS_LIBRARIES - The libraries needed to use GEOS
#  GEOS_DEFINITIONS - Compiler switches required for using GEOS

find_package(PkgConfig QUIET)
pkg_check_modules(PC_GEOS QUIET geos)
set(GEOS_DEFINITIONS ${PC_GEOS_CFLAGS_OTHER})

find_path(GEOS_INCLUDE_DIR geos_c.h
          HINTS ${PC_GEOS_INCLUDEDIR} ${PC_GEOS_INCLUDE_DIRS} 
          PATHS ENV GEOS_INC
          PATH_SUFFIXES geos )

find_library(GEOS_C_LIBRARY NAMES geos_c
             HINTS ${PC_GEOS_LIBDIR} ${PC_GEOS_LIBRARY_DIRS} 
             PATHS ENV GEOS_BINARY )

find_library(GEOS_LIBRARY NAMES geos
             HINTS ${PC_GEOS_LIBDIR} ${PC_GEOS_LIBRARY_DIRS} 
             PATHS ENV GEOS_BINARY )

#find_library(GEOS_L_LIBRARY NAMES libgeos
#             HINTS ${PC_GEOS_LIBDIR} ${PC_GEOS_LIBRARY_DIRS} 
#             PATHS ENV GEOS_BINARY )
			 
set(GEOS_LIBRARIES ${GEOS_C_LIBRARY} ${GEOS_LIBRARY} )
set(GEOS_INCLUDE_DIRS ${GEOS_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set GEOS_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(GEOS  DEFAULT_MSG
                                  GEOS_LIBRARY GEOS_C_LIBRARY GEOS_INCLUDE_DIR)

mark_as_advanced(GEOS_INCLUDE_DIR GEOS_LIBRARY GEOS_C_LIBRARY)

