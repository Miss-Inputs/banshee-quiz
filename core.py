# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import sqlite3
from os.path import expanduser

def query(db, sql, * params):
	cursor = db.execute(sql, params)
	columns = [x[0] for x in cursor.description]
		
	return [dict(zip(columns, row)) for row in cursor]

def query_onecol(db, sql, * params):
	cursor = db.execute(sql, params)
	return [row[0] for row in cursor]

def query_first(db, sql, * params):
	cursor = db.execute(sql, params)
	columns = [x[0] for x in cursor.description]
	row = cursor.fetchone()
	if row is None:
		return None
	
	return dict(zip(columns, row))

def banshee_is_running():
	"""
	This relies on you having the MPRIS plugin enabled, but if you don't, it'll probably just
	act like it's never running
	It seems you can't check for the org.bansheeproject.Banshee service because
	that is always there even when it's not running
	"""
	bus = dbus.SessionBus()
	for service in bus.list_names():
		if service == 'org.mpris.MediaPlayer2.banshee':
			return True
		
	return False

def get_db(readonly=True):	
	#Under Windows, this'd be in the roaming application data apparently (who cares tho mirite)
	banshee_db_path = '{0}/.config/banshee-1/banshee.db'.format(expanduser('~'))
	#if banshee_is_running():
	#Does this actually matter? I've commented it out for now
	#	print('Banshee is running so we will avoid messing with its locking by having our own copy')
	#	new_path = copy2(banshee_db_path, '/tmp/banshee-analysis.db')
	#	path = 'file:{0}?mode=ro'.format(new_path)
	#else:
	path = 'file:{0}?mode={1}'.format(banshee_db_path, 'ro' if readonly else 'rw')
	conn = sqlite3.connect(path, uri=True)
	#conn.create_function("ensure_singular", 1, ensure_singular)
	return conn