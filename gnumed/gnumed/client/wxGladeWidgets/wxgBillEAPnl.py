#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.5 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgBillEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade


class wxgBillEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmDateTimeInput import cDateInputPhraseWheel
        from Gnumed.wxpython.gmAddressWidgets import cAddressPhraseWheel

        # begin wxGlade: wxgBillEAPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._TCTRL_invoice_id = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self._PRW_close_date = cDateInputPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_address = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self._BTN_select_address = wx.Button(self, -1, _("&Select"), style=wx.BU_EXACTFIT)
        self._TCTRL_value = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self._CHBOX_vat_applies = wx.CheckBox(self, -1, _("&VAT applies"))
        self._TCTRL_value_with_vat = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_select_address_button_pressed, self._BTN_select_address)
        self.Bind(wx.EVT_CHECKBOX, self._on_vat_applies_box_checked, self._CHBOX_vat_applies)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgBillEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._TCTRL_invoice_id.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_invoice_id.SetToolTipString(_("The invoice ID.\n\nNote that in most jurisdictions this must be a unique entity.\n\nGNUmed will create one for you."))
        self._PRW_close_date.SetToolTipString(_("The close date of the bill.\n\nWhen a bill is closed items shall not be added to it anymore."))
        self._TCTRL_address.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_address.SetToolTipString(_("Where to send the bill."))
        self._BTN_select_address.SetToolTipString(_("Select the address where to send the bill."))
        self._TCTRL_value.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_value.SetToolTipString(_("The total value of this bill without VAT applied."))
        self._CHBOX_vat_applies.SetToolTipString(_("Select here whether or not to apply VAT when creating an invoice for this bill."))
        self._TCTRL_value_with_vat.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_value_with_vat.SetToolTipString(_("The total value of this bill after VAT has been applied."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgBillEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(4, 2, 1, 3)
        __szr_value_details = wx.BoxSizer(wx.HORIZONTAL)
        __szr_address_details = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_invoice_id = wx.StaticText(self, -1, _("Invoice ID"))
        __lbl_invoice_id.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_invoice_id, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_invoice_id, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __close_date = wx.StaticText(self, -1, _("Close date"))
        __close_date.SetForegroundColour(wx.Colour(255, 127, 0))
        _gszr_main.Add(__close_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_close_date, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_address = wx.StaticText(self, -1, _("Address"))
        __lbl_address.SetForegroundColour(wx.Colour(255, 127, 0))
        _gszr_main.Add(__lbl_address, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_address_details.Add(self._TCTRL_address, 1, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_address_details.Add(self._BTN_select_address, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_address_details, 1, wx.EXPAND, 0)
        __lbl_value = wx.StaticText(self, -1, _("Value"))
        _gszr_main.Add(__lbl_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_value_details.Add(self._TCTRL_value, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_value_details.Add(self._CHBOX_vat_applies, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_value_details.Add(self._TCTRL_value_with_vat, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        _gszr_main.Add(__szr_value_details, 1, wx.EXPAND, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

    def _on_vat_applies_box_checked(self, event):  # wxGlade: wxgBillEAPnl.<event_handler>
        print "Event handler `_on_vat_applies_box_checked' not implemented!"
        event.Skip()

    def _on_select_address_button_pressed(self, event):  # wxGlade: wxgBillEAPnl.<event_handler>
        print "Event handler `_on_select_address_button_pressed' not implemented"
        event.Skip()

# end of class wxgBillEAPnl
