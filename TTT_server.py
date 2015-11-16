
import socket
import threading

class server():

	def __init__( self ):
		
		self.server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.port = 9999
		self.server_socket.bind( (socket.gethostname(), self.port) )
		#self.server_socket.bind( ('192.168.0.118', self.port) )
		self.server_socket.listen(0)
		self.wait_list = None
		self.active_games_count=0



	def run( self ):
		
		print 'TIC_TAC_TOE - server started.'
		try: 
			while True:
				self.client_socket, address = self.server_socket.accept()
				print 'connection recieved :', address

				if self.wait_list == None:
					self.client_socket.send( '0' )	#0 means wait until one more player is connected
					self.wait_list = self.client_socket

				else:
					self.client_socket.send( '1' )	#tell the player about its own status
					self.wait_list.send( '0' )	#tell player1 that game is ready now.
					
					game_session = threading.Thread( target=self.start_session, args=[self.wait_list, self.client_socket] )
					game_session.daemon = True
					game_session.start()
					self.wait_list = None


		except Exception as error:
			print error
			self.stop_server()

		except KeyboardInterrupt:
			self.stop_server()
			



	def stop_server( self ):
		print 
		if self.active_games_count != 0:
			print 'Some active games were interrupted.'
		print 'Server stopped Successfully.'
		self.server_socket.close()










	def start_session( self, player1, player2 ):

		print 'Game_session_id	    :', self.active_games_count
		self.active_games_count+=1
		msg = None
		while msg != '0':
			try:
				msg = player1.recv(1)
				if msg == '0':
					player2.send( '0' )
					break
				#print 'recieved from player1', msg
				player2.send( msg )
				#print 'sent to player2', msg

				msg = player2.recv(1)
				#print 'recieved from player2', msg
				player1.send( msg )
				#print 'sent to player1', msg
			except:
				break

		self.active_games_count-=1
		print 'Game session closed :', self.active_games_count








game_server = server()
game_server.run()


