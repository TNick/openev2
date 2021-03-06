###############################################################################
# $Id$
#
# Project:  OpenEV
# Purpose:  Convenience widgets, and services built on Gtk widgets.
#           Note that these will eventually be moved into an Atlantis wide
#           set of utility classes in python.
# Author:   Frank Warmerdam, warmerda@home.com
#
# Maintained by Mario Beauchamp (starged@gmail.com)
#
###############################################################################
# Copyright (c) 2000, Atlantis Scientific Inc. (www.atlsci.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################

import pygtk
pygtk.require('2.0')
import gtk as _gtk
from gtk.gdk import *
import pgu
import os
import pgufilesel

# differentiate between CIETMap and OpenEV
if 'CIETMAP_HOME' in os.environ:
    import cview as gview
else:
    import gview

def is_of_class(class_obj,class_name):
    if class_obj.__name__ == class_name:
        return 1
    for c in class_obj.__bases__:
        if is_of_class(c,class_name) == 1:
            return 1
    return 0

# DEPRECATED: please use pgu.ComboText
class GvOptionMenu(pgu.ComboText):
    def __init__(self, contents, callback=None):
        pgu.ComboText.__init__(self, contents, model=None, action=callback)
        self.callback = callback
        self.cur_selection = 0
        self.set_active(0)

    def set_history(self, item):
        if item == self.cur_selection:
            return

        self.cur_selection = item
        self.set_active(item)

        if self.callback:
            self.callback(self)

    def get_history(self):
        return self.get_active()

    def set_om_selection(self, widget, data):
        if widget.get_active():
            self.set_history(data)

#
# borrowed from CIETmap cietutils.py and adapted for OpenEV
#
class _MessageBox(_gtk.Dialog):
    def __init__(self, message='', buttons=(), stock=None):
        _gtk.Dialog.__init__(self, title='', parent=None, flags=_gtk.DIALOG_MODAL, buttons=buttons)
        self.set_border_width(5)

        hbox = _gtk.HBox(spacing=5)
        hbox.set_border_width(5)
        self.vbox.pack_start(hbox)

        if stock:
            img = _gtk.image_new_from_stock(stock, _gtk.ICON_SIZE_DIALOG)
            hbox.pack_start(img, expand=False)

        label = _gtk.Label(message)
        label.set_justify(_gtk.JUSTIFY_LEFT)
        hbox.pack_start(label)

        self.vbox.show_all()
        # TODO: fix grab_focus
##        default.grab_focus()

def gv_message(title, text, stock=None, buttons=(_gtk.STOCK_OK,1)):
    """display a message dialog in a standardized way (modal, pixmap etc)"""
    win = _MessageBox(text, buttons, stock)
    win.set_title(title)
    id = win.run()
    win.hide()
    win.destroy()

    return id

def warning(text):
    return gv_message("Warning", text, _gtk.STOCK_DIALOG_WARNING)

def error(text):
    return gv_message("ERROR", text, _gtk.STOCK_DIALOG_ERROR)

def yesno(title="Confirm Action", text="Do you wish to do this?"):
    id = gv_message(title, text, _gtk.STOCK_DIALOG_QUESTION, (_gtk.STOCK_YES,1,_gtk.STOCK_NO,0))
    return ('No','Yes')[id]

def noyes(title="Confirm Action", text="Do you wish to do this?"):
    id = gv_message(title, text, _gtk.STOCK_DIALOG_QUESTION, (_gtk.STOCK_NO,0,_gtk.STOCK_YES,1))
    return ('No','Yes')[id]

def okcancel(title="Continue", text="Continue or cancel action?"):
    return gv_message(title, text, _gtk.STOCK_DIALOG_QUESTION, (_gtk.STOCK_OK, _gtk.RESPONSE_OK,
                                                                _gtk.STOCK_CANCEL, _gtk.RESPONSE_CANCEL))

def is_shapefile( filename ):
    try:
        ext = filename[len(filename)-4:].lower()
        if ext == '.shp' or ext == '.shx' or ext == '.dbf':
            return 1
        else:
            return 0
    except:
        return 0

def is_project_file( filename ):
    try:
        ext = filename[len(filename)-4:].lower()
        if ext == '.opf':
            return 1

        first_line = open(filename).read(20)
        if first_line[:10] == '<GViewApp>':
            return 1
        else:
            return 0
    except:
        return 0


# GvMenuFactory is just GtkExtra.MenuFactory, with the
# addition of a function to allow you to insert entries
# after the fact...

class GvMenuFactory(_gtk.MenuBar):
    def __init__(self, type=0):
        _gtk.MenuBar.__init__(self)
        self.accelerator = _gtk.AccelGroup()
        self.__menus = {}
        self.__items = {}
    def add_entries(self, entries):
        for entry in entries:
            apply(self.create, tuple(entry))
    def create(self, path, accelerator=None, callback=None, *args):
        last_slash = path.rfind('/')
        if last_slash < 0:
            parentmenu = self
        else:
            parentmenu = self.get_menu(path[:last_slash])
        label = path[last_slash+1:]
        if label == '<separator>':
            item = _gtk.MenuItem()
        elif label[:7] == '<check>':
            item = _gtk.CheckMenuItem(label[7:])
        else:
            item = _gtk.MenuItem(label)
        if label != '<nothing>':
            item.show()
        if accelerator:
            key, mods = self.parse_accelerator(accelerator)
            item.add_accelerator("activate", self.accelerator,
                                     key, mods, 'visible')
        if callback:
            apply(item.connect, ("activate", callback) + args)
        # right justify the help menu automatically
        if label.lower() == 'help' and parentmenu == self:
            item.set_right_justified(True)
        parentmenu.append(item)
        self.__items[path] = item
        return item
    def get_menu(self, path):
        if path == '':
            return self
        if self.__menus.has_key(path):
            return self.__menus[path]
        wid = self.create(path)
        menu = _gtk.Menu()
        menu.set_accel_group(self.accelerator)
        wid.set_submenu(menu)
        self.__menus[path] = menu
        return menu
    def parse_accelerator(self, accelerator):
        key = 0
        mods = 0
        done = False
        while not done:
            if accelerator[:7] == '<shift>':
                mods = mods | _gtk.gdk.SHIFT_MASK
                accelerator = accelerator[7:]
            elif accelerator[:5] == '<alt>':
                mods = mods | _gtk.gdk.MOD1_MASK
                accelerator = accelerator[5:]
            elif accelerator[:6] == '<meta>':
                mods = mods | _gtk.gdk.MOD1_MASK
                accelerator = accelerator[6:]
            elif accelerator[:9] == '<control>':
                mods = mods | _gtk.gdk.CONTROL_MASK
                accelerator = accelerator[9:]
            else:
                done = True
                key = ord(accelerator[0])
        return key, mods
    def remove_entry(self, path):
        if path not in self.__items.keys():
            return
        item = self.__items[path]
        item.destroy()
        length = len(path)
        # clean up internal hashes
        for i in self.__items.keys():
            if i[:length] == path:
                del self.__items[i]
        for i in self.__menus.keys():
            if i[:length] == path:
                del self.__menus[i]

    def get_entry(self, path):
        result = []
        if path not in self.__items.keys():
            return result
        item = self.__items[path]
        result.append(item)
        length = len(path)
        # clean up internal hashes
        for i in self.__items.keys():
            if i[:length] == path:
                result.append(self.__items[i])
        for i in self.__menus.keys():
            if i[:length] == path:
                result.append(self.__menus[i])

	return result
    def remove_entries(self, paths):
        for path in paths:
            self.remove_entry(path)
    def find(self, path):
        return self.__items[path]

    def insert_entry(self, pos, path, accelerator=None, callback=None, *args):
        # like create, but lets you specify position in menu
        last_slash = path.rfind('/')
        if last_slash < 0:
            parentmenu = self
        else:
            parentmenu = self.insert_get_menu(path[:last_slash])
        label = path[last_slash+1:]
        if label == '<separator>':
            item = _gtk.MenuItem()
        elif label[:7] == '<check>':
            item = _gtk.CheckMenuItem(label[7:])
        else:
            item = _gtk.MenuItem(label)
        if label != '<nothing>':
            item.show()
        if accelerator:
            key, mods = self.parse_accelerator(accelerator)
            item.add_accelerator("activate", self.accelerator,
                             key, mods, 'visible')
        if callback:
            apply(item.connect, ("activate", callback) + args)
        # right justify the help menu automatically
        if label.lower() == 'help' and parentmenu == self:
            item.right_justify()
        # all this copying for just the next few line...
        if pos is not None:
            parentmenu.insert(item, pos)
        elif parentmenu == self:
            # Make sure Help retains far-right position
            if self.__menus.has_key('Help'):
                num_main_menus = 0
                for current_path in self.__menus.keys():
                    # Check that it isn't a sub-menu...
                    temp_slash = current_path.rfind('/')
                    if temp_slash < 0:
                        num_main_menus = num_main_menus + 1
                parentmenu.insert(item,max(num_main_menus - 1,1))
            else:
                parentmenu.append(item)
        else:
            parentmenu.append(item)

        self.__items[path] = item
        return item

    def insert_get_menu(self, path):
        # Allows new menus to be placed before help on toolbar
        # by using insert_entry to create parents instead of 
        # create.
        if path == '':
            return self
        if self.__menus.has_key(path):
            return self.__menus[path]
        wid = self.insert_entry(None,path)
        menu = _gtk.Menu()
        menu.set_accel_group(self.accelerator)
        wid.set_submenu(menu)
        self.__menus[path] = menu
        return menu


def read_keyval( line ) :
    import re

    # skip comments & lines that don't contain a '='
    if line[0] == '#' : return [None,None]
    if '=' not in line : return [None,None]

    # Grab the key, val
    [ key, val ] = re.compile( r"\s*=\s*" ).split( line )

    # Strip excess characters from the key string
    key_re = re.compile( r"\b\w+\b" )
    key = key[key_re.search(key).start():]
    key = key[:key_re.search(key).end()]

    # Strip excess characters from the value string
    val = val.strip()
    i = val.find(' ')
    if i > 0 : val = val[0:i]

    return [ key, val ]


def get_tempdir():
    if os.environ.has_key('TMPDIR'):
        tmpdir = os.environ['TMPDIR']
    elif os.environ.has_key('TEMPDIR'):
        tmpdir = os.environ['TEMPDIR']
    elif os.environ.has_key('TEMP'):
        tmpdir = os.environ['TEMP']
    else:
        if os.name == 'nt':
            tmpdir = 'C:'
        else:
            tmpdir = '/tmp'

    return tmpdir

def tempnam( tdir = None, basename = None, extension = None ):
    import gview

    if tdir is None:
        plotfile = gview.get_preference('gvplot_tempfile')
        if plotfile is not None and len(plotfile) > 0:
            if os.path.isdir(plotfile):
                tdir = plotfile
            elif os.path.isdir(os.path.dirname(plotfile)):
                tdir = os.path.dirname(plotfile)
            else:
                tdir = get_tempdir()
        else:
            tdir = get_tempdir()

    if basename is None:
        try:
            pgu.pnm = pgu.pnm + 1
        except:
            pgu.pnm = 1
        basename = 'OBJ_' + str(pgu.pnm)

    if extension is None:
        extension = 'tmp'

    return os.path.join(tdir,basename + '.' + extension)        

def FindExecutable( exe_name ):
    """Try to return full path to requested executable.

    First checks directly, then searches $OPENEV_HOME/bin and the PATH.
    Will add .exe on NT.  Returns None on failure.
    """

    import gview

    if os.name == 'nt':
        (root, ext) = os.path.splitext(exe_name)
        if ext != '.exe':
            exe_name = exe_name + '.exe'

    if os.path.isfile(exe_name):
        return exe_name

    if os.path.isfile(os.path.join(gview.home_dir,'bin',exe_name)):
        return os.path.join(gview.home_dir,'bin',exe_name)

    exe_path = os.environ['PATH']
    if (os.name == 'nt'):
        path_items = exe_path.split(';')
    else:
        path_items = exe_path.split(':')

    for item in path_items:
        exe_path = os.path.join(item,exe_name)
        if os.path.isfile(exe_path):
            return exe_path

    return None

# XML stuff moved to gvxml.py, import it here for backwards compatibility
from gvxml import *

#-----------------------------------------------------------------
# GvDataFilesFrame- function to create data file frame and entries
#-----------------------------------------------------------------
class GvDataFilesFrame(_gtk.Frame):
    def __init__(self,title='',sel_list=('Input','Output'),editable=True):
        _gtk.Frame.__init__(self)
        self.set_label(title)
        self.channels=sel_list

        self.show_list = []
        self.file_dict = {}
        self.button_dict = {}
        self.entry_dict = {}

        #  File options
        file_table = _gtk.Table(len(self.channels),5,False)
        file_table.set_row_spacings(3)
        file_table.set_col_spacings(3)
        self.table = file_table
        self.add(file_table)
        self.show_list.append(file_table)

        for idx in range(len(self.channels)):
            ch = self.channels[idx]
            self.button_dict[ch] = _gtk.Button(ch)
            self.button_dict[ch].set_size_request(100,25)
            self.show_list.append(self.button_dict[ch])
            file_table.attach(self.button_dict[ch], 0,1, idx,idx+1)
            self.entry_dict[ch] = _gtk.Entry()
            self.entry_dict[ch].set_editable(editable)
            self.entry_dict[ch].set_size_request(400, 25)
            self.entry_dict[ch].set_text('')
            self.show_list.append(self.entry_dict[ch])
            self.set_dsfile('',ch)
            file_table.attach(self.entry_dict[ch], 1,5, idx,idx+1)
            if editable == True:
                self.entry_dict[ch].connect('leave-notify-event',self.update_ds)


        for bkey in self.button_dict.keys():
            self.button_dict[bkey].connect('clicked',self.set_dsfile_cb,bkey)

    def set_border_width(self,width):
        self.table.set_border_width(width)

    def set_spacings(self, rowspc, colspc):
        self.table.set_row_spacings(rowspc)
        self.table.set_col_spacings(colspc)

    def update_ds(self,*args):
        for ch in self.channels:
            self.set_dsfile(self.entry_dict[ch].get_text(),ch)

    def show(self,*args):
        for item in self.show_list:
            item.show()


    def set_dsfile_cb(self,*args):
        fkey = args[1]
        file_str = 'Select ' + fkey + ' File'
        pgufilesel.SimpleFileSelect(self.set_dsfile,
                                    fkey,
                                    file_str)

    def set_dsfile(self,fname,fkey):
        self.file_dict[fkey] = fname

        # Save selected file directory
        head = os.path.dirname(fname)
        if len(head) > 0:
            if os.access(head,os.R_OK):
                pgufilesel.simple_file_sel_dir = head+os.sep

        if self.entry_dict.has_key(fkey):            
            if self.file_dict[fkey] is None:
                self.entry_dict[fkey].set_text('')
            else:
                self.entry_dict[fkey].set_text(
                     self.file_dict[fkey])

    def get(self,fkey):
        if self.file_dict.has_key(fkey):
            return self.file_dict[fkey]
        else:
            return None

#-----------------------------------------------------------------
# GvEntryFrame- function to create a frame with a table of entries.
# Input: a list, or list of list, of strings.  initializing with
# [['e1','e2'],['e3'],['e4','e5']] would create a table like this:
#
# e1: <entry>   e2:<entry>
# e3: <entry>
# e4: <entry>   e5:<entry>
#
# The strings in the list are used to index for returning entry
# values, and must be unique.
#
# If some of the entries must have only certain values, a second
# list of the same size may be supplied.  This should contain
# None where entries should be used, but a tuple of strings
# where an option menu should be used.
#-----------------------------------------------------------------
class GvEntryFrame(_gtk.Frame):
    def __init__(self,title,entry_list,widget_list=None):
        _gtk.Frame.__init__(self)
        self.set_label(title)
        table_rows = len(entry_list)
        cols = 1
        for item in entry_list:
            if type(item) in [type((1,)),type([1])]:
                cols = max(cols,len(item))

        # Note: the extra one column is because on windows,
        # creating a gtk table with N columns sometimes only shows
        # N-1 columns???
        self.table = _gtk.Table(table_rows,cols*2+1,False)
        self.table.set_col_spacings(3)
        self.table.set_row_spacings(3)
        self.add(self.table)
        self.entries = {}
        if widget_list is None:
            ridx=0
            for item in entry_list:
                if type(item) in [type((1,)),type([1])]:
                    cidx=0
                    for item2 in item:
                        label = _gtk.Label(item2)
                        label.set_alignment(0,0.5)
                        self.table.attach(label,cidx,cidx+1,ridx,ridx+1)
                        self.entries[item2] = _gtk.Entry()
                        self.entries[item2].set_max_length(30)
                        self.entries[item2].set_editable(True)
                        cidx = cidx+1
                        self.table.attach(self.entries[item2],
                                          cidx,cidx+1,ridx,ridx+1)
                        cidx = cidx+1
                else:
                    label = _gtk.Label(item)
                    label.set_alignment(0,0.5)
                    self.table.attach(label,0,1,ridx,ridx+1)
                    self.entries[item] = _gtk.Entry()
                    self.entries[item].set_max_length(30)
                    self.entries[item].set_editable(True)
                    self.table.attach(self.entries[item],
                                      1,2,ridx,ridx+1)
                ridx=ridx+1

        else:
            ridx=0
            for item in entry_list:
                wtype=widget_list[ridx]
                if type(item) in [type((1,)),type([1])]:
                    cidx=0
                    widx=0
                    for item2 in item:
                        wtype2=wtype[widx]
                        label = _gtk.Label(item2)
                        label.set_alignment(0,0.5)
                        self.table.attach(label,cidx,cidx+1,ridx,ridx+1)
                        if wtype2 is None:
                            self.entries[item2] = _gtk.Entry()
                            self.entries[item2].set_max_length(30)
                            self.entries[item2].set_editable(True)
                        else:
                            self.entries[item2] = GvOptionMenu(wtype2)
                            self.entries[item2].set_history(0)
                            self.entries[item2].contents = wtype2
                        cidx = cidx+1
                        self.table.attach(self.entries[item2],
                                          cidx,cidx+1,ridx,ridx+1)
                        cidx = cidx+1
                        widx = widx+1
                else:
                    label = _gtk.Label(item)
                    label.set_alignment(0,0.5)
                    self.table.attach(label,0,1,ridx,ridx+1)
                    if wtype is None:
                        self.entries[item] = _gtk.Entry()
                        self.entries[item].set_max_length(30)
                        self.entries[item].set_editable(True)
                    else:
                        self.entries[item] = GvOptionMenu(wtype)
                        self.entries[item].set_history(0)
                        self.entries[item].contents = wtype
                    self.table.attach(self.entries[item],
                                      1,2,ridx,ridx+1)
                ridx=ridx+1


    def get(self,fkey):
        if self.entries.has_key(fkey):
            if hasattr(self.entries[fkey],'get_text'):
                return self.entries[fkey].get_text()
            else:
                hist=self.entries[fkey].get_history()
                return self.entries[fkey].contents[hist]   
        else:
            return None

    def set_default_values(self,default_dict):
        """Set default entry values.  Input is default_dict,
           a dictionary with keys corresponding to entries
           (strings) and values corresponding to default
           text or menu setting (also strings).
        """
        for ckey in default_dict.keys():
            cval = default_dict[ckey]
            if self.entries.has_key(ckey):
                if hasattr(self.entries[ckey],'set_text'):
                    self.entries[ckey].set_text(cval)
                else:
                    useidx=None
                    for idx in range(len(self.entries[ckey].contents)):
                        if self.entries[ckey].contents[idx] == cval:
                            useidx=idx
                    if useidx is not None:
                        self.entries[ckey].set_history(useidx)
                    else:
                        print cval+' not a valid entry for '+ckey

            else:
                print 'No entry '+ckey+'- skipping'

    def set_default_lengths(self,default_dict):
        """ Set the maximum entry lengths for non-menu entries.
            Input is defalut_dict, a dictionary with keys
            corresponding to entries (strings) and values
            corresponding to entry lengths (integers)
        """
        for ckey in default_dict.keys():
            cval = default_dict[ckey]
            if self.entries.has_key(ckey):
                if hasattr(self.entries[ckey],'set_text'):
                    self.entries[ckey].set_max_length(cval)
                else:
                    print 'Length cannot be set for a menu ('+ckey+')'

            else:
                print 'No entry '+ckey+'- skipping'

    def set_border_width(self,width):
        self.table.set_border_width(width)

    def set_spacings(self, rowspc, colspc):
        self.table.set_row_spacings(rowspc)
        self.table.set_col_spacings(colspc)

home_dir = gview.home_dir
pics_dir = os.path.join(home_dir, 'pics')

# borrowed from cietutils
def set_layer_color(layer, type, color):
    """set a color property on a layer"""
    prop = " ".join([str(col) for col in color])

    old_prop = layer.get_property(type)
    if old_prop is None or old_prop != prop:
        layer.set_property(type, prop)
        layer.display_change()

def add_stock_icons():
    factory = _gtk.IconFactory()
    for xpm in os.listdir(pics_dir):
        pix = pixbuf_new_from_file(os.path.join(pics_dir, xpm))
        factory.add(os.path.basename(xpm)[:-4], _gtk.IconSet(pix))

    factory.add_default()

def create_pixmap(filename):
    """load an xpm from a filename and create an image

        filename - string, the filename to load the xpm from

    """
    full_filename = os.path.join(pics_dir, filename)
    if not os.path.isfile(full_filename):
        full_filename = os.path.join(pics_dir, 'default.xpm')

    return _gtk.image_new_from_file(full_filename)

def create_pixbuf(filename):
    """load an xpm from a filename and create a pixbuf

        filename - string, the filename to load the xpm from

    """
    if not filename.endswith('.xpm'):
        filename += '.xpm'
    full_filename = os.path.join(pics_dir, filename)
    if not os.path.isfile(full_filename):
        full_filename = os.path.join(pics_dir, 'default.xpm')

    return pixbuf_new_from_file(full_filename)

def create_stock_button(stock, cb, *args):
    image = _gtk.image_new_from_stock(stock, _gtk.ICON_SIZE_BUTTON)
    button = _gtk.Button()
    button.add(image)
    if cb:
        apply(button.connect, ('clicked', cb) + args)

    return button


if __name__ == '__main__':
    dialog = _gtk.Window()

    om = GvOptionMenu( ('Option 1', 'Option 2') )
    om.show()
    dialog.add( om )

    dialog.connect('delete-event', _gtk.main_quit)
    dialog.show()

    _gtk.main()
