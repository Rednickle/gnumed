#!/bin/sh

#==============================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/Attic/backup-gnumed-database.sh,v $
# $Id: backup-gnumed-database.sh,v 1.5 2007-01-24 22:56:05 ncq Exp $
#
# author: Karsten Hilbert
# license: GPL v2
#==============================================================

PGDATABASE="gnumed_v5"
PGPASSWORD="need to set this"

# where to eventually put the backups
BACKUP_DIR="/root/"

# user/group the backup is eventually owned by
BACKUP_OWNER="$USER.$USER"

# file permissions mask to set the backup file to
BACKUP_MASK="0600"

# identify the logical/business-level owner of this
# GNUmed database instance, such as "ACME GP Office",
# do not use spaces: "ACME_GP_Offices"
INSTANCE_OWNER="GNUmed_Team"

# set this to an email address which will receive
# digitally signed replies from the GNotary server
# notarizing the hash of the backup
SIG_RECEIVER="root"

# set this to the email address of the GNotary server
# you want your hashes to be signed by
GNOTARY_SERVER="gnotary@gnotary.de"

# you will have to set the GNotary TAN here, using
# "free" works but makes you a Freeloader, as it is
# mainly intended for testing
GNOTARY_TAN="free"

# it is useful to have a PROCMAIL rule for the replies
# piping them into the stoarage area where the backups
# are kept

#==============================================================
# There really should not be any need to
# change anything below this line.
#==============================================================

TS=`date +%Y-%m-%d-%H-%M-%S`
HOST=`hostname`
BACKUP_FILE="$BACKUP_DIR/backup-$PGDATABASE-$INSTANCE_OWNER-$HOST-$TS.sql"

# create dump
PGUSER="gm-dbo"
PGPORT="5432"
pg_dump -f $BACKUP_FILE

# give to admin owner
chmod $BACKUP_MASK $BACKUP_FILE
chown $BACKUP_OWNER $BACKUP_FILE

# GNotary support
LOCAL_MAILER=`which mail`

#SHA512="SHA 512:"`sha512sum -b $BACKUP_FILE`
SHA512=`openssl dgst -sha512 -hex $BACKUP_FILE`
RMD160=`openssl dgst -ripemd160 -hex $BACKUP_FILE`

export REPLYTO=$SIG_RECEIVER
#export USER="karsten.hilbert@gmx.net"

# send mail
(
	echo "Subject: gnotarize"
	echo " "
	echo "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>"
	echo "<message>"
	echo "	<tan>$GNOTARY_TAN</tan>"
	echo "	<action>notarize</action>"
	echo "	<hashes number=\"2\">"
	echo "		<hash file=\"$BACKUP_FILE\" modified=\"$TS\" algorithm=\"SHA-512\">$SHA512</hash>"
	echo "		<hash file=\"$BACKUP_FILE\" modified=\"$TS\" algorithm=\"RIPE-MD-160\">$RMD160</hash>"
	echo "	</hashes>"
	echo "</message>"
	echo " "
) | $LOCAL_MAILER -s "gnotarize" $GNOTARY_SERVER


exit 0

#==============================================================
# $Log: backup-gnumed-database.sh,v $
# Revision 1.5  2007-01-24 22:56:05  ncq
# - support gnotarization
#
# Revision 1.4  2007/01/07 23:10:24  ncq
# - more documentation
# - add backup file permission mask
#
# Revision 1.3  2006/12/25 22:55:10  ncq
# - comment on gnotary support
#
# Revision 1.2  2006/12/21 19:01:21  ncq
# - add target owner chown
#
# Revision 1.1  2006/12/05 14:48:08  ncq
# - first release of a backup script
#
#