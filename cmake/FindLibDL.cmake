# - Try to find LibDL library
# Once done this will define
#  LIBDL_FOUND - System has LibDL
#  LIBDL_INCLUDE_DIRS - The LibDL include directories
#  LIBDL_LIBRARIES - The libraries needed to use LibDL
#  LIBDL_DEFINITIONS - Compiler switches required for using LibDL

find_package(PkgConfig QUIET)
pkg_check_modules(PC_LIBDL QUIET LibDL)
set(LIBDL_DEFINITIONS ${PC_LIBDL_CFLAGS_OTHER})

find_path(LIBDL_INCLUDE_DIR libdl.h
          HINTS ${PC_LIBDL_INCLUDEDIR} ${PC_LIBDL_INCLUDE_DIRS})

find_library(LIBDL_LIBRARY NAMES dl
             HINTS ${PC_LIBDL_LIBDIR} ${PC_LIBDL_LIBRARY_DIRS})

set(LIBDL_LIBRARIES ${LIBDL_LIBRARY} )
set(LIBDL_INCLUDE_DIRS ${LIBDL_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
	LibDL DEFAULT_MSG
    LIBDL_LIBRARY LIBDL_INCLUDE_DIR)

mark_as_advanced(LIBDL_INCLUDE_DIR LIBDL_LIBRARY)
