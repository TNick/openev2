# ----------------------------------------------------------------------------
# Todo
# ============================================================================


# ----------------------------------------------------------------------------

#TODO: correct the source code; it should use the headers just like any other
# client application.
include_directories(${PROJECT_SOURCE_DIR}/src/lib/gv)


add_executable(testmain testmain.c)
target_link_libraries(testmain
    gv
    ${OPENGL_gl_LIBRARY}
    ${OPENGL_glu_LIBRARY}
    ${PROJ4_LIBRARY}
    ${GTK2_ATK_LIBRARY_RELEASE}
    ${GTK2_CAIRO_LIBRARY_RELEASE}
    ${GTK2_GDK_PIXBUF_LIBRARY_RELEASE}
    ${GTK2_GIO_LIBRARY_RELEASE}
    ${GTK2_GLIB_LIBRARY_RELEASE}
    ${GTK2_GMODULE_LIBRARY_RELEASE}
    ${GTK2_GTHREAD_LIBRARY_RELEASE}
    ${GTK2_PANGOCAIRO_LIBRARY_RELEASE}
    ${GTK2_PANGOFT2_LIBRARY_RELEASE}
    ${GTK2_PANGO_LIBRARY_RELEASE}
    ${GTK2_GDK_LIBRARY_RELEASE}
    ${GTK2_GTK_LIBRARY_RELEASE}
    ${GLIB_CORE}
    ${GLIB_CORE}
    ${GDAL_LIBRARIES}
    ${GTK2_GOBJECT_LIBRARY_RELEASE}
)
# ============================================================================
