"""
Task list:
	- Change difficulty - number of songs picked
	- Play song again
	- Maybe play song from different positions than the start?
	- Handle titles of picked songs being the same
	- Different attributes than song title
	- Time limit on questions (maybe)
	- Scoring by time taken to answer question
"""

import random
import vlc
from core import *
		
vlc_instance = vlc.Instance()
vlc_player = vlc_instance.media_player_new()

class GlobalState:
	def __init__(self):	
		self.score = 0
		self.rounds = 0
		self.db = get_db(True)
		
	@property
	def score_ratio(self):
		return self.score / self.rounds

def console_main():
	state = GlobalState()
	playing = True
	while playing:
		playing = play_round_console(state)
	print('Your score is {0} out of {1} ({2:.2%})'.format(state.score, state.rounds, 
		  state.score_ratio))
		
def is_numeric(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
def play_round_console(state):
	random_songs = get_random_songs(state.db, 4)
	actual_song = random.choice(random_songs)
	
	uri = actual_song['Uri']
	play_media(uri)

	print('Round {0}: Which song is this?'.format(state.rounds + 1))
	for index, song in enumerate(random_songs):
		print('{0}) {1}'.format(index + 1, song['Title']))
		
	raw_choice = ''
	input_valid = False
	while not input_valid:
		raw_choice = input('Enter answer or q to quit: ')
		if raw_choice.startswith('q'):
			return False
		
		def __handle_input(user_input):
			if is_numeric(user_input):
				choice = int(user_input) - 1
				if choice < len(random_songs):
					if random_songs[choice] is actual_song:
						print('Yay you guessed right')
						state.score += 1
						state.rounds += 1
					else:
						print('BZZT that was {0}'.format(actual_song['Title']))
						state.rounds += 1
					return True
				else:
					print('Not a valid number')
					return False
			print('Not valid input')
		
		input_valid = __handle_input(raw_choice)
		
	return True
	
def play_media(uri):
	media = vlc_instance.media_new(uri)
	vlc_player.set_media(media)
	vlc_player.play()
	
def get_random_songs(db, count):
	sql = 'SELECT * FROM coretracks WHERE primarysourceid = 1 ORDER BY RANDOM() LIMIT ?'
	return query(db, sql, count)

if __name__ == "__main__":
	console_main()
