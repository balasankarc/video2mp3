#! /usr/bin/env python
#
# video2mp3
#       
# Copyright (c) 2013
#	 Balasankar C <c.balasankar@gmail.com>
#
#       
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pygtk
import gtk
import sys
import os


class Base:
	#Exit Button
	def destroy(self,widget,data=None):					
		sys.exit()			
	
	def outputselect(self,widget):
		"""Select output file"""
		dialog1=gtk.FileChooserDialog("Name Output File",None,gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		dialog1.set_default_response(gtk.RESPONSE_OK)
		response = dialog1.run()
		self.outputfilename=dialog1.get_filename()
		dialog1.destroy()
		
	def selectfile(self,widget):
		"""Selecting input files"""
		dialog=gtk.FileChooserDialog("Select Input Files",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(True)
		filter = gtk.FileFilter()
		filter.set_name("Video Files")									
		filter.add_pattern("*.mkv")
		filter.add_pattern("*.webm")
		filter.add_pattern("*.flv")
		filter.add_pattern("*.avi")
		filter.add_pattern("*.MKV")
		filter.add_pattern("*.WEBM")
		filter.add_pattern("*.FLV")
		filter.add_pattern("*.AVI")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.filelist = dialog.get_filenames()		
		dialog.destroy()	
	
	def convert(self,widget):
		"""Converting files"""
		md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Select Input Files")
		if self.filelist=="":
			md1.run()
			md1.destroy()
			return
		md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Select Output Folder")
		if self.outputfilename=="":
			md1.run()
			md1.destroy()
			return		
		bitrate=self.combo1.get_active_text().split()[0]
		for p in self.filelist:		
			filename1=p.split('.')
			filename=filename1[0].split('/')
			cmnd = "ffmpeg -y -i '"+p+"' -acodec libmp3lame -ab "+ str(bitrate)+"k '"+self.outputfilename+"/"+ filename[-1] +".mp3'"			
			flag=os.system(cmnd)
		md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Error while converting")
		if flag!=0:
			md1.run()
			md1.destroy()
			self.filelist=""
			self.outputfilename=""
			return
		md = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE, "Successfully Converted")
		md.run()		#Displaying successful message
		md.destroy()
		
	def __init__(self):
		"""Main function"""
		self.flag=0
		self.window = gtk.Window()
		self.window.set_title("VIDEO2MP3")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.resize(220,360)
		self.windowx,self.windowy = self.window.get_position()
		self.window.show()
		self.fixed = gtk.Fixed()
		self.window.connect("destroy",self.destroy)
		self.combo1=gtk.combo_box_new_text()		
		self.combo1.append_text("128 kbps")
		self.combo1.append_text("320 kbps")
		self.combo1.set_active(0)
		self.button4=gtk.Button("Exit")
		self.button1 = gtk.Button("Open")
		self.button3 = gtk.Button("Convert")
		self.button2 = gtk.Button("Choose Output File")
		self.button3.connect("clicked",self.convert)		
		self.button4.connect("clicked",self.destroy)		
		self.button1.connect("clicked",self.selectfile)
		self.button2.connect("clicked",self.outputselect)
		self.button3.set_size_request(150,50)				
		self.button1.set_size_request(150,50)	
		self.button2.set_size_request(150,50)	
		self.button4.set_size_request(150,50)
		self.combo1.set_size_request(150,30)		
		self.fixed.put(self.button1,35,30)
		self.fixed.put(self.button2,35,100)
		self.fixed.put(self.combo1,35,170)		
		self.fixed.put(self.button3,35,220)		
		self.fixed.put(self.button4,35,290)
		self.filelist=""
		self.outputfilename=""
		self.window.add(self.fixed)
		self.window.show_all()
	def main(self):
		gtk.main()
	
if __name__ == "__main__":
	base= Base()
	base.main()

