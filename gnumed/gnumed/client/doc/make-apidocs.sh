#!/bin/sh

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/doc/make-apidocs.sh,v $
# $Revision: 1.4 $
# license: GPL
# author: Karsten.Hilbert@gmx.net

BASE="~/gnumed/gnumed/client"
MODULES="$BASE/business/ $BASE/connectors/ $BASE/exporters/ $BASE/importers/ $BASE/pycommon/"

export DISPLAY=":0.0"
nice -n 19 epydoc -n GnuMed -u http://www.gnumed.org --no-private -o ~/gm-apidocs $MODULES

#============================================
# $Log: make-apidocs.sh,v $
# Revision 1.4  2005-02-15 12:01:20  ncq
# - since there is no easy answer to cronning epydoc over wxPython
#   exclude that for now such that we at least get the rest of the
#   API epydoced regularly
#
# Revision 1.3  2005/01/19 09:27:59  ncq
# - let callers deal with output, don't predefine target as file (cron mails it)
#
# Revision 1.2  2005/01/09 15:58:56  ncq
# - add export DISPLAY to make epydoc think it can open the local display for importing wx to succeed
#
# Revision 1.1  2004/07/14 10:11:04  ncq
# - first checkin
#
