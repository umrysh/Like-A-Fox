#    Built for python 2.7

#    Copyright 2012 Dave Umrysh
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import MySQLdb as mdb
import pygtk,gtk,re,csv,string

class MysqlClient:
	def submit(self,widget):
		if self.type == "Select":
			# Print headings
			if self.selectcolumn == "*":
				self.cur.execute('select column_name from information_schema.columns where table_name = "%s" and TABLE_SCHEMA = "%s"' % (self.table,self.database))
				numrows = int(self.cur.rowcount)
				toprint = ""
				for i in range(numrows):
					row = self.cur.fetchone()
					if i == 0:
						toprint = "%s" % row[0]
					else:
						toprint = toprint + " | %s" % row[0]
				print toprint
			else:
				print self.selectcolumn

			if self.wherecolumn != "" and self.where2column != "" and self.where3.get_text() != "":
				self.cur.execute('select %s from %s where %s %s "%s"' % (self.selectcolumn,self.table,self.wherecolumn,self.where2column,self.where3.get_text()))
			else:
				self.cur.execute('select %s from %s' % (self.selectcolumn,self.table))
			numrows = int(self.cur.rowcount)
		    	for i in range(numrows):
				row = self.cur.fetchone()
				length = len(row)
				toprint = ""
				for f in range(length):
					if f == 0:
						toprint = "%s" % row[f]
					else:
						toprint = toprint + ", %s" % row[f]
				print toprint
			print "END"
		elif self.type == "Insert":
			if self.csvpath != "":
				Ofile = open(self.csvpath, 'r')
				Reader = csv.reader(Ofile, delimiter=',', quotechar='"')

				for row in Reader:
					temp = ""
					for count in range(0,len(row)):
						if temp == "":
							temp = '"%s"' % row[count]
						else:
							temp = temp + "," + '"%s"' % row[count]
					
					print 'insert into %s values(%s)' % (self.table,temp)
					self.cur.execute('insert into %s values(%s)' % (self.table,temp))
	def enter_callback(self,widget, entry):
		temp=0;
	def cb_select_menu_select(self,widget,data):
		self.selectcolumn = data
	def cb_where_menu_select(self,widget,data):
		self.wherecolumn = data
	def cb_where2_menu_select(self,widget,data):
		self.where2column = data
	def cb_from_menu_select(self,widget,data):
		# Destroy rest of query
		self.QSelectHbox.destroy()
		self.QWhereHbox.destroy()
		if data != "":
			self.cur.execute('select column_name from information_schema.columns where table_name = "%s" and TABLE_SCHEMA = "%s"' % (data,self.database))
			self.table = data
			numrows = int(self.cur.rowcount)

			self.QSelectHbox = gtk.HBox(False, 0)

			self.QSelectText = gtk.Label("Select Column : ")
			self.QSelectHbox.pack_start(self.QSelectText, True, True, 0)

			self.QSelectMenu = gtk.Menu()
		
			self.QSelectOpt = gtk.OptionMenu()
		
			item = self.make_menu_item_database ("All(*)", self.cb_select_menu_select, "*")
			item.show()
			self.QSelectMenu.append(item)
			self.selectcolumn = "*"

			self.columns = []

			## Append to array instead because we need the values again
			for i in range(numrows):
				row = self.cur.fetchone()
				self.columns.append(row[0])

	    		for i in range(numrows):
				item = self.make_menu_item_database (self.columns[i], self.cb_select_menu_select, self.columns[i])
				item.show()
				self.QSelectMenu.append(item)
			self.QSelectOpt.set_menu(self.QSelectMenu)
			self.QSelectHbox.pack_start(self.QSelectOpt, True, True, 0)
			self.Qvbox.pack_start(self.QSelectHbox, False, True, 0)
			self.QSelectOpt.show()
			self.QSelectHbox.show()
			self.QSelectText.show()
			######
			self.QWhereHbox= gtk.HBox(False, 0)

			self.QWhereText = gtk.Label("Where the value in column : ")
			self.QWhereHbox.pack_start(self.QWhereText, True, True, 0)

			self.QWhereMenu = gtk.Menu()
		
			self.QWhereOpt = gtk.OptionMenu()
		
			item = self.make_menu_item_database ("-----", self.cb_where_menu_select, "")
			item.show()
			self.QWhereMenu.append(item)
			self.wherecolumn = ""
			for i in range(numrows):
				item = self.make_menu_item_database (self.columns[i], self.cb_where_menu_select, self.columns[i])
				item.show()
				self.QWhereMenu.append(item)
			self.QWhereOpt.set_menu(self.QWhereMenu)
			self.QWhereHbox.pack_start(self.QWhereOpt, True, True, 0)


			self.QWhere2Menu = gtk.Menu()
			self.QWhere2Opt = gtk.OptionMenu()
			item = self.make_menu_item_database ("-----", self.cb_where2_menu_select, "")
			item.show()
			self.QWhere2Menu.append(item)
			self.where2column = ""

			item = self.make_menu_item_database ("Equals", self.cb_where2_menu_select, "=")
			item.show()
			self.QWhere2Menu.append(item)
			item = self.make_menu_item_database ("Is Greater Than", self.cb_where2_menu_select, ">")
			item.show()
			self.QWhere2Menu.append(item)
			item = self.make_menu_item_database ("Is Greater or Equal To", self.cb_where2_menu_select, ">=")
			item.show()
			self.QWhere2Menu.append(item)
			item = self.make_menu_item_database ("Is Less Than", self.cb_where2_menu_select, "<")
			item.show()
			self.QWhere2Menu.append(item)
			item = self.make_menu_item_database ("Is Less or Equal To", self.cb_where2_menu_select, "<=")
			item.show()
			self.QWhere2Menu.append(item)
			

			self.QWhere2Opt.set_menu(self.QWhere2Menu)
			self.QWhereHbox.pack_start(self.QWhere2Opt, True, True, 0)


			self.where3 = gtk.Entry()
			self.where3.set_max_length(255)
			self.where3.connect("activate", self.enter_callback, self.where3)
			self.where3.set_text("")
			self.where3.select_region(0, len(self.where3.get_text()))
			self.QWhereHbox.pack_start(self.where3, True, True, 0)

			self.Qvbox.pack_start(self.QWhereHbox, False, True, 0)
			self.QWhereOpt.show()
			self.QWhere2Opt.show()
			self.where3.show()
			self.QWhereHbox.show()
			self.QWhereText.show()

			self.submithbox.show()

	def cb_type_menu_select(self,widget,data):
		if data != "":
			self.warning2.hide()
			try:
				self.con = mdb.connect(host=self.ipaddress.get_text(), port=int(self.port.get_value_as_int()),user=self.username.get_text(), passwd=self.password.get_text(),db=data)
		  	except mdb.Error, e:
		    		print("Could not connect to MySQL database.\nError %d: %s" % (e.args[0],e.args[1]))
				self.warning2.show()
				return
			self.database = data
			self.con.autocommit(True)
			self.cur = self.con.cursor()
			self.buttons_hbox.show()

	def select_query(self,widget):
		self.type = "Select"
		self.Qvbox.destroy()
		self.submithbox.hide()
		
				
		self.cur.execute('show tables')

		numrows = int(self.cur.rowcount)

		self.Qframe.show()
		self.Qvbox = gtk.VBox(False, 0)
		self.Qvbox.set_border_width(5)
		self.Qframe.add(self.Qvbox)

		self.QFromHbox = gtk.HBox(False, 0)

		self.QFromText = gtk.Label("From Table : ")
		self.QFromHbox.pack_start(self.QFromText, True, True, 0)

		self.QFromMenu = gtk.Menu()
	
		self.QFromOpt = gtk.OptionMenu()
	
		item = self.make_menu_item_database ("-----", self.cb_from_menu_select, "")
		item.show()
		self.QFromMenu.append(item)
    		for i in range(numrows):
			row = self.cur.fetchone()
			item = self.make_menu_item_database (row[0], self.cb_from_menu_select, row[0])
			item.show()
			self.QFromMenu.append(item)
		self.QFromOpt.set_menu(self.QFromMenu)
		self.QFromHbox.pack_start(self.QFromOpt, True, True, 0)
		self.Qvbox.pack_start(self.QFromHbox, False, True, 0)
		self.Qvbox.show()
		self.QFromOpt.show()
		self.QFromHbox.show()
		self.QFromText.show()

		self.QSelectHbox = gtk.HBox(False, 0)
		self.QWhereHbox = gtk.HBox(False, 0)

	def insert_query(self,widget):
		self.type = "Insert"	
		self.Qvbox.destroy()
		self.submithbox.hide()
			
		self.cur.execute('show tables')

		numrows = int(self.cur.rowcount)

		self.Qframe.show()
		self.Qvbox = gtk.VBox(False, 0)
		self.Qvbox.set_border_width(5)
		self.Qframe.add(self.Qvbox)

		self.QFromHbox = gtk.HBox(False, 0)

		self.QFromText = gtk.Label("Insert Into Table : ")
		self.QFromHbox.pack_start(self.QFromText, True, True, 0)

		self.QFromMenu = gtk.Menu()
	
		self.QFromOpt = gtk.OptionMenu()
	
		item = self.make_menu_item_database ("-----", self.cb_insert_menu_select, "")
		item.show()
		self.QFromMenu.append(item)
    		for i in range(numrows):
			row = self.cur.fetchone()
			item = self.make_menu_item_database (row[0], self.cb_insert_menu_select, row[0])
			item.show()
			self.QFromMenu.append(item)
		self.QFromOpt.set_menu(self.QFromMenu)
		self.QFromHbox.pack_start(self.QFromOpt, True, True, 0)
		self.Qvbox.pack_start(self.QFromHbox, False, True, 0)
		self.Qvbox.show()
		self.QFromOpt.show()
		self.QFromHbox.show()
		self.QFromText.show()

		self.QSelectHbox = gtk.HBox(False, 0)
		
	def cb_insert_menu_select(self,widget,data):
		# Destroy rest of query
		self.QSelectHbox.destroy()
		if data != "":
			self.table = data
			self.QSelectHbox = gtk.HBox(False, 0)
			button3 = gtk.Button("Select CSV File")
			entryLOC = gtk.Entry()
			entryLOC.set_text("")
			entryLOC.set_editable(False)
			button3.connect("clicked", self.fileselect, entryLOC)
			button3.show()
			entryLOC.show()

			self.QSelectHbox.pack_start(entryLOC, True, True, 0)
			self.QSelectHbox.pack_start(button3, False, False, 0)

			self.Qvbox.pack_start(self.QSelectHbox, False, True, 0)

			self.QSelectHbox.show()
			self.submithbox.show()

	def fileselect(self, widget, entryLOC):
		dialog = gtk.FileChooserDialog("Open..",
			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("CSV")
		filter.add_pattern("*.csv")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.csvpath = dialog.get_filename()
			entryLOC.set_text(self.csvpath)
		dialog.destroy()	

	def make_menu_item_database(self,named, callback, data1):
	    item = gtk.MenuItem(named)
	    item.connect("activate", callback, data1)
	    return item
	def is_valid_ipv4(self,ip):
	    """Validates IPv4 addresses.
	    """
	    pattern = re.compile(r"""
		^
		(?:
		  # Dotted variants:
		  (?:
		    # Decimal 1-255 (no leading 0's)
		    [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
		  |
		    0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
		  |
		    0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
		  )
		  (?:                  # Repeat 0-3 times, separated by a dot
		    \.
		    (?:
		      [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
		    |
		      0x0*[0-9a-f]{1,2}
		    |
		      0+[1-3]?[0-7]{0,2}
		    )
		  ){0,3}
		|
		  0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
		|
		  0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
		|
		  # Decimal notation, 1-4294967295:
		  429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
		  42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
		  4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
		)
		$
	    """, re.VERBOSE | re.IGNORECASE)
	    return pattern.match(ip) is not None
	def is_valid_ipv6(self,ip):
	    """Validates IPv6 addresses.
	    """
	    pattern = re.compile(r"""
		^
		\s*                         # Leading whitespace
		(?!.*::.*::)                # Only a single whildcard allowed
		(?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
		(?:                         # Repeat 6 times:
		    [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
		    (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
		){6}                        #
		(?:                         # Either
		    [0-9a-f]{0,4}           #   Another group
		    (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
		    [0-9a-f]{0,4}           #   Last group
		    (?: (?<=::)             #   Colon iff preceeded by exacly one colon
		     |  (?<!:)              #
		     |  (?<=:) (?<!::) :    #
		     )                      # OR
		 |                          #   A v4 address with NO leading zeros 
		    (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
		    (?: \.
		        (?:25[threading0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
		    ){3}
		)
		\s*                         # Trailing whitespace
		$
	    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
	    return pattern.match(ip) is not None
	def is_valid_ip(self,ip):
	    """Validates IP addresses. Function originally posted by MizardX on http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
	    """
	    return self.is_valid_ipv4(ip) or self.is_valid_ipv6(ip)

	def deselectdb(self,widget):
		self.cur = None
		self.con = None
		self.port.set_editable(True) 
		self.username.set_editable(True) 
		self.password.set_editable(True)
		self.ipaddress.set_editable(True)
		self.button1.show()
		self.button2.hide()
		self.Qvbox.destroy()
		self.vbox.destroy()
		self.submithbox.hide()
		self.buttons_hbox.hide()
	def selectdb(self,widget):
		self.warning2.hide()
		if self.is_valid_ip(self.ipaddress.get_text()):
			self.warning1.hide()
			try:
				self.con = mdb.connect(host=self.ipaddress.get_text(), port=int(self.port.get_value_as_int()),user=self.username.get_text(), passwd=self.password.get_text())
		  	except mdb.Error, e:
		    		print("Could not connect to MySQL database.\nError %d: %s" % (e.args[0],e.args[1]))
				self.warning2.show()
				return
			self.ipaddress.set_editable(False) 
			self.port.set_editable(False) 
			self.username.set_editable(False) 
			self.password.set_editable(False)
			self.ipaddress.set_editable(False)
			self.con.autocommit(True)
			self.cur = self.con.cursor()	
			self.cur.execute('show databases')

			numrows = int(self.cur.rowcount)

			self.DatabaseMenu = gtk.Menu()
		
			self.DatabaseOpt = gtk.OptionMenu()
		
			item = self.make_menu_item_database ("-----", self.cb_type_menu_select, "")
			item.show()
			self.DatabaseMenu.append(item)
	    		for i in range(numrows):
				row = self.cur.fetchone()


				item = self.make_menu_item_database (row[0], self.cb_type_menu_select, row[0])
				item.show()
				self.DatabaseMenu.append(item)
			self.DatabaseOpt.set_menu(self.DatabaseMenu)
			self.DatabaseHbox = gtk.HBox(False, 0)

			self.DatabaseText = gtk.Label("Select a Database:")
			self.DatabaseHbox.pack_start(self.DatabaseText, True, True, 0)
			self.DatabaseHbox.pack_start(self.DatabaseOpt, True, True, 0)
			
			self.vbox = gtk.VBox(False, 0)
			self.vbox.set_border_width(5)
			self.frame.add(self.vbox)

			self.Qvbox = gtk.VBox(False, 0)
			self.Qvbox.set_border_width(5)
			self.Qframe.add(self.Qvbox)

			self.vbox.pack_start(self.DatabaseHbox, False, True, 0)
			self.DatabaseOpt.show()
			self.DatabaseText.show()
			self.DatabaseHbox.show()
			self.frame.show()
			self.vbox.show()
			self.button1.hide()
			self.button2.show()
		else:
			self.warning1.show()
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	 	self.window.connect("destroy", lambda w: gtk.main_quit())
	 	self.window.set_title("Like A Fox")
		self.window.set_default_size(750, 600)
		self.window.set_position(gtk.WIN_POS_CENTER)

	  	self.main_vbox = gtk.VBox(False, 5)
	  	self.main_vbox.set_border_width(10)
	  	self.window.add(self.main_vbox) 
		#
		self.iphbox = gtk.HBox(False, 0)
		self.main_vbox.pack_start(self.iphbox, False, False, 5)

		self.iplabel = gtk.Label("IP Address of MySQL Server : ")
		self.iplabel.set_alignment(0, 0.5)
		self.iphbox.pack_start(self.iplabel, True, True, 0)
	  
		self.ipaddress = gtk.Entry()
		self.ipaddress.set_max_length(15)
		self.ipaddress.connect("activate", self.enter_callback, self.ipaddress)
		self.ipaddress.set_text("127.0.0.1")
		self.ipaddress.select_region(0, len(self.ipaddress.get_text()))
		self.iphbox.pack_start(self.ipaddress, True, True, 0)

		adj = gtk.Adjustment(3306, 1.0, 999999.0, 1.0, 5.0, 0.0)
		self.port = gtk.SpinButton(adj, 0, 0)
		self.port.set_wrap(True)
		self.iphbox.pack_start(self.port, True, True, 0)
		#
		self.userhbox = gtk.HBox(False, 0)
		self.main_vbox.pack_start(self.userhbox, False, False, 5)

		self.userlabel = gtk.Label("MySQL Username : ")
		self.userlabel.set_alignment(0, 0.5)
		self.userhbox.pack_start(self.userlabel, True, True, 0)
	  
		self.username = gtk.Entry()
		self.username.set_max_length(30)
		self.username.connect("activate", self.enter_callback, self.username)
		self.username.set_text("root")
		self.username.select_region(0, len(self.username.get_text()))
		self.userhbox.pack_start(self.username, True, True, 0)
		#
		self.passhbox = gtk.HBox(False, 0)
		self.main_vbox.pack_start(self.passhbox, False, False, 5)

		self.passlabel = gtk.Label("MySQL Password : ")
		self.passlabel.set_alignment(0, 0.5)
		self.passhbox.pack_start(self.passlabel, True, True, 0)
	  
		self.password = gtk.Entry()
		self.password.set_max_length(30)
		self.password.connect("activate", self.enter_callback, self.password)
		self.password.set_text("*******")
		self.password.select_region(0, len(self.password.get_text()))
		self.passhbox.pack_start(self.password, True, True, 0)
		#
		self.connecthbox = gtk.HBox(False, 0)

		self.button1 = gtk.Button("Connect")
		self.button2 = gtk.Button("Disconnect")
		self.frame = gtk.Frame("Database")
		self.typeframe = gtk.Frame("Type of Query to Perform")
		self.Qframe = gtk.Frame("Query")

	  	self.button1.connect("clicked", self.selectdb)
		self.connecthbox.pack_start(self.button1, True, True, 5)
	
	  	self.button2.connect("clicked", self.deselectdb)
		self.connecthbox.pack_start(self.button2, True, True, 5) 
	 	self.main_vbox.pack_start(self.connecthbox, False, False, 5) 
	 	#
		self.main_vbox.pack_start(self.frame, False, False, 0)
		self.main_vbox.pack_start(self.typeframe, False, False, 0)
		self.main_vbox.pack_start(self.Qframe, False, False, 0)
		#
		selectQButton = gtk.Button("Select")
		selectQButton.connect("clicked", self.select_query)
		insertQButton = gtk.Button("Insert")
		insertQButton.connect("clicked", self.insert_query)
		self.buttons_hbox = gtk.HBox(False, 5)
		self.typeframe.add(self.buttons_hbox)
		self.buttons_hbox.pack_start(selectQButton, False, False, 5)
		self.buttons_hbox.pack_start(insertQButton, False, False, 5)
		#
		self.submithbox = gtk.HBox(False, 0)
		self.button3 = gtk.Button("Submit Query")
		self.button3.connect("clicked", self.submit)
		self.submithbox.pack_start(self.button3, True, True, 5) 
	 	self.main_vbox.pack_start(self.submithbox, False, False, 5) 
		#
		self.warninghbox = gtk.HBox(False, 0)
	   	self.main_vbox.pack_start(self.warninghbox, False, False, 5)
		self.warning1 = gtk.Label("Please Enter A Valid IP Address.")
		self.warning1.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ff0000'))
		self.warninghbox.pack_start(self.warning1, True, True, 0)
		#
		self.warninghbox2 = gtk.HBox(False, 0)
	   	self.main_vbox.pack_start(self.warninghbox2, False, False, 5)
		self.warning2 = gtk.Label("Could not connect to MySQL database.")
		self.warning2.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ff0000'))
		self.warninghbox2.pack_start(self.warning2, True, True, 0)

		self.window.show_all()
		self.button2.hide()
		self.warning1.hide()
		self.warning2.hide()
		self.submithbox.hide()
		self.buttons_hbox.hide()
		gtk.main()

if __name__ == "__main__":
    MysqlClient()
