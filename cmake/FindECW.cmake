#
# We find the new versions (4, 5, ...) that does not allow writing files.
#
#  ECW_INCLUDE_DIRS - where to find headers
#  ECW_LIBRARIES    - List of libraries
#  ECW_FOUND        - True if found.
#  ECW_FLAGS        - Definitions
#  ECW_DLLS         - DLLs
#  ECW_VER_MAJOR    - major version
#  ECW_VER_MINOR    - minor version
#  ECW_VER_SERVICE  - service version
#  ECW_VER_BUILD    - build
#
#
# Set ECW_PROCESSOR_TYPE to either "win32" or "x64" before find_package.
# By default ECW_PROCESSOR_TYPE is set to match CMAKE_SIZE_OF_VOID_P.
#
# Set ECW_DEBUG_PARTICLE to "d" to select debug build. Leave it unset
# or set it to an empty string to select release version.
#
# Set ECW_STATIC to use the static version; by default shared version
# is returned.
#
#

# set (ECW_STATIC ON)


include(FindPackageHandleStandardArgs)

IF   (ECW_INCLUDE_DIRS AND ECW_LIBRARIES)
	# Already in cache, be silent
ELSE (ECW_INCLUDE_DIRS AND ECW_LIBRARIES)
	set (ECW_DLLS )
	set (ECW_LIBRARIES )
    set (ECW_PROCESSOR_TYPE "$ENV{ECW_PROCESSOR_TYPE}")

	if (NOT ECW_PROCESSOR_TYPE)
		if    ("${CMAKE_SIZE_OF_VOID_P}" STREQUAL "4")
			set (ECW_PROCESSOR_TYPE "win32")
		else  ("${CMAKE_SIZE_OF_VOID_P}" STREQUAL "4")
			set (ECW_PROCESSOR_TYPE "x64")
		endif ("${CMAKE_SIZE_OF_VOID_P}" STREQUAL "4")
    elseif ("${ECW_PROCESSOR_TYPE}" STREQUAL "64")
        set (ECW_PROCESSOR_TYPE "x64")
    elseif ("${ECW_PROCESSOR_TYPE}" STREQUAL "32")
        set (ECW_PROCESSOR_TYPE "win32")
    endif ()
	message (STATUS "ECW_PROCESSOR_TYPE = ${ECW_PROCESSOR_TYPE}")
	
	find_path(ECW_INCLUDE_DIR 
		NAMES ECWJP2BuildNumber.h
		PATH_SUFFIXES ecw
		PATHS 
			"$ENV{UNIX_LIKE_ROOT}/include"
			"$ENV{ECW_ROOT}/include")
			
			
	# extract the version from the header
	if (ECW_INCLUDE_DIR)
		file(STRINGS "${ECW_INCLUDE_DIR}/ECWJP2BuildNumber.h" ECW_BUILD_DATA)
		set (ECW_VER_MAJOR "0")
		set (ECW_VER_MINOR "0")
		set (ECW_VER_SERVICE "0")
		set (ECW_VER_BUILD "0")
		foreach(ECW_BUILD_DATA_LINE_ ${ECW_BUILD_DATA})
			set (ECW_BUILD_DATA_LINE ${ECW_BUILD_DATA_LINE_})
			
			if (ECW_BUILD_DATA_LINE     MATCHES "[ \t]*#define[ \t]+NCS_ECWJP2_VER[ \t]+")
				string (REGEX REPLACE           "[ \t]*#define[ \t]+NCS_ECWJP2_VER[ \t]+" "" 
					ECW_VER_MAJOR ${ECW_BUILD_DATA_LINE})
			elseif (ECW_BUILD_DATA_LINE MATCHES "[ \t]*#define[ \t]+NCS_ECWJP2_VER_MAJOR[ \t]+")
				string (REGEX REPLACE           "[ \t]*#define[ \t]+NCS_ECWJP2_VER_MAJOR[ \t]+" "" 
					ECW_VER_MAJOR ${ECW_BUILD_DATA_LINE})
			elseif (ECW_BUILD_DATA_LINE MATCHES "[ \t]*#define[ \t]+NCS_ECWJP2_VER_MIN[ \t]+")
				string (REGEX REPLACE           "[ \t]*#define[ \t]+NCS_ECWJP2_VER_MIN[ \t]+" ""
					ECW_VER_MINOR ${ECW_BUILD_DATA_LINE})
			elseif (ECW_BUILD_DATA_LINE MATCHES "[ \t]*#define[ \t]+NCS_ECWJP2_VER_BUILD[ \t]+")
				string (REGEX REPLACE           "[ \t]*#define[ \t]+NCS_ECWJP2_VER_BUILD[ \t]+" ""
					ECW_VER_BUILD ${ECW_BUILD_DATA_LINE})
			elseif (ECW_BUILD_DATA_LINE MATCHES "[ \t]*#define[ \t]+NCS_ECWJP2_VER_SERVICE[ \t]+")
				string (REGEX REPLACE           "[ \t]*#define[ \t]+NCS_ECWJP2_VER_SERVICE[ \t]+" ""
					ECW_VER_SERVICE ${ECW_BUILD_DATA_LINE})
			endif()
		endforeach()
	endif()
	
	if (ECW_STATIC)
		find_library(ECW_LIBRARY
			NAMES NCSEcwS${ECW_DEBUG_PARTICLE} NCSEcwS4_RO${ECW_DEBUG_PARTICLE} NCSEcwS5_RO${ECW_DEBUG_PARTICLE}
			PATHS 
				"$ENV{UNIX_LIKE_ROOT}/lib"
				"$ENV{ECW_ROOT}/lib/vc${MSVC_VERSION}0/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc130/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc120/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc110/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc100/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc90/${ECW_PROCESSOR_TYPE}"
				)
		if (ECW_LIBRARY)
			list (APPEND ECW_LIBRARIES ${ECW_LIBRARY})
		endif (ECW_LIBRARY)
		set(ECW_FLAGS -DNCSECW_EXPORTS)
	
	else(ECW_STATIC)
		
		find_library(ECW_LIBRARY
			NAMES NCSEcw${ECW_DEBUG_PARTICLE} NCSEcw4_RO${ECW_DEBUG_PARTICLE} NCSEcw5_RO${ECW_DEBUG_PARTICLE}
			PATHS 
				"$ENV{UNIX_LIKE_ROOT}/lib"
				"$ENV{ECW_ROOT}/lib/vc${MSVC_VERSION}0/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc130/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc120/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc110/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc100/${ECW_PROCESSOR_TYPE}"
				"$ENV{ECW_ROOT}/lib/vc90/${ECW_PROCESSOR_TYPE}"
				)
		if (ECW_LIBRARY)
			list (APPEND ECW_LIBRARIES ${ECW_LIBRARY})
		
			get_filename_component(ECW_LIB_PATH "${ECW_LIBRARY}" DIRECTORY)
			get_filename_component(ECW_LIB_NAME "${ECW_LIBRARY}" NAME)
			message (STATUS "ECW_LIB_PATH = ${ECW_LIB_PATH}")
			message (STATUS "ECW_LIB_NAME = ${ECW_LIB_NAME}")
			
			find_library(ECW_LIBRARY_NET
				NAMES NCScnet${ECW_DEBUG_PARTICLE} NCScnet4${ECW_DEBUG_PARTICLE} NCScnet5${ECW_DEBUG_PARTICLE}
				PATHS 
					"${ECW_LIB_PATH}"
				NO_DEFAULT_PATH)
			if (ECW_LIBRARY_NET)
				list (APPEND ECW_LIBRARIES ${ECW_LIBRARY_NET})
			endif ()
			message (STATUS "ECW_LIBRARY_NET = ${ECW_LIBRARY_NET}")
			
			find_library(ECW_LIBRARY_UTIL
				NAMES NCSUtil${ECW_DEBUG_PARTICLE} NCSUtil4${ECW_DEBUG_PARTICLE} NCSUtil5${ECW_DEBUG_PARTICLE}
				PATHS 
					"${ECW_LIB_PATH}"
				NO_DEFAULT_PATH)
			if (ECW_LIBRARY_UTIL)
				list (APPEND ECW_LIBRARIES ${ECW_LIBRARY_UTIL})
			endif ()
			message (STATUS "ECW_LIBRARY_UTIL = ${ECW_LIBRARY_UTIL}")	
		
			if (WIN32)
				STRING(REGEX REPLACE "[\\\\/]lib[\\\\/]" "/bin/" ECW_DLL_PATH ${ECW_LIB_PATH})
				set (ECW_DLL_PATHS 
						${ECW_DLL_PATH}
						${ECW_INCLUDE_DIR}/../bin
						${ECW_INCLUDE_DIR}/../../bin)
				message (STATUS "ECW_DLL_PATH = ${ECW_DLL_PATH}")	

				STRING(REGEX REPLACE "\\.lib$" ".dll" ECW_DLL_NAME ${ECW_LIB_NAME})
				find_file(ECW_DLL ${ECW_DLL_NAME} PATHS ${ECW_DLL_PATHS})
				if (ECW_DLL)
					list (APPEND ECW_DLLS ${ECW_DLL})		
				endif ()
				message (STATUS "ECW_DLL = ${ECW_DLL}")	

				if (ECW_LIBRARY_NET)
					get_filename_component(ECW_DLL_NAME "${ECW_LIBRARY_NET}" NAME)
					STRING(REGEX REPLACE "\\.lib$" ".dll" ECW_DLL_NAME ${ECW_DLL_NAME})
					message (STATUS "ECW_DLL_NAME = ${ECW_DLL_NAME}")	
					
					find_file(ECW_DLL_NET ${ECW_DLL_NAME} PATHS ${ECW_DLL_PATHS})
					if (ECW_DLL_NET)
						list (APPEND ECW_DLLS ${ECW_DLL_NET})		
					endif ()
				endif ()
				message (STATUS "ECW_DLL_NET = ${ECW_DLL_NET}")	
				
				if (ECW_LIBRARY_UTIL)
					get_filename_component(ECW_DLL_NAME "${ECW_LIBRARY_UTIL}" NAME)
					STRING(REGEX REPLACE "\\.lib$" ".dll" ECW_DLL_NAME ${ECW_DLL_NAME})
					message (STATUS "ECW_DLL_NAME = ${ECW_DLL_NAME}")	
					
					find_file(ECW_DLL_UTIL ${ECW_DLL_NAME} PATHS ${ECW_DLL_PATHS})
					if (ECW_DLL_UTIL)
						list (APPEND ECW_DLLS ${ECW_DLL_UTIL})		
					endif ()
				endif ()
				message (STATUS "ECW_DLL_UTIL = ${ECW_DLL_UTIL}")	
				
				find_file(ECW_DLL_TBB "tbb${ECW_DEBUG_PARTICLE}.dll" PATHS ${ECW_DLL_PATHS})
				if (ECW_DLL_TBB)
					list (APPEND ECW_DLLS ${ECW_DLL_TBB})		
				endif ()
				message (STATUS "ECW_DLL_TBB = ${ECW_DLL_TBB}")	
				
			endif(WIN32)
		endif(ECW_LIBRARY)
		set(ECW_FLAGS )
	
	endif(ECW_STATIC)
	
	FIND_PACKAGE_HANDLE_STANDARD_ARGS(ECW 
										ECW_INCLUDE_DIR
										ECW_LIBRARY)

	if (ECW_FOUND)
		set(ECW_INCLUDE_DIRS ${ECW_INCLUDE_DIR})
	endif (ECW_FOUND)
ENDIF (ECW_INCLUDE_DIRS AND ECW_LIBRARIES)

