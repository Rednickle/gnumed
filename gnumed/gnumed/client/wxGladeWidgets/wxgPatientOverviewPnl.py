#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgPatientOverviewPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgPatientOverviewPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmListWidgets import cReportListCtrl
        from Gnumed.wxpython import gmDateTimeInput

        # begin wxGlade: wxgPatientOverviewPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LCTRL_identity = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_contacts = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._PRW_encounter_range = gmDateTimeInput.cIntervalPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._LCTRL_encounters = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_problems = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_meds = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_history = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_inbox = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_results = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)
        self._LCTRL_documents = cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.SIMPLE_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgPatientOverviewPnl.__set_properties
        self.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgPatientOverviewPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.HORIZONTAL)
        __szr_right = wx.BoxSizer(wx.VERTICAL)
        __szr_middle = wx.BoxSizer(wx.VERTICAL)
        __szr_left = wx.BoxSizer(wx.VERTICAL)
        __szr_encounters = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_identity = wx.StaticText(self, -1, _("Identity:"))
        __szr_left.Add(__lbl_identity, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_left.Add(self._LCTRL_identity, 1, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_contacts = wx.StaticText(self, -1, _("Contacts:"))
        __szr_left.Add(__lbl_contacts, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_left.Add(self._LCTRL_contacts, 1, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_encounters = wx.StaticText(self, -1, _("Encounters / admissions (last"))
        __szr_encounters.Add(__lbl_encounters, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        __szr_encounters.Add(self._PRW_encounter_range, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
        __lbl_closing_brace = wx.StaticText(self, -1, _("):"))
        __szr_encounters.Add(__lbl_closing_brace, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_left.Add(__szr_encounters, 0, wx.BOTTOM|wx.EXPAND, 3)
        __szr_left.Add(self._LCTRL_encounters, 1, wx.EXPAND, 5)
        __szr_main.Add(__szr_left, 1, wx.RIGHT|wx.EXPAND, 5)
        __lbl_problem_list = wx.StaticText(self, -1, _("Active Problems:"))
        __szr_middle.Add(__lbl_problem_list, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_middle.Add(self._LCTRL_problems, 2, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_meds = wx.StaticText(self, -1, _("Current meds and substances:"))
        __szr_middle.Add(__lbl_meds, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_middle.Add(self._LCTRL_meds, 2, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_history = wx.StaticText(self, -1, _("History:"))
        __szr_middle.Add(__lbl_history, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_middle.Add(self._LCTRL_history, 3, wx.EXPAND, 5)
        __szr_main.Add(__szr_middle, 1, wx.RIGHT|wx.EXPAND, 5)
        __lbl_inbox = wx.StaticText(self, -1, _("Inbox / Scratch pad:"))
        __szr_right.Add(__lbl_inbox, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_right.Add(self._LCTRL_inbox, 1, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_measurements = wx.StaticText(self, -1, _("Measurements:"))
        __szr_right.Add(__lbl_measurements, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_right.Add(self._LCTRL_results, 2, wx.BOTTOM|wx.EXPAND, 5)
        __lbl_documents = wx.StaticText(self, -1, _("Unsigned documents:"))
        __szr_right.Add(__lbl_documents, 0, wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_right.Add(self._LCTRL_documents, 1, wx.EXPAND, 5)
        __szr_main.Add(__szr_right, 1, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

# end of class wxgPatientOverviewPnl


