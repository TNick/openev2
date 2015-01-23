# ----------------------------------------------------------------------------
# Todo
# ============================================================================


# ----------------------------------------------------------------------------

configure_file (
	"gv_config.h_cmake"
	"${INCLUDE_OUTPUT_PATH}/gv_config.h"
	@ONLY
)

set (LIB_HEADERS
	"${INCLUDE_OUTPUT_PATH}/gv_config.h"
	atkutil.h
	crs.h
	dllfct.h
	gextra.h
	glu.h
	gluos.h
	gtypes.h
	gvareatool.h
	gvautopan.h
	gvdata.h
	gview.h
	gvlayer.h
	gvlinetool.h
	gvmanager.h
	gvmarshal.h
	gvmesh.h
	gvnodetool.h
	gvpointtool.h
	gvpoitool.h
	gvpquerylayer.h
	gvproperties.h
	gvraster.h
	gvrasteraverage.h
	gvrastercache.h
	gvrasterize.h
	gvrasterlayer.h
	gvrasterlut.h
	gvrastertypes.h
	gvrecttool.h
	gvrenderinfo.h
	gvroitool.h
	gvrotatetool.h
	gvselecttool.h
	gvshape.h
	gvshapelayer.h
	gvshapes.h
	gvshapeslayer.h
	gvsymbolmanager.h
	gvtool.h
	gvtoolbox.h
	gvtracktool.h
	gvtypes.h
	gvundo.h
	gvutils.h
	gvviewarea.h
	gvviewlink.h
	gvzoompantool.h
	invdistance.h
	shapefil.h)

set (LIB_SOURCES
	crs.c
	dbfopen.c
	gextra.c
	gvareatool.c
	gvautopan.c
	gvdata.c
	gvlayer.c
	gvlinetool.c
	gvmanager.c
	gvmarshal.c
	gvmesh.c
	gvmodule.c
	gvnodetool.c
	gvogr.c
	gvpointtool.c
	gvpoitool.c
	gvpquerylayer.c
	gvprint.c
	gvproperties.c
	gvraster.c
	gvrasteraverage.c
	gvrastercache.c
	gvrasterconvert.c
	gvrasterize.c
	gvrasterlayer.c
	gvrasterlut.c
	gvrastersource.c
	gvrecttool.c
	gvrenderinfo.c
	gvroitool.c
	gvrotatetool.c
	gvselecttool.c
	gvshape.c
	gvshapefile.c
	gvshapelayer.c
	gvshapes.c
	gvshapeslayer.c
	gvshape_wrap.c
	gvskirt.c
	gvsymbolmanager.c
	gvtessshape.c
	gvtexturecache.c
	gvtool.c
	gvtoolbox.c
	gvtracktool.c
	gvundo.c
	gvutils.c
	gvviewarea.c
	gvviewlink.c
	gvwinprint.c
	gvzoompantool.c
	gv_override.c
	gv_pwrap.c
	invdistance.c
	llrasterize.c
	shpopen.c)

set (LIB_DEPS )

if (OPENEV_SHARED)
    set(LIB_TYPE SHARED)
    add_definitions (-DOPENEV_SHARED_EXPORT)
else ()
    set(LIB_TYPE STATIC)
endif()
add_library(gv ${LIB_TYPE} ${LIB_HEADERS} ${LIB_SOURCES})
#target_link_libraries (gv ${LIB_DEPS})

# ============================================================================
