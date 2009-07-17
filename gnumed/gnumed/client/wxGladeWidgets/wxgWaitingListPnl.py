#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgWaitingListPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgWaitingListPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel, gmPatSearchWidgets, gmListWidgets

        # begin wxGlade: wxgWaitingListPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_zone = gmPatSearchWidgets.cWaitingZonePhraseWheel(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self._LBL_no_of_patients = wx.StaticText(self, -1, "")
        self._LCTRL_patients = gmListWidgets.cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.SIMPLE_BORDER)
        self._BTN_activate = wx.Button(self, -1, _("&Activate"), style=wx.BU_EXACTFIT)
        self._BTN_activateplus = wx.Button(self, -1, _("Activate&+"), style=wx.BU_EXACTFIT)
        self._BTN_add_patient = wx.Button(self, -1, _("Enlist"), style=wx.BU_EXACTFIT)
        self._BTN_remove = wx.Button(self, -1, _("Delist"), style=wx.BU_EXACTFIT)
        self._BTN_edit = wx.Button(self, -1, _("&Edit"), style=wx.BU_EXACTFIT)
        self._BTN_up = wx.Button(self, wx.ID_UP, "", style=wx.BU_EXACTFIT)
        self._BTN_down = wx.Button(self, wx.ID_DOWN, "", style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_list_item_activated, self._LCTRL_patients)
        self.Bind(wx.EVT_BUTTON, self._on_activate_button_pressed, self._BTN_activate)
        self.Bind(wx.EVT_BUTTON, self._on_activateplus_button_pressed, self._BTN_activateplus)
        self.Bind(wx.EVT_BUTTON, self._on_add_patient_button_pressed, self._BTN_add_patient)
        self.Bind(wx.EVT_BUTTON, self._on_remove_button_pressed, self._BTN_remove)
        self.Bind(wx.EVT_BUTTON, self._on_edit_button_pressed, self._BTN_edit)
        self.Bind(wx.EVT_BUTTON, self._on_up_button_pressed, self._BTN_up)
        self.Bind(wx.EVT_BUTTON, self._on_down_button_pressed, self._BTN_down)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgWaitingListPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_zone.SetToolTipString(_("Enter the waiting zone you want to filter by here.\nIf you leave this empty all waiting patients will be shown regardless of which zone they are waiting in."))
        self._LCTRL_patients.SetToolTipString(_("These patients are waiting.\n\nDoubleclick to activate (entry will stay in list)."))
        self._BTN_activate.SetToolTipString(_("Activate patient but do not remove from waiting list."))
        self._BTN_activate.Enable(False)
        self._BTN_activate.SetDefault()
        self._BTN_activateplus.SetToolTipString(_("Activate patient and remove from waiting list."))
        self._BTN_activateplus.Enable(False)
        self._BTN_add_patient.SetToolTipString(_("Add patient to the waiting list.\n\nAdds active patient (if any) if search field is empty."))
        self._BTN_remove.SetToolTipString(_("Remove selected patient from waiting list."))
        self._BTN_remove.Enable(False)
        self._BTN_edit.SetToolTipString(_("Edit details of the waiting list entry."))
        self._BTN_edit.Enable(False)
        self._BTN_up.SetToolTipString(_("Move patient up."))
        self._BTN_up.Enable(False)
        self._BTN_down.SetToolTipString(_("Move patient down."))
        self._BTN_down.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgWaitingListPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_top = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_filter = wx.StaticText(self, -1, _("Filter by:"))
        __szr_top.Add(__lbl_filter, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_zone = wx.StaticText(self, -1, _("Zone"))
        __szr_top.Add(__lbl_zone, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_top.Add(self._PRW_zone, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_top.Add(self._LBL_no_of_patients, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_top.Add((20, 20), 3, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_main.Add(__szr_top, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 3)
        __szr_main.Add(self._LCTRL_patients, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 3)
        __szr_buttons.Add((20, 20), 2, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_activate, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_activateplus, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_add_patient, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_remove, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_edit, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_up, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_buttons.Add(self._BTN_down, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 2, wx.EXPAND, 0)
        __szr_main.Add(__szr_buttons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_add_patient_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_add_patient_button_pressed' not implemented!"
        event.Skip()

    def _on_activate_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_activate_button_pressed' not implemented!"
        event.Skip()

    def _on_activateplus_button_called(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_activateplus_button_called' not implemented!"
        event.Skip()

    def _on_remove_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_remove_button_pressed' not implemented!"
        event.Skip()

    def _on_edit_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_edit_button_pressed' not implemented!"
        event.Skip()

    def _on_up_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_up_button_pressed' not implemented!"
        event.Skip()

    def _on_down_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_down_button_pressed' not implemented!"
        event.Skip()

    def _on_list_item_activated(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_list_item_activated' not implemented"
        event.Skip()

    def _on_activateplus_button_pressed(self, event): # wxGlade: wxgWaitingListPnl.<event_handler>
        print "Event handler `_on_activateplus_button_pressed' not implemented"
        event.Skip()

# end of class wxgWaitingListPnl


