#!/usr/bin/env python
#----------------------------------------------------------------
"""
This is patient EMR pat history/notes viewer
"""
__version__ = "$Revision: 1.4 $"
__author__ = "cfmoro1976@yahoo.es"
#================================================================
import os.path, sys

from wxPython.wx import *

from Gnumed.pycommon import gmLog, gmI18N, gmPG
from Gnumed.exporters import gmPatientExporter
from Gnumed.business import gmEMRStructItems
from Gnumed.pycommon.gmPyCompat import *

_log = gmLog.gmDefLog

if __name__ == '__main__':
    _log.SetAllLogLevels(gmLog.lData)
else:
    from Gnumed.pycommon import gmGuiBroker

_log.Log(gmLog.lInfo, __version__)

#== for standalone use ==================================
if __name__ == '__main__':
    
    from Gnumed.pycommon import gmLoginInfo, gmPG, gmExceptions, gmCfg
    from Gnumed.business import gmPatient
    
    _cfg = gmCfg.gmDefCfgFile
    
    #============================================================
    class cEMRBrowser(wxPanel):
        
        def __init__(self, parent, id, exporter):
            
            """
            Contructs a new instance of EMR browser
            
            parent - Wx parent widget
            id - Wx widget id
            exporter - Patient exporter instance
            """
            
            wxPanel.__init__(self, parent, id, wxDefaultPosition, wxDefaultSize, wxRAISED_BORDER)

            self.__exporter = exporter
            
            # widget's UI initialization
            self.notes_splitter = wxSplitterWindow(self, -1)
            
            # EMR right tree
            self.__emr_tree = wxTreeCtrl(self.notes_splitter, -1, style=wxTR_HAS_BUTTONS|wxSUNKEN_BORDER)
            demo = exporter.get_patient().get_demographic_record()
            dump = demo.export_demographics(True)
            active_item = self.__emr_tree.AddRoot(dump['names'][0]['first'] + " EMR")
            self.__emr_tree.Expand(active_item)
            
            # selected encounter left dump
            self.notes_text_ctrl = wxTextCtrl(self.notes_splitter, -1, style=wxTE_MULTILINE|wxTE_READONLY|wxTE_DONTWRAP)
    
            # final widget configuration and population
            self.__set_properties()
            self.__do_layout()
            self.refresh_tree()
            
            # event handlers
            EVT_TREE_SEL_CHANGED(self.__emr_tree, self.__emr_tree.GetId(), self.__on_select)

        #--------------------------------------------------------    
        def __set_properties(self):
            """
            Configures EMR browser main properties
            """
            self.notes_splitter.SetSashPosition(150, True)
            self.notes_splitter.SetMinimumPaneSize(20)            
            self.notes_splitter.SplitVertically(self.__emr_tree, self.notes_text_ctrl)

        #--------------------------------------------------------    
        def __do_layout(self):
            """
            Arranges EMR browser layout
            """
            sizer_1 = wxBoxSizer(wxVERTICAL)
            sizer_1.Add(self.notes_splitter, 1, wxEXPAND, 0)
            self.SetAutoLayout(1)
            self.SetSizer(sizer_1)
            sizer_1.Fit(self)
            sizer_1.SetSizeHints(self)
            self.Layout()
            
        #--------------------------------------------------------
        def refresh_tree(self):
            """
            Updates EMR browser right tree
            """
            self.__exporter.get_historical_tree(self.__emr_tree)
            self.notes_text_ctrl.WriteText('Summary\n' + '=======\n\n' + \
            self.__exporter.dump_summary_info(0))
            
        #--------------------------------------------------------
        def __on_select(self, event):
            """
            Displays information for a selected tree node
            """
            sel_item = event.GetItem()
            sel_item_obj = self.__emr_tree.GetPyData(sel_item)
            self.notes_text_ctrl.Clear()
            if(isinstance(sel_item_obj, gmEMRStructItems.cEncounter)):
                episode = self.__emr_tree.GetPyData(self.__emr_tree.GetItemParent(sel_item))
                self.notes_text_ctrl.WriteText('Encounter\n' + '========\n\n' + self.__exporter.dump_encounter_info(
                    episode, sel_item_obj, 0))
            elif (isinstance(sel_item_obj, gmEMRStructItems.cEpisode)):
                self.notes_text_ctrl.WriteText('Episode\n' + '======\n\n' + self.__exporter.dump_episode_info(
                    sel_item_obj, 0))
            elif (isinstance(sel_item_obj, gmEMRStructItems.cHealthIssue)):
                self.notes_text_ctrl.WriteText('Health Issue\n' + '=========\n\n' + self.__exporter.dump_issue_info(
                    sel_item_obj, 0))
            else:
                self.notes_text_ctrl.WriteText('Summary\n' + '=======\n\n' + self.__exporter.dump_summary_info(0))
#== for plugin use ======================================
else:
    # FIXME pending
    pass    
    
#== Module convenience functions (for standalone use) =======================
#------------------------------------------------------------                
def prompted_input(prompt, default=None):
    """
    Obtains entry from standard input
    
    promp - Promt text to display in standard output
    default - Default value (for user to press only intro)
    """
    usr_input = raw_input(prompt)
    if usr_input == '':
        return default
    return usr_input
    
#------------------------------------------------------------                
def getSelectedPatient():
    """
        Main module application patient selection function.
    """
    
    # Variable initializations
    pat_searcher = gmPatient.cPatientSearcher_SQL()

    # Ask patient to dump and set in exporter object
    patient_term = prompted_input("\nPatient search term (or 'bye' to exit) (eg. Kirk): ")
    if patient_term == 'bye':
        return None
    search_ids = pat_searcher.get_patient_ids(search_term = patient_term)
    if search_ids is None or len(search_ids) == 0:
        prompted_input("No patient matches the query term. Press any key to continue.")
        return None
    elif len(search_ids) > 1:
        prompted_input("Various patients match the query term. Press any key to continue.")
        return None
    patient_id = search_ids[0]
    patient = gmPatient.gmCurrentPatient(patient_id)
    return patient
    
#================================================================
# MAIN
#----------------------------------------------------------------
if __name__ == '__main__':
    _log.Log (gmLog.lInfo, "starting emr broswer...")

    if _cfg is None:
        _log.Log(gmLog.lErr, "Cannot run without config file.")
        sys.exit("Cannot run without config file.")

    try:
        # make sure we have a db connection
        gmPG.set_default_client_encoding('latin1')
        pool = gmPG.ConnectionPool()
        
        # obtain patient
        patient = getSelectedPatient()
        if patient is None:
            print "None patient. Exiting gracefully..."
            sys.exit(0)
        
        # instantiate patient exporter
        export_tool = gmPatientExporter.cEmrExport()
        export_tool.set_patient(patient)
            
        # display standalone browser
        application = wxPyWidgetTester(size=(640,480))
        emr_browser = cEMRBrowser(application.frame, -1, export_tool)
        application.frame.Show(True)
        application.MainLoop()
        
        # clean up
        if patient is not None:
            try:
                patient.cleanup()
            except:
                print "error cleaning up patient"
    except StandardError:
        _log.LogException("unhandled exception caught !", sys.exc_info(), 1)
        # but re-raise them
        raise
    try:
        pool.StopListeners()
    except:
        _log.LogException('unhandled exception caught', sys.exc_info(), verbose=1)
        raise

    _log.Log (gmLog.lInfo, "closing emr browser...")

#================================================================
# $Log: gmEMRBrowser.py,v $
# Revision 1.4  2004-09-01 22:01:45  ncq
# - actually use Carlos' issue/episode summary code
#
# Revision 1.3  2004/08/11 09:46:24  ncq
# - now that EMR exporter supports SOAP notes - display them
#
# Revision 1.2  2004/07/26 00:09:27  ncq
# - Carlos brings us data display for the encounters - can REALLY browse EMR now !
#
# Revision 1.1  2004/07/21 12:30:25  ncq
# - initial checkin
#
