#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgHealthIssueEditAreaPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgHealthIssueEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel
        from Gnumed.wxpython import gmDateTimeInput
        from Gnumed.wxpython import gmEMRStructWidgets
        from Gnumed.wxpython.gmCodingWidgets import cGenericCodesPhraseWheel

        # begin wxGlade: wxgHealthIssueEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_condition = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._ChBOX_left = wx.CheckBox(self, -1, _("left"))
        self._ChBOX_right = wx.CheckBox(self, -1, _("right"))
        self._PRW_certainty = gmEMRStructWidgets.cDiagnosticCertaintyClassificationPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_grouping = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_age_noted = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_year_noted = gmDateTimeInput.cFuzzyTimestampInput(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_status = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.NO_BORDER)
        self._ChBOX_active = wx.CheckBox(self, -1, _("Active"))
        self._ChBOX_relevant = wx.CheckBox(self, -1, _("Relevant"))
        self._ChBOX_confidential = wx.CheckBox(self, -1, _("Confidential"))
        self._ChBOX_caused_death = wx.CheckBox(self, -1, _("Caused death"))
        self._PRW_codes = cGenericCodesPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_code_details = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgHealthIssueEditAreaPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_condition.SetToolTipString(_("Enter the condition (health issue/past history item) here. Keep it short but precise."))
        self._PRW_grouping.SetToolTipString(_("Here you can add arbitrary text which will be used for sorting health issues in the tree."))
        self._PRW_age_noted.SetToolTipString(_("Enter the age in years when this condition was diagnosed. Setting this will adjust the \"in the year\" field accordingly."))
        self._PRW_year_noted.SetToolTipString(_("Enter the year when this condition was diagnosed. Setting this will adjust the \"at age\" field accordingly."))
        self._TCTRL_status.SetToolTipString(_("A summary of the state of this issue."))
        self._ChBOX_active.SetToolTipString(_("Check if this is an active, ongoing problem."))
        self._ChBOX_active.SetValue(1)
        self._ChBOX_relevant.SetToolTipString(_("Check if this is a clinically relevant problem."))
        self._ChBOX_relevant.SetValue(1)
        self._ChBOX_confidential.SetToolTipString(_("Check if this condition is to be kept confidential and not disclosed to anyone else."))
        self._ChBOX_caused_death.SetToolTipString(_("Check if this condition contributed to causing death of the patient."))
        self._PRW_codes.SetToolTipString(_("Codes relevant to this health issue\nseparated by \";\"."))
        self._TCTRL_code_details.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgHealthIssueEditAreaPnl.__do_layout
        __gszr_main = wx.FlexGridSizer(7, 2, 3, 10)
        __szr_options = wx.BoxSizer(wx.HORIZONTAL)
        __szr_diagnosed = wx.BoxSizer(wx.HORIZONTAL)
        __szr_certainty_grouping = wx.BoxSizer(wx.HORIZONTAL)
        __szr_condition = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_condition = wx.StaticText(self, -1, _("Condition"))
        __lbl_condition.SetForegroundColour(wx.Colour(255, 0, 0))
        __gszr_main.Add(__lbl_condition, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_condition.Add(self._PRW_condition, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __szr_condition.Add(self._ChBOX_left, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_condition.Add(self._ChBOX_right, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __gszr_main.Add(__szr_condition, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_certainty = wx.StaticText(self, -1, _("Certainty"))
        __gszr_main.Add(__lbl_certainty, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_certainty_grouping.Add(self._PRW_certainty, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_group = wx.StaticText(self, -1, _("Grouping:"))
        __szr_certainty_grouping.Add(__lbl_group, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_certainty_grouping.Add(self._PRW_grouping, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __gszr_main.Add(__szr_certainty_grouping, 1, wx.EXPAND, 0)
        __lbl_noted = wx.StaticText(self, -1, _("When Noted"))
        __gszr_main.Add(__lbl_noted, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_age = wx.StaticText(self, -1, _("Age:"), style=wx.ALIGN_RIGHT)
        __szr_diagnosed.Add(__lbl_age, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_diagnosed.Add(self._PRW_age_noted, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_year = wx.StaticText(self, -1, _("Or year:"), style=wx.ALIGN_RIGHT)
        __szr_diagnosed.Add(__lbl_year, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_diagnosed.Add(self._PRW_year_noted, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(__szr_diagnosed, 1, wx.EXPAND, 0)
        __lbl_status = wx.StaticText(self, -1, _("Synopsis"))
        __gszr_main.Add(__lbl_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._TCTRL_status, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add((1, 1), 0, wx.EXPAND, 0)
        __szr_options.Add(self._ChBOX_active, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_options.Add(self._ChBOX_relevant, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_options.Add(self._ChBOX_confidential, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_options.Add(self._ChBOX_caused_death, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __gszr_main.Add(__szr_options, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_codes = wx.StaticText(self, -1, _("Codes"))
        __gszr_main.Add(__lbl_codes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._PRW_codes, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add((20, 20), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __gszr_main.Add(self._TCTRL_code_details, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(__gszr_main)
        __gszr_main.Fit(self)
        __gszr_main.AddGrowableRow(3)
        __gszr_main.AddGrowableRow(6)
        __gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgHealthIssueEditAreaPnl


