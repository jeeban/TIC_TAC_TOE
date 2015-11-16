import Tkinter
import threading
import socket
import time
import os



class game_board_cell():
	#design of each cell in the board
	#contains three background image
	def __init__( self, parent, index ):

		#this frmae will hold the objects and later it will be bind to main board.
		self.cell_frame = Tkinter.Frame( parent )
		
		self.cell_image1 = Tkinter.PhotoImage( file='blank.gif' )
		self.blank_background = Tkinter.Button( self.cell_frame, image=self.cell_image1  )
		self.blank_background.image = self.cell_image1

		self.cell_image2 = Tkinter.PhotoImage( file='circle.gif' )
		self.circle_background = Tkinter.Label( self.cell_frame, image=self.cell_image2  )
		self.circle_background.image = self.cell_image2

		self.cell_image3 = Tkinter.PhotoImage( file='cross.gif' )
		self.cross_background = Tkinter.Label( self.cell_frame, image=self.cell_image3  )
		self.cross_background.image = self.cell_image3

		
		self.blank_background.grid( row=0, column=0, columnspan=2 )
		self.circle_background.grid( row=0, column=0, columnspan=2 )
		self.cross_background.grid( row=0, column=0, columnspan=2 )

		self.circle_background.grid_remove()
		self.cross_background.grid_remove()

		self.index = index
		self.player_code = None



class TTT_interface():

	def __init__( self ):
		#possible winning conditions for a 3x3 tic-tac-toe gameplay
		self.win_conditions =  (	None,
						( (1,2,3), (1,4,7), (1,5,9) ),
						( (1,2,3), (2,5,8) ),
						( (1,2,3), (3,6,9), (3,5,7) ),
						( (4,5,6), (1,4,7) ),
						( (4,5,6), (2,5,8), (1,5,9), (3,5,7) ),
						( (4,5,6), (3,6,9) ),
						( (7,8,9), (1,4,7), (3,5,7) ),
						( (7,8,9), (2,5,8) ),
						( (7,8,9), (3,6,9), (1,5,9) )
					)

		self.root_window = Tkinter.Tk()
		self.root_window.title("TIC-TAC-TOE Client")
		self.root_window.geometry("362x340")
		self.root_window.resizable(0,0)
		self.root_window.protocol("WM_DELETE_WINDOW", self.close_app )
		self.root_window.bind("<Destroy>", self.close_app )

		self.cell_image = Tkinter.PhotoImage( file='circle.gif' )
		#self.cell_image = None

		button1 = game_board_cell( self.root_window, 1 )
		button2 = game_board_cell( self.root_window, 2 )
		button3 = game_board_cell( self.root_window, 3 )
		button4 = game_board_cell( self.root_window, 4 )
		button5 = game_board_cell( self.root_window, 5 )
		button6 = game_board_cell( self.root_window, 6 )
		button7 = game_board_cell( self.root_window, 7 )
		button8 = game_board_cell( self.root_window, 8 )
		button9 = game_board_cell( self.root_window, 9 )

		#button binding
		button1.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button1) )
		button2.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button2) )
		button3.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button3) )
		button4.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button4) )
		button5.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button5) )
		button6.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button6) )
		button7.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button7) )
		button8.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button8) )
		button9.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server( button9) )
		

		sidepadding=20
		inpadding=2

		button1.cell_frame.grid( row=0, column=0, padx=(sidepadding,inpadding), pady=(sidepadding,inpadding) )
		button2.cell_frame.grid( row=0, column=1, padx=(inpadding,inpadding),  pady=(sidepadding,inpadding) )
		button3.cell_frame.grid( row=0, column=2, padx=(0,sidepadding), pady=(sidepadding,inpadding) )
		button4.cell_frame.grid( row=1, column=0, padx=(sidepadding,inpadding) )
		button5.cell_frame.grid( row=1, column=1 )
		button6.cell_frame.grid( row=1, column=2, padx=(inpadding,sidepadding) )
		button7.cell_frame.grid( row=2, column=0, padx=(sidepadding,inpadding), pady=(inpadding,sidepadding) )
		button8.cell_frame.grid( row=2, column=1, pady=(inpadding,sidepadding) )
		button9.cell_frame.grid( row=2, column=2, padx=(inpadding,sidepadding), pady=(inpadding,sidepadding) )


		self.init_label = Tkinter.Label( text='', width=44, height=22 )
		self.init_label.grid( row=0, column=0, rowspan=3, columnspan=3 )

		self.info_label = Tkinter.Label( text='', width=44, height=1 )
		self.info_label.grid( row=3, column=0, rowspan=3, columnspan=3 )

		self.retry_button = Tkinter.Button( text='Retry' )
		self.retry_button.grid( row=2, column=0, rowspan=3, columnspan=3, sticky=Tkinter.N )
		self.retry_button.grid_remove()
		self.retry_button.bind( "<Button-1>", lambda event : self.restart_game() )


		self.button_list = ( None, button1, button2, button3, button4, button5, button6, button7, button8, button9 )
		
		##print button1
		#ndex=0
		#for button in self.button_list[1:-2] :
			#button.blank_background.bind("<Button-1>", self.send_cell_detail_over_server )
		#	index+=1
		#	button.blank_background.bind( '<Button-1>', lambda event: self.send_cell_detail_over_server(index) )

	
		self.my_turn = None
		self.key_press_count=0
		self.game_status=1



	def init_app_interface( self ):
		#enter the tkinter mainloop
		self.root_window.mainloop()




	def close_app( self ):
		try:
			self.server.send('x')
		except:
			pass
		os.system( 'kill -9 ' + str(os.getpid()) )








	def send_cell_detail_over_server( self, button ):
		if self.my_turn:
			button.blank_background.grid_remove()
			button.circle_background.grid()
			button.player_code=0
			##print self.check_for_wining_condition( parent.widget['text'])
			
			if self.check_for_wining_condition( button.index):
				self.close_game( color='green', msg='WINNER')
				
			else:
				#parent.widget.bind("<Button-1>", self.cell_already_selected )
				self.info_label.config( text='Wait until opponents move...', background='#ff0000' )
				self.key_press_count += 1
				self.my_turn = False

			try:
				self.server.send( str(button.index) )
				##print 'sent : ', parent.widget['text']
			except Exception as error:
				pass
		else:
			self.info_label.config( text='Its not your turn. Wait until opponents move...', background='#ff0000' )















	def cell_already_selected( self, parent ):
		#callback when oone cell is already selected by someone.
		if self.my_turn:
			self.info_label.config( text='cell already selected. Try another cell.', background='yellow' )
		else:
			self.info_label.config( text='Its not your turn. Wait until opponents move...', background='#ff0000' )






	def restart_game( self ):
		self.retry_button.grid_remove()
		self.init_label.config( bg='#ffffff')
		self.info_label.grid()
		for button in self.button_list[1:]:
			button.player_code = None
			button.blank_background.grid()
			button.cross_background.grid_remove()
			button.circle_background.grid_remove()

		self.my_turn = None
		self.key_press_count=0
		self.game_status=1

		self.server.close()
		#print 'disconnected from server.'
		threading.Thread( target=self.connect_to_server ).start()








	def init_board( self ):
		self.init_label.grid_remove()






	def run( self ):
		threading.Thread( target=self.connect_to_server ).start()
		self.init_app_interface()









	def update_my_board_with_opponents_move( self, msg=None ):
		if msg != '0':
			try:
				button = self.button_list[ int(msg) ]
				button.blank_background.grid_remove()
				button.cross_background.grid()
				button.player_code=1
			except Exception as error:
				self.close_game( color='yellow', msg='connection terminated from server.')

			self.key_press_count += 1
			self.my_turn = True
			self.info_label.config( text='Its your turn. PLay your move...', background='#00ff00' )

			if self.check_for_wining_condition( int(msg) ):
					self.close_game( color='red', msg='LOOSER.')
					self.server.send('0')
			else:
				if self.key_press_count == 9:
					self.close_game( color='yellow', msg='No more moves possible.\nGAME OVER.' )
					self.server.send('0')
			
			
		else:
			if self.key_press_count == 9:
				self.close_game( color='yellow', msg='No more moves possible.\nGAME OVER.' )
			else:
				self.close_game( color='green', msg='WINNER' )








	def close_game( self, color=None, msg=None ):
		self.init_label.grid()
		self.init_label.config( text=msg, background=color )
		self.info_label.grid_remove()
		self.retry_button.grid()
		self.game_status=0
		##print msg








	def check_for_wining_condition( self, msg ):
		for combinations in self.win_conditions[ msg ]:
			if self.button_list[ combinations[0]].player_code == self.button_list[ combinations[1]].player_code == self.button_list[ combinations[2]].player_code:
				return True
		return False







	def connect_to_server( self ):
		
		self.server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.port = 9999

		for attempt in xrange(1,3):
			try:
				self.init_label.config( text='Attempt '+str(attempt)+': connecting to server...')
				time.sleep(1)
				self.server.connect( (socket.gethostname(),self.port) )
				#self.server.connect( ('192.168.0.109',self.port) )
				#self.init_board()
				#self.init_label.grid_remove()
				break
			except Exception as error:
				#print error
				self.init_label.config( text='Connection error: Server not found.\nReconnecting in 5 sec...')
				time.sleep(5)
		else:
			###print 'limit exceed'
			self.init_label.config( text='MAX Attempt limit reached.\nAPP will be closed.' )
			time.sleep(1)
			os.system( 'kill -9 ' + str(os.getpid()) )


		try:
			#connection established
			if self.server.recv(1) == '0':
				self.init_label.config( text='Connected to the server.\nOne more player is  required to start.\nwait for one more player.\n\n\nSearching player2...' )
				
				if self.server.recv(1) == '0':	#indicate that two players are connected. so begin the game.
					self.init_board()
					self.info_label.config( text='You are player1.  Play your move...', background='#00ff00')
					self.my_turn = True



			else:
				#self.init_label.config( text='Connected to the server.\nPlayers found.\nGame will be started soon.' )
				#time.sleep(1)

				self.init_board()
				self.info_label.config( text='You are player2. Wait until player1 move...', background='#ff0000')
				self.my_turn = False

				#wait for the first move only. then both client will be same.
				msg = self.server.recv(1)
				self.update_my_board_with_opponents_move( msg )
		except Exception as error:
			self.close_game( color='yellow', msg='connection terminated from server.')
			

		##print 'while loop started for client.'
		while self.game_status != 0 :
			##print 'waiting for incomming data from server.'
			try:
				msg = self.server.recv(1)
				self.update_my_board_with_opponents_move( msg )
			except:
				#self.close_game( color='yellow', msg='connection failed.')
				break






app = TTT_interface()
app.run()