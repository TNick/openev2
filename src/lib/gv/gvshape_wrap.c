/******************************************************************************
 * $Id$
 *
 * Project:  OpenEV
 * Purpose:  GvShape Python wrapper
 * Author:   Mario Beauchamp, starged@gmail.com
 *
 ******************************************************************************
 * Copyright (c) 2000, Atlantis Scientific Inc. (www.atlsci.com)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 ******************************************************************************
 *
 */

#include <gv_config.h>

#ifdef HAVE_PYTHON

#define GV_SHAPE(op) (((PyGvShape *)(op))->_o)

typedef struct
{
    PyObject_VAR_HEAD
    GvShape *_o;
} PyGvShape;

PyTypeObject G_GNUC_INTERNAL PyGvShape_Type;

/* ----------- PyGvShape object methods ----------- */

static PyObject *
pygv_shape_from_shape(GvShape *shape)
{
    PyGvShape *self = PyObject_NEW(PyGvShape, &PyGvShape_Type);

    if (self != NULL && shape != NULL) {
        self->_o = shape;
        return (PyObject *)self;
    }
    else {
        PyErr_SetString(PyExc_RuntimeError, "could not create Shape object");
        return NULL;
    }
}

static int
_PyGvShape_init(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "type", NULL };
    int type = GVSHAPE_POINT;
    GvShape *shape;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i:_gv.Shape.__init__",
                                    kwlist, &type))
        return -1;

    shape = gv_shape_new(type);
    if (shape != NULL) {
        gv_shape_ref(shape);
        self->_o = shape;
    }
    else {
        PyErr_SetString(PyExc_RuntimeError, "could not create Shape object");
        return -1;
    }

    return 0;
}

static PyObject *
_PyGvShape_getattro(PyGvShape *self, PyObject *name)
{
    const char *value = NULL;
    PyObject *result = NULL;

    result = PyObject_GenericGetAttr((PyObject *)self, name);
    if (result != NULL)
        return result;
    else
        value = gv_properties_get( gv_shape_get_properties(self->_o), PyString_AsString(name) );

    if (value != NULL)
        return PyString_FromString(value);
    else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static int
_PyGvShape_setattro(PyGvShape *self, PyObject *name, PyObject *value)
{
    GvProperties *properties = NULL;

    properties = gv_shape_get_properties(self->_o);
    if (properties == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Shape object has no properties");
        return -1;
    }
    if (value == NULL)
        gv_properties_remove(properties, PyString_AsString(name));
    else
        gv_properties_set(properties, PyString_AsString(name), PyString_AsString(value));

    return 0;
}

/* ----------- GvShape methods ----------- */

static PyObject *
_wrap_gv_shape_ref(PyGvShape *self)
{
    gv_shape_ref(self->_o);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
_wrap_gv_shape_unref(PyGvShape *self)
{
    gv_shape_unref(self->_o);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
_wrap_gv_shape_get_ref(PyGvShape *self)
{
    return Py_BuildValue( "i", gv_shape_get_ref(self->_o) );
}

static PyObject *
_wrap_gv_shape_copy(PyGvShape *self)
{
    GvShape *copy = gv_shape_copy(self->_o);

    if (copy != NULL)
        return pygv_shape_from_shape(copy);
    else
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject *
_wrap_gv_shape_get_shape_type(PyGvShape *self)
{
    return Py_BuildValue("i", gv_shape_type(self->_o));
}

static PyObject *
_wrap_gv_shape_get_rings(PyGvShape *self)
{
    return Py_BuildValue("i", gv_shape_get_rings(self->_o));
}

static PyObject *
_wrap_gv_shape_get_nodes(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "ring", NULL };
    int      ring = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i:GvShape.get_nodes",
                                    kwlist, &ring))
        return NULL;

    return Py_BuildValue("i", gv_shape_get_nodes(self->_o, ring));
}

static PyObject *
_wrap_gv_shape_add_node(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "x", "y", "z", "ring", NULL };
    int        ring = 0;
    double x=0.0, y=0.0, z=0.0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd|di:GvShape.add_node",
                                    kwlist, &x, &y, &z, &ring))
        return NULL;

    return Py_BuildValue("i", gv_shape_add_node(self->_o, ring, x, y, z));
}

static PyObject *
_wrap_gv_shape_point_in_polygon(PyGvShape *self, PyObject *args)
{
    double  x, y;

    if (!PyArg_ParseTuple(args, "dd:GvShape.point_in_polygon", &x, &y))
        return NULL;

    return Py_BuildValue("i", gv_shape_point_in_polygon(self->_o, x, y));
}

static PyObject *
_wrap_gv_shape_distance_from_polygon(PyGvShape *self, PyObject *args)
{
    double  x, y;

    if (!PyArg_ParseTuple(args, "dd:GvShape.distance_from_polygon", &x, &y))
        return NULL;

    return Py_BuildValue("d", gv_shape_distance_from_polygon(self->_o, x, y));
}

static PyObject *
_wrap_gv_shape_clip_to_rect(PyGvShape *self, PyObject *args)
{
    double  x, y, width, height;
    GvRect      rect;
    GvShape *new_shape;

    if (!PyArg_ParseTuple(args, "dddd:GvShape.clip_to_rect", &x, &y, &width, &height))
        return NULL;

    rect.x = x;
    rect.y = y;
    rect.width = width;
    rect.height = height;

    new_shape = gv_shape_clip_to_rect(self->_o, &rect);

    if (new_shape != NULL)
        return pygv_shape_from_shape(new_shape);
    else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject *
_wrap_gv_shape_collection_get_count(PyGvShape *self)
{
    return Py_BuildValue( "i", gv_shape_collection_get_count(self->_o) );
}

/* ----------- PyGvShape methods ----------- */

static PyObject *
pygv_shape_destroy(PyGvShape *self)
{
    gv_shape_delete(self->_o);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
pygv_shape_get_property(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "property_name", "default_value", NULL };
    char *key;
    char *default_value = NULL;
    const char *value = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|s:GvShape.get_property",
                                    kwlist, &key, &default_value))
        return NULL;

    value = gv_properties_get( gv_shape_get_properties(self->_o), key );
    if (value != NULL)
        return PyString_FromString(value);
    else if (default_value != NULL)
        return PyString_FromString(default_value);
    else
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject *
pygv_shape_get_properties(PyGvShape *self)
{
    GvProperties *properties = NULL;
    PyObject *psDict = NULL;

    properties = gv_shape_get_properties(self->_o);

    psDict = PyDict_New();
    if( properties != NULL )
    {
        int        i, count;

        count = gv_properties_count( properties );
        for( i = 0; i < count; i++ )
        {
            const char *value, *name;
            PyObject *py_name, *py_value;

            value = gv_properties_get_value_by_index(properties,i);
            name = gv_properties_get_name_by_index(properties,i);

            py_name = Py_BuildValue("s",name);
            py_value = Py_BuildValue("s",value);
            PyDict_SetItem( psDict, py_name, py_value );

            Py_DECREF(py_name);
            Py_DECREF(py_value);
        }
    }

    return psDict;
}

static PyObject *
pygv_shape_get_typed_property(PyGvShape *self, PyObject *args)
{
    GvProperties *properties = NULL;
    char *field = NULL, *ftype = "string";
    const char *value = NULL;

    if (!PyArg_ParseTuple(args, "s|s:GvShape.get_typed_property", &field, &ftype))
        return NULL;

    properties = gv_shape_get_properties(self->_o);
    if (properties != NULL)
        value = gv_properties_get(properties, field);

    if (value == NULL)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
    
    if (g_strcasecmp(ftype, "float") == 0)
        return Py_BuildValue("f", atof(value));
    else if (g_strcasecmp(ftype, "integer") == 0)
        return Py_BuildValue("i", atoi(value));
    else
        return Py_BuildValue("s", value);
}

static PyObject *
pygv_shape_get_typed_properties(PyGvShape *self, PyObject *args)
{
    GvProperties *properties = NULL;
    PyObject *psDict = NULL;
    PyObject *pyFieldList = NULL;
    int      nCount, i;

    if (!PyArg_ParseTuple(args, "O!:GvShape.get_typed_properties",
                          &PyList_Type, &pyFieldList))
        return NULL;

    properties = gv_shape_get_properties(self->_o);

    psDict = PyDict_New();
    if( properties == NULL )
        return psDict;

    nCount = PyList_Size(pyFieldList);
    for( i = 0; i < nCount; i++ )
    {
        char *pszFieldName = NULL;
        int nNumericFlag = 0;
        const char *value;
        PyObject *py_name, *py_value;

        if( !PyArg_Parse( PyList_GET_ITEM(pyFieldList,i), "(si)",
                          &pszFieldName, &nNumericFlag ) )
        {
            PyErr_SetString(PyExc_ValueError,
                            "expecting (name,flag) tuples in list.");
            return NULL;
        }

        value = gv_properties_get(properties,pszFieldName);
        if( value == NULL )
        {
            py_value = Py_None;
            Py_INCREF( Py_None );
        }
        else if( nNumericFlag )
            py_value = Py_BuildValue("f",atof(value));
        else
            py_value = Py_BuildValue("s",value);

        py_name = Py_BuildValue("s",pszFieldName);

        PyDict_SetItem( psDict, py_name, py_value );

        Py_DECREF(py_name);
        Py_DECREF(py_value);
    }

    return psDict;
}

static PyObject *
pygv_shape_set_properties(PyGvShape *self, PyObject *args)
{
    GvProperties *properties = NULL;
    PyObject *psDict = NULL;
    PyObject    *pyKey = NULL, *pyValue = NULL;
    Py_ssize_t i;

    if (!PyArg_ParseTuple(args, "O!:GvShape.set_properties", &PyDict_Type, &psDict))
        return NULL;

    properties = gv_shape_get_properties(self->_o);
    gv_properties_clear(properties);

    i = 0;
    while( PyDict_Next( psDict, &i, &pyKey, &pyValue ) )
    {
        char            *key = NULL, *value = NULL;

        if( !PyArg_Parse( pyKey, "s", &key )
            || !PyArg_Parse( pyValue, "s", &value ))
            continue;

        gv_properties_set( properties, key, value );

        pyKey = pyValue = NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
pygv_shape_set_property(PyGvShape *self, PyObject *args)
{
    char *name=NULL, *value=NULL;
    GvProperties *properties = NULL;

    if (!PyArg_ParseTuple(args, "ss:GvShape.set_property", &name, &value))
        return NULL;

    properties = gv_shape_get_properties(self->_o);
    gv_properties_set(properties, name, value);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
pygv_shape_get_node(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "node", "ring", NULL };
    int ring = 0, node = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|ii:GvShape.get_node",
                                    kwlist, &node, &ring))
        return NULL;

    return Py_BuildValue("(" CCC ")",
                         gv_shape_get_x(self->_o, ring, node),
                         gv_shape_get_y(self->_o, ring, node),
                         gv_shape_get_z(self->_o, ring, node));
}

static PyObject *
pygv_shape_set_node(PyGvShape *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "x", "y", "z", "node", "ring", NULL };
    int        ring = 0, node = 0;
    double x=0.0, y=0.0, z=0.0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd|dii:GvShape.set_node",
                                    kwlist, &x, &y, &z, &node, &ring))
        return NULL;

    return Py_BuildValue("i", gv_shape_set_xyz(self->_o, ring, node, x, y, z));
}

static PyObject *
pygv_shape_add_shape(PyGvShape *self, PyObject *args)
{
    PyObject *py_sub_shape;

    if (!PyArg_ParseTuple(args, "O!:GvShape.add_shape", &PyGvShape_Type, &py_sub_shape))
        return NULL;

    gv_shape_collection_add_shape( self->_o, GV_SHAPE(py_sub_shape) );

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
pygv_shape_get_shape(PyGvShape *self, PyObject *args)
{
    int shape_index;
    GvShape *shape;

    if (!PyArg_ParseTuple(args, "i:GvShape.get_shape", &shape_index))
        return NULL;

    shape = gv_shape_collection_get_shape(self->_o, shape_index);
    if (shape != NULL)
        return pygv_shape_from_shape(shape);
    else {
        PyErr_SetString(PyExc_IndexError, "shape index out of range for collection");
        return NULL;
    }
}

static PyObject *
pygv_shape_serialize(PyGvShape *self)
{
    CPLXMLNode *psTree;
    PyObject *py_xml = NULL;

    if (self->_o == NULL)
        return NULL;

    psTree = gv_shape_to_xml_tree(self->_o);
    py_xml = XMLTreeToPyList(psTree);
    CPLDestroyXMLNode(psTree);

    return py_xml;
}

static PyObject *
pygv_shape_from_xml(PyGvShape *self, PyObject *args)
{
    GvShape     *shape;
    CPLXMLNode  *cpl_tree;
    PyObject    *py_tree = NULL;

    if (!PyArg_ParseTuple(args, "O!:GvShape.from_xml", &PyList_Type, &py_tree))
        return NULL;

    cpl_tree = PyListToXMLTree(py_tree);
    
    shape = gv_shape_from_xml_tree(cpl_tree);
    if (shape != NULL)
        return pygv_shape_from_shape(shape);
    else {
        PyErr_SetString(PyExc_ValueError, "XML translation to GvShape filed.");
        return NULL;
    }
}

/* ----------- PyGvShape object definitions ----------- */

static const PyMethodDef _PyGvShape_methods[] = {
    { "add_node", (PyCFunction)_wrap_gv_shape_add_node, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "add_shape", (PyCFunction)pygv_shape_add_shape, METH_VARARGS,
      NULL },
    { "clip_to_rect", (PyCFunction)_wrap_gv_shape_clip_to_rect, METH_VARARGS,
      NULL },
    { "collection_get_count", (PyCFunction)_wrap_gv_shape_collection_get_count, METH_NOARGS,
      NULL },
    { "copy", (PyCFunction)_wrap_gv_shape_copy, METH_NOARGS,
      NULL },
    { "destroy", (PyCFunction)pygv_shape_destroy, METH_NOARGS,
      NULL },
    { "distance_from_polygon", (PyCFunction)_wrap_gv_shape_distance_from_polygon, METH_VARARGS,
      NULL },
    { "from_xml", (PyCFunction)pygv_shape_from_xml, METH_VARARGS,
      NULL },
    { "get_node", (PyCFunction)pygv_shape_get_node, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "get_nodes", (PyCFunction)_wrap_gv_shape_get_nodes, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "get_properties", (PyCFunction)pygv_shape_get_properties, METH_NOARGS,
      NULL },
    { "get_property", (PyCFunction)pygv_shape_get_property, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "get_ref", (PyCFunction)_wrap_gv_shape_get_ref, METH_NOARGS,
      NULL },
    { "get_rings", (PyCFunction)_wrap_gv_shape_get_rings, METH_NOARGS,
      NULL },
    { "get_shape", (PyCFunction)pygv_shape_get_shape, METH_VARARGS,
      NULL },
    { "get_shape_type", (PyCFunction)_wrap_gv_shape_get_shape_type, METH_NOARGS,
      NULL },
    { "get_typed_properties", (PyCFunction)pygv_shape_get_typed_properties, METH_VARARGS,
      NULL },
    { "get_typed_property", (PyCFunction)pygv_shape_get_typed_property, METH_VARARGS,
      NULL },
    { "ref", (PyCFunction)_wrap_gv_shape_ref, METH_NOARGS,
      NULL },
    { "point_in_polygon", (PyCFunction)_wrap_gv_shape_point_in_polygon, METH_VARARGS,
      NULL },
    { "serialize", (PyCFunction)pygv_shape_serialize, METH_NOARGS,
      NULL },
    { "set_node", (PyCFunction)pygv_shape_set_node, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "set_properties", (PyCFunction)pygv_shape_set_properties, METH_VARARGS,
      NULL },
    { "set_property", (PyCFunction)pygv_shape_set_property, METH_VARARGS,
      NULL },
    { "unref", (PyCFunction)_wrap_gv_shape_unref, METH_NOARGS,
      NULL },
    { NULL, NULL, 0, NULL }
};

PyTypeObject G_GNUC_INTERNAL PyGvShape_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                 /* ob_size */
    "_gv.Shape",                   /* tp_name */
    sizeof(PyGvShape),          /* tp_basicsize */
    0,                                 /* tp_itemsize */
    /* methods */
    (destructor)0,        /* tp_dealloc */
    (printfunc)0,                      /* tp_print */
    (getattrfunc)0,       /* tp_getattr */
    (setattrfunc)0,       /* tp_setattr */
    (cmpfunc)0,           /* tp_compare */
    (reprfunc)0,             /* tp_repr */
    (PyNumberMethods*)0,     /* tp_as_number */
    (PySequenceMethods*)0, /* tp_as_sequence */
    (PyMappingMethods*)0,   /* tp_as_mapping */
    (hashfunc)0,             /* tp_hash */
    (ternaryfunc)0,          /* tp_call */
    (reprfunc)0,              /* tp_str */
    (getattrofunc)_PyGvShape_getattro,     /* tp_getattro */
    (setattrofunc)_PyGvShape_setattro,     /* tp_setattro */
    (PyBufferProcs*)0,  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                      /* tp_flags */
    NULL,                        /* Documentation string */
    (traverseproc)0,     /* tp_traverse */
    (inquiry)0,             /* tp_clear */
    (richcmpfunc)0,   /* tp_richcompare */
    0,             /* tp_weaklistoffset */
    (getiterfunc)0,          /* tp_iter */
    (iternextfunc)0,     /* tp_iternext */
    (struct PyMethodDef*)_PyGvShape_methods, /* tp_methods */
    (struct PyMemberDef*)0,              /* tp_members */
    (struct PyGetSetDef*)0,  /* tp_getset */
    NULL,                              /* tp_base */
    NULL,                              /* tp_dict */
    (descrgetfunc)0,    /* tp_descr_get */
    (descrsetfunc)0,    /* tp_descr_set */
    0,                 /* tp_dictoffset */
    (initproc)_PyGvShape_init,             /* tp_init */
    (allocfunc)0,           /* tp_alloc */
    (newfunc)0,               /* tp_new */
    (freefunc)0,             /* tp_free */
    (inquiry)0              /* tp_is_gc */
};
#endif // HAVE_PYTHON
