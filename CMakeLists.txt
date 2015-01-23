# ----------------------------------------------------------------------------
# The project uses cmake to build its components. This is the main cmake file
# that should be used like so:
#     mkdir build && cd build && cmake $OPTIONS ../src && make && make install
# $OPTIONS are a set of definitions of the form `-DDEFINITION=Value`
# Here are valid definitions:
#
#   -DCMAKE_BUILD_TYPE=Debug
#   -DCMAKE_BUILD_TYPE=Release
#       Either enable or disable development aids;
#
#   -DCMAKE_INSTALL_PREFIX:PATH=/usr
#       The base path for installed components;
#
#   -DCMAKE_PREFIX_PATH=/some/path;/some/other/path
#       Add to the list of standard paths used to find packages
#
# To get the full list of make targets run `make help` in build directory. Here
# are some important ones:
#
#   install
#       copies installable components to their intended places
#
#   doc
#       creates documentation
#
#
# ============================================================================

# ----------------------------------------------------------------------------
# generic things
cmake_minimum_required(VERSION 3.0.0)
project("OpenEV" VERSION "2.0.0" LANGUAGES C CXX)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/")
# ============================================================================

# ----------------------------------------------------------------------------
# various options
option( OPENEV_BUILD_TESTS
		"Activate or deactivate building of internal tests"
		OFF)
option( OPENEV_BUILD_DOCUMENTATION
		"Activate or deactivate building of documentation"
		OFF)
option( OPENEV_SHARED
        "Build the library as a shared library or as a static library"
        OFF)

# What is ATLANTIS_BUILD?

add_definitions (-D_CRT_SECURE_NO_WARNINGS )
# ============================================================================

# ----------------------------------------------------------------------------
# assume a "build" directory inside actual build directory
# actual build directory
#     build
#         bin
#         lib
#         include
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY
	"${PROJECT_BINARY_DIR}/build/bin" )
set( EXECUTABLE_OUTPUT_PATH
	"${PROJECT_BINARY_DIR}/build/bin" )
file(MAKE_DIRECTORY ${EXECUTABLE_OUTPUT_PATH})
set( LIBRARY_OUTPUT_PATH
	"${PROJECT_BINARY_DIR}/build/lib" )
file(MAKE_DIRECTORY ${LIBRARY_OUTPUT_PATH})
set( INCLUDE_OUTPUT_PATH
	"${PROJECT_BINARY_DIR}/build/include/${PROJECT_NAME_UNIX}" )
file(MAKE_DIRECTORY ${INCLUDE_OUTPUT_PATH})

include_directories(
  "${INCLUDE_OUTPUT_PATH}")
# ============================================================================

# ----------------------------------------------------------------------------
# other definitions
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_DEBUG_POSTFIX  "_debug")
# ============================================================================

# ----------------------------------------------------------------------------
# Prepare proper system variables (for config files)
if (MSVC)
	set (TARGET_COMPILER_MSVC ON)
else (MSVC)
	set (TARGET_COMPILER_MSVC OFF)
endif (MSVC)

if (WIN32)
  set (TARGET_SYSTEM_WIN32 ON)
else (WIN32)
  set (TARGET_SYSTEM_WIN32 OFF)
endif (WIN32)

if (UNIX)
  set (TARGET_SYSTEM_UNIX ON)
else ()
  set (TARGET_SYSTEM_UNIX OFF)
endif ()

if ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "x86")
	set (TARGET_32BITS ON)
	set (TARGET_64BITS OFF)
elseif ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "arm")
	message (FATAL_ERROR "Architecture is not available for testing")
else ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "x86")
	set (TARGET_32BITS OFF)
	set (TARGET_64BITS ON)
endif ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "x86")

include (CheckIncludeFile)
include (CheckFunctionExists)
include (TestBigEndian)

CHECK_INCLUDE_FILE("stdio.h" STDC_HEADERS)
CHECK_INCLUDE_FILE("fcntl.h" HAVE_FCNTL_H)
CHECK_INCLUDE_FILE("unistd.h" HAVE_UNISTD_H)
CHECK_INCLUDE_FILE("dlfcn.h" HAVE_DLFCN_H)

CHECK_FUNCTION_EXISTS("_doprnt" HAVE_DOPRNT)
CHECK_FUNCTION_EXISTS("vprintf" HAVE_VPRINTF)
TEST_BIG_ENDIAN(WORDS_BIGENDIAN)

# ============================================================================

# ----------------------------------------------------------------------------
# Dependencies
find_package(OpenGL REQUIRED)
include_directories (${OPENGL_INCLUDE_DIRS})

find_package(GLib REQUIRED)
include_directories (${GLIB_INCLUDE_DIRS})

set(GTK2_ADDITIONAL_SUFFIXES "gdk;gtk-2.0/gdk;include/gtk-2.0/gdk;lib/gtk-2.0/gdk;gtk-2.0/include/gtk-2.0/gdk;gtk-2.0/lib/gtk-2.0/gdk")
find_package(Gtk2 REQUIRED)
include_directories (${GTK2_INCLUDE_DIRS})



find_path(GDK_CONFIG "gdkconfig.h"
    PATHS ${GTK2_INCLUDE_DIRS} ${CMAKE_MODULE_PATH}
    PATH_SUFFIXES "lib/gtk-2.0/include")
message(STATUS "GDK_CONFIG = ${GDK_CONFIG}")
find_path(GDK_PIXBUF "gdk-pixbuf/gdk-pixbuf.h"
    PATHS ${GTK2_INCLUDE_DIRS} ${CMAKE_MODULE_PATH}
    PATH_SUFFIXES "gdk-pixbuf-2.0")
message(STATUS "GDK_PIXBUF = ${GDK_PIXBUF}")
find_path(GDK_GLEXT "gtk/gtkgl.h"
    PATHS ${GTK2_INCLUDE_DIRS} ${CMAKE_MODULE_PATH}
    PATH_SUFFIXES "gtkglext-1.0")
message(STATUS "GDK_GLEXT = ${GDK_GLEXT}")
find_path(GDK_GLEXT_CFG "gdkglext-config.h"
    PATHS ${GTK2_INCLUDE_DIRS} ${CMAKE_MODULE_PATH}
    PATH_SUFFIXES "lib/gtkglext-1.0/include")
message(STATUS "GDK_GLEXT_CFG = ${GDK_GLEXT_CFG}")

include_directories (${GTK2_GTK_INCLUDE_DIR})
include_directories (${GTK2_GDK_INCLUDE_DIR})
include_directories (${GTK2_CAIRO_INCLUDE_DIR})
include_directories (${GTK2_PANGO_INCLUDE_DIR})
include_directories (${GTK2_ATK_INCLUDE_DIR})
include_directories (${GTK2_FONTCONFIG_INCLUDE_DIR})
include_directories (${GTK2_GOBJECT_INCLUDE_DIR})
include_directories (${GDK_CONFIG})
include_directories (${GDK_PIXBUF})
include_directories (${GDK_GLEXT})
include_directories (${GDK_GLEXT_CFG})


find_package(Gdal REQUIRED)
set (HAVE_OGR ${GDAL_FOUND})
include_directories (${GDAL_INCLUDE_DIRS})

find_package(LibDL)
set (HAVE_LIBDL ${LIBDL_FOUND})

# ============================================================================

# ----------------------------------------------------------------------------
# subcomponents
add_subdirectory(resource)
add_subdirectory(src)
# ============================================================================
