#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgIdentityEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgIdentityEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmDemographicsWidgets, gmDateTimeInput

        # begin wxGlade: wxgIdentityEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LBL_info = wx.StaticText(self, -1, "")
        self._PRW_dob = gmDateTimeInput.cFuzzyTimestampInput(self, -1, "", style=wx.NO_BORDER)
        self._DP_dod = gmDateTimeInput.cDateInputCtrl(self, -1, style=wx.DP_DROPDOWN|wx.DP_ALLOWNONE|wx.DP_SHOWCENTURY)
        self._PRW_gender = gmDemographicsWidgets.cGenderSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_ethnicity = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_title = gmDemographicsWidgets.cTitlePhraseWheel(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgIdentityEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_dob.SetToolTipString(_("The date of birth for this person."))
        self._DP_dod.SetToolTipString(_("The date of death."))
        self._PRW_ethnicity.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgIdentityEAPnl.__do_layout
        __gzszr_main = wx.FlexGridSizer(6, 2, 1, 3)
        __lbl_name = wx.StaticText(self, -1, _("Status"))
        __gzszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._LBL_info, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_dob = wx.StaticText(self, -1, _("Born"))
        __gzszr_main.Add(__lbl_dob, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._PRW_dob, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_dod = wx.StaticText(self, -1, _("Deceased"))
        __gzszr_main.Add(__lbl_dod, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._DP_dod, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_gender = wx.StaticText(self, -1, _("Gender"))
        __gzszr_main.Add(__lbl_gender, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._PRW_gender, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_ethnicity = wx.StaticText(self, -1, _("Ethnicity"))
        __gzszr_main.Add(__lbl_ethnicity, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._PRW_ethnicity, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_title = wx.StaticText(self, -1, _("Title"))
        __gzszr_main.Add(__lbl_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzszr_main.Add(self._PRW_title, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(__gzszr_main)
        __gzszr_main.Fit(self)
        __gzszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgIdentityEAPnl


