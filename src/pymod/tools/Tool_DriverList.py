#!/usr/bin/env python
##############################################################################
# $Id$
#
# Project:  OpenEV
# Purpose:  Graphical tool to list drivers built into current version of GDAL.
# Author:   Gillian Walter, gillian.walter@atlantis-scientific.com
#
# Notes: GDAL's html files must be copied into OpenEV's html directory for
#        the help buttons to work properly.
#
###############################################################################
# Copyright (c) 2003, Atlantis Scientific Inc. (www.atlantis-scientific.com)
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

from gviewapp import Tool_GViewApp
from osgeo import gdal
import gvhtml
import gtk

class ToolDriverList(Tool_GViewApp):
    def __init__(self, app=None, startpath=None):
        Tool_GViewApp.__init__(self, app)

        self.init_menu()

        self.supported_list = []
        self.unsupported_list = []
        self._official_support = []

        for i in range(gdal.GetDriverCount()):
            iDriver = gdal.GetDriver(i)
            next_list = []
            if iDriver.HelpTopic:
                helpstr = iDriver.HelpTopic
            else:
                helpstr = None
            next_list.append(iDriver.LongName)
            next_list.append(iDriver.ShortName)

            mdata = iDriver.GetMetadata()
            next_list.append(mdata.get("DCAP_CREATECOPY","NO"))
            next_list.append(mdata.get("DMD_CREATIONDATATYPES",'Unknown'))
            next_list.append(helpstr)

            if iDriver.ShortName in self._official_support:
                self.supported_list.append(next_list)
            else:
                self.unsupported_list.append(next_list)

        self.init_dialog()

    def init_menu(self):
        self.menu_entries.set_entry("Help/Formats...", 1, self.driver_tool_cb)

    def init_dialog(self):
        self.dialog = gtk.Window()
        self.dialog.set_title('Available Image Formats')
        self.dialog.set_size_request(300,500)
        self.dialog.set_border_width(10) 
        self.dialog.set_resizable(False)
        self.tooltips = gtk.Tooltips()
        self.button_dict={}
        # main shell 
        mainshell = gtk.VBox(spacing=1)
        self.dialog.add(mainshell)
        self.show_list = []
        self.show_list.append(mainshell)

        #frame1=gtk.Frame('Supported')
        #self.show_list.append(frame1)
        #mainshell.pack_start(frame1,expand=False)
        #num_s=len(self.supported_list)
        #if num_s > 0:
        #    s_table = gtk.Table(num_s,3)
        #    row=0            
        #    for fmt_list in self.supported_list:
        #        clabel=gtk.Entry()
        #        clabel.set_editable(False)
        #        clabel.set_text(fmt_list[0])
        #        self.show_list.append(clabel)
        #        self._make_tooltip(clabel,fmt_list)
        #        s_table.attach(clabel,0,1,row,row+1)
        #        if fmt_list[4] is not None:
        #            self.button_dict[fmt_list[1]]=gtk.Button('Help')
        #            self.button_dict[fmt_list[1]].connect('clicked',self.help_clicked_cb,fmt_list[4])
        #            s_table.attach(self.button_dict[fmt_list[1]],1,2,row,row+1)
        #        row=row+1
        #    frame1.add(s_table)
        #    self.show_list.append(s_table)

        frame2 = gtk.Frame()
        pixel_scroll = gtk.ScrolledWindow()
        pixel_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.show_list.append(pixel_scroll)
        self.show_list.append(frame2)
        mainshell.pack_start(frame2)
        frame2.add(pixel_scroll)
        num_us = len(self.unsupported_list)
        if num_us:
            us_table = gtk.Table()
            row = 0
            for fmt_list in self.unsupported_list:
                clabel = gtk.Entry()
                clabel.set_editable(False)
                clabel.set_text(fmt_list[0])
                self.show_list.append(clabel)
                self._make_tooltip(clabel, fmt_list)
                us_table.attach(clabel, 0, 1, row, row+1)
                if fmt_list[4] is not None:
                    self.button_dict[fmt_list[1]] = gtk.Button(stock=gtk.STOCK_HELP)
                    self.button_dict[fmt_list[1]].connect('clicked',self.help_clicked_cb,fmt_list[4])
                    us_table.attach(self.button_dict[fmt_list[1]], 1, 2, row, row+1)
                row += 1
            pixel_scroll.add_with_viewport(us_table)
            self.show_list.append(us_table)
        self.button_dict['close'] = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.button_dict['close'].connect('clicked', self.close)
        mainshell.pack_start(self.button_dict['close'], expand=False)
        self.show_list.append(self.button_dict['close'])
        self.dialog.connect('delete-event', self.close)
        for item in self.show_list:
            item.show()

    def help_clicked_cb(self, but, topic):
        gvhtml.LaunchHTML(topic)

    def driver_tool_cb(self, *args):
        for item in self.show_list:
            item.show()
        self.dialog.show_all()
        self.dialog.present()

    def _make_tooltip(self, clabel, info_list):
        txt ='Long Name: '+info_list[0]+'\n'
        txt += 'Short Name: '+info_list[1]+'\n'
        txt += 'Creation support: '+info_list[2]+'\n'
        txt += 'Data types: '+info_list[3]
        self.tooltips.set_tip(clabel, txt)

    def close(self, *args):
        self.dialog.hide()
        return True

TOOL_LIST=['ToolDriverList']
