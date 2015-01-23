# - Try to find GLib library
# Once done this will define
#  GLIB_FOUND - System has GLib
#  GLIB_INCLUDE_DIRS - The GLib include directories
#  GLIB_LIBRARIES - The libraries needed to use GLib
#  GLIB_DEFINITIONS - Compiler switches required for using GLib

find_package(PkgConfig QUIET)
pkg_check_modules(PC_GLIB QUIET GLib)
set(GLIB_DEFINITIONS ${PC_GLIB_CFLAGS_OTHER})

find_path(GLIB_CORE_DIR glib.h
          HINTS ${PC_GLIB_INCLUDEDIR} ${PC_GLIB_INCLUDE_DIRS}
		  PATH_SUFFIXES glib-2.0/ glib-2.0/include)
find_path(GLIB_CONFIG_DIR glibconfig.h
          HINTS ${PC_GLIB_INCLUDEDIR} ${PC_GLIB_INCLUDE_DIRS} ${PC_GLIB_LIBDIR} ${PC_GLIB_LIBRARY_DIRS}
		  PATH_SUFFIXES glib-2.0/ glib-2.0/include lib/glib-2.0/ lib/glib-2.0/include)

find_library(GLIB_CORE NAMES glib-2.0 glib
             HINTS ${PC_GLIB_LIBDIR} ${PC_GLIB_LIBRARY_DIRS})
find_library(GLIB_THREAD NAMES gthread-2.0 gthread
             HINTS ${PC_GLIB_LIBDIR} ${PC_GLIB_LIBRARY_DIRS})
find_library(GLIB_MODULE NAMES gmodule-2.0 gmodule
             HINTS ${PC_GLIB_LIBDIR} ${PC_GLIB_LIBRARY_DIRS})

set(GLIB_LIBRARIES ${GLIB_CORE} ${GLIB_THREAD} ${GLIB_MODULE} )
set(GLIB_INCLUDE_DIRS ${GLIB_CORE_DIR} ${GLIB_CONFIG_DIR})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
	GLib DEFAULT_MSG
    GLIB_MODULE GLIB_THREAD GLIB_CORE
	GLIB_CORE_DIR GLIB_CONFIG_DIR)

mark_as_advanced(GLIB_MODULE GLIB_THREAD GLIB_CORE GLIB_CORE_DIR GLIB_CONFIG_DIR)
