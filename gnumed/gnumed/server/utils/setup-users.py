#!/usr/bin/env python

"""GnuMed user/group installation.

This script installs all the users and groups needed for
proper GnuMed usage. It will also set proper access rights.

Theory of operation:

Rights will be granted to users via groups. Effectively, groups
are granted certain access rights and users are added to the
appropriate groups as needed.

There's a special user called "gmdb-owner" who owns all the
database objects.

Normal users are represented twice in the database:
 1) under their normal user name with read-only rights
 2) under their user name prepended by "_" for write access

For all this to work you must be able to access the database
server as the standard "postgres" superuser.

This script does NOT set up user specific configuration options.

All definitions are loaded from a config file.

Please consult the Developer's Guide in the GnuMed CVS for
further details.
"""
#==================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/utils/Attic/setup-users.py,v $
__version__ = "$Revision: 1.8 $"
__author__ = "Karsten.Hilbert@gmx.net"
__license__ = "GPL"

import sys, string, os.path

# location of our modules
sys.path.append(os.path.join('.', 'modules'))

import gmLog
_log = gmLog.gmDefLog
_log.SetAllLogLevels(gmLog.lData)

import gmCfg
_cfg = gmCfg.gmDefCfgFile

dbapi = None
conn = None

known_passwords = {}
#==================================================================
def connect_to_db():

	# load database adapter
	global dbapi
	dbapi = None
	try:
		from pyPgSQL import PgSQL
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot load pyPgSQL.pgSQL database adapter module.", exc, fatal=1)
		return None
	dbapi = PgSQL

	# load authentication information
	host = _cfg.get("server", "name")
	if not host:
		_log.Log(gmLog.lErr, "Cannot load database host name from config file.")
		return None
	port = _cfg.get("server", "port")
	if not port.isdigit():
		_log.Log(gmLog.lErr, "Cannot load database API port number from config file.")
		return None
	database = _cfg.get("server", "database")
	if not database:
		_log.Log(gmLog.lErr, "Cannot load database name from config file.")
		return None
	user = _cfg.get("server", "user")
	if not user:
		_log.Log(gmLog.lErr, "Cannot load database super-user from config file.")
		return None

	# get password from user
	print "We still need a password to actually access the database."
	print "(user [%s] in db [%s] on [%s:%s])" % (user, database, host, port)
	password = raw_input("Please type password: ")

	# log in
	global conn
	dsn = "%s:%s:%s:%s:%s" % (host, port, database, user, password)
	try:
		conn = PgSQL.connect(dsn)
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (user, password, database, host, port), exc, fatal=1)
		return None
	_log.Log(gmLog.lInfo, "successfully connected to database (user [%s] in db [%s] on [%s:%s])" % (user, database, host, port))

	return 1
#------------------------------------------------------------------
def verify_db():
	"""Verify database version information."""

	required_version = _cfg.get("server", "version")
	if not required_version:
		_log.Log(gmLog.lErr, "Cannot load minimum required PostgreSQL version from config file.")
		return None

	if conn.version < required_version:
		_log.Log(gmLog.lErr, "Reported live PostgreSQL version [%s] is smaller than the required minimum version [%s]." % (conn.version, required_version))
		print "Installed PostgreSQL does not have minimum required version !"
		return None

	_log.Log(gmLog.lInfo, "installed PostgreSQL version: %s - this is fine with me" % conn.version)
	return 1
#==================================================================
# user related
#------------------------------------------------------------------
def user_exists(aCursor, aUser):
	try:
		aCursor.execute("SELECT usename FROM pg_user WHERE usename='%s';" % aUser)
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot check for user existence.", exc, fatal=1)
		return None
	res = aCursor.fetchone()
	if aCursor.rowcount == 1:
		_log.Log(gmLog.lInfo, "User %s exists." % aUser)
		return 1
	_log.Log(gmLog.lInfo, "User %s does not exist." % aUser)
	return None
#------------------------------------------------------------------
def create_superuser():
	superuser = _cfg.get("defaults", "gnumed database owner")
	if not superuser:
		_log.Log(gmLog.lErr, "Cannot load GnuMed database owner name from config file.")
		return None
	cursor = conn.cursor()
	# does this user already exist ?
	if user_exists(cursor, superuser):
		cursor.close()
		return 1
	# get password for super user
	print "We need a password for the GnuMed standard superuser [%s]." % superuser
	password = raw_input("Please type password: ")
	try:
		cursor.execute("CREATE USER \"%s\" WITH PASSWORD '%s' CREATEDB;" % (superuser, password))
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot create GnuMed standard superuser [%s]." % superuser, exc, fatal=1)
		cursor.close()
		return None
	# paranoia is good
	if user_exists(cursor, superuser):
		cursor.close()
		conn.commit()
		return 1

	cursor.close()
	return None
#------------------------------------------------------------------
def create_user(aCursor, aUser):
	# does this group already exist ?
	if user_exists(aCursor, aUser):
		return 1

	# FIXME: remember this, too for "_usr"
	valid_until = _cfg.get(aUser, "valid until")
	if not valid_until:
		_log.Log(gmLog.lErr, "Cannot load account expiration date for GnuMed user [%s] from config file." % aUser)
		return None

	groups = _cfg.get(aUser, "groups")
	if not groups:
		_log.Log(gmLog.lWarn, "GnuMed user [%s] does not seem to belong to any GnuMed groups." % aUser)
		group_cmd = ""
	else:
		group_cmd = ' IN GROUP "' + string.join(groups, '", "') + '"'
		_log.Log(gmLog.lWarn, "GnuMed user [%s] belongs to GnuMed groups [%s]." % (aUser, group_cmd))

	global known_passwords
	if not known_passwords.has_key(aUser):
		# get password for user
		print "We need a password for the GnuMed user [%s]." % aUser
		password = raw_input("Please type password: ")
		# FIXME: this assumes that "usr" is always defined before "_usr"
		known_passwords[aUser] = password
		known_passwords["_%s" % aUser] = password

	try:
		aCursor.execute("CREATE USER \"%s\" WITH PASSWORD '%s' %s VALID UNTIL '%s';" % (aUser, known_passwords[aUser], group_cmd, valid_until))
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot create GnuMed user [%s]." % aUser, exc, fatal=1)
		return None

	# paranoia is good
	if user_exists(aCursor, aUser):
		return 1

	return None
#------------------------------------------------------------------
def create_users(aCfg = None, aSection = None):
	if aCfg is None:
		cfg = _cfg
	else:
		cfg = aCfg

	if aSection is None:
		section = "defaults"
	else:
		section = aSection

	users = cfg.get(section, "users")
	if users is None:
		_log.Log(gmLog.lErr, "Cannot load GnuMed user names from config file (section = [%s])." % aSection)
		return None

	cursor = conn.cursor()
	for user in users:
		if not create_user(cursor, user):
			cursor.close()
			return None

	conn.commit()
	cursor.close()
	return 1
#------------------------------------------------------------------
def create_test_users():
	print "\nDo you want to create GnuMed database test accounts ?"
	print "This would create a few dummy accounts in the GnuMed"
	print "database that you can use to get to know things."
	print "They are NOT intended to be used in a production environment !"
	answer = None
	while answer not in ["y", "n", "yes", "no"]:
		answer = raw_input("Create test accounts ? [y/n]: ")

	if answer not in ["y", "yes"]:
		_log.Log(gmLog.lInfo, "User did not want to create test accounts.")
		return 1

	if not create_users(aSection = "test users"):
		_log.Log(gmLog.lErr, "Cannot create GnuMed test users.")
		return None
	return 1
#==================================================================
# group related
#------------------------------------------------------------------
def group_exists(aCursor, aGroup):
	try:
		aCursor.execute("SELECT groname FROM pg_group WHERE groname='%s';" % aGroup)
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot check for group existence.", exc, fatal=1)
		return None
	res = aCursor.fetchone()
	if aCursor.rowcount == 1:
		_log.Log(gmLog.lInfo, "Group %s exists." % aGroup)
		return 1
	_log.Log(gmLog.lInfo, "Group %s does not exist." % aGroup)
	return None
#------------------------------------------------------------------
def create_group(aCursor, aGroup):
	# does this group already exist ?
	if group_exists(aCursor, aGroup):
		return 1

	try:
		aCursor.execute("CREATE GROUP \"%s\";" % aGroup)
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot create GnuMed group [%s]." % aGroup, exc, fatal=1)
		return None

	# paranoia is good
	if group_exists(aCursor, aGroup):
		return 1

	return None
#------------------------------------------------------------------
def create_groups(aCfg = None, aSection = None):
	if aCfg is None:
		cfg = _cfg
	else:
		cfg = aCfg

	if aSection is None:
		section = "defaults"
	else:
		section = aSection

	groups = cfg.get(section, "groups")
	if groups is None:
		_log.Log(gmLog.lErr, "Cannot load GnuMed group names from config file (section [%s])." % section)
		return None

	cursor = conn.cursor()

	for group in groups:
		if not create_group(cursor, group):
			cursor.close()
			return None

	conn.commit()
	cursor.close()
	return 1
#==================================================================
# user _and_ group related
#------------------------------------------------------------------
def create_standard_structure():
	# create GnuMed superuser
	if not create_superuser():
		_log.Log(gmLog.lErr, "Cannot install GnuMed database owner.")
		return None

	# insert standard groups
	if not create_groups():
		_log.Log(gmLog.lErr, "Cannot create GnuMed standard groups.")
		return None

	return 1
#------------------------------------------------------------------
def create_local_structure():
	print "\nDo you want to create site-specific GnuMed database accounts ?"
	print "You will usually want to do this if you are\ninstalling a production site for real use."
	answer = None
	while answer not in ["y", "n", "yes", "no"]:
		answer = raw_input("Create site-specific accounts ? [y/n]: ")

	if answer not in ["y", "yes"]:
		_log.Log(gmLog.lInfo, "User did not want to create site-specific accounts.")
		return 1

	print "Please type the path to the config file from which\nyou want to load site-specific account definitions.\nLeave empty to abort."
	done = None
	while done is None:
		tmp = raw_input("path to config file: ")
		if tmp == "":
			_log.Log(gmLog.lInfo, "User aborted creation of site-specific accounts.")
			return 1
		fname = os.path.abspath(os.path.expanduser(tmp))
		if not os.path.exists(fname):
			print "file [%s] does not exist" % fname
		else:
			done = 1

	print "Reading site-specific accounts from [%s]." % fname

	# open local config file
	try:
		myCfg = gmCfg.cCfgFile(aFile = fname)
	except:
		exc = sys.exc_info()
		_log.LogException("Unhandled exception encountered.", exc, fatal=1)
		return None

	# create local groups
	if not create_groups(aCfg = myCfg, aSection = "site specific"):
		_log.Log(gmLog.lErr, "Cannot create site-specific GnuMed users.")
		return None

	# create local users
	if not create_users(aCfg = myCfg, aSection = "site specific"):
		_log.Log(gmLog.lErr, "Cannot create site-specific GnuMed users.")
		return None
	return 1
#==================================================================
if __name__ == "__main__":
	_log.Log(gmLog.lInfo, "startup (%s)" % __version__)
	_log.Log(gmLog.lInfo, "installing GnuMed users/groups from file [%s] (%s)" % (_cfg.get("revision control", "file"), _cfg.get("revision control", "version")))

	# connect to database
	if not connect_to_db():
		sys.exit("Cannot connect to database.\nPlease see log file for details.")

	if not verify_db():
		conn.close()
		sys.exit("Cannot verify database version.\nPlease see log file for details.")

	if not create_standard_structure():
		conn.close()
		sys.exit("Cannot create GnuMed standard user/group structure.\nPlease see log file for details.")

	# insert test users
	if not create_test_users():
		print "Cannot create GnuMed test users.\nPlease see log file for details."

	# insert site-specific users
	if not create_local_structure():
		print "Cannot create site-specific GnuMed user/group structure.\nPlease see log file for details."

	conn.close()
	_log.Log(gmLog.lInfo, "shutdown")
else:
	print "This currently isn't intended to be used as a module."
	print "Please rewrite this as a plugin for GnuMed !"
#==================================================================
# $Log: setup-users.py,v $
# Revision 1.8  2002-10-29 22:55:55  ncq
# - changed to importing from a symlink "modules" which points to client/python-common/
#
# Revision 1.7  2002/10/20 15:29:14  ncq
# - now has support for site-specific configuration in a separate file
# - remembers passwords from "usr" to "_usr"
#
# Revision 1.6  2002/10/08 14:08:37  ncq
# - seems to fully work now
#
# Revision 1.5  2002/10/04 15:49:52  ncq
# - creating groups now works, users is next
#
# Revision 1.4  2002/10/03 14:51:46  ncq
# - finally works
#
# Revision 1.3  2002/10/03 14:05:37  ncq
# - actually create the gnumed superuser
#
# Revision 1.2  2002/10/03 00:16:20  ncq
# - first real steps: connect and verify database version
#
# Revision 1.1  2002/09/30 23:06:26  ncq
# - first shot so people can see what I am getting at
#
