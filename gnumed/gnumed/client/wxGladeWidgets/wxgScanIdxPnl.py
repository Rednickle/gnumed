#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4 on Sat Nov 26 00:42:17 2005

import wx

class wxgScanIdxPnl(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgScanIdxPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.__szr_top_middle_staticbox = wx.StaticBox(self, -1, _("Properties"))
        self.__szr_top_right_staticbox = wx.StaticBox(self, -1, _("Pages"))
        self.__szr_top_left_szr_staticbox = wx.StaticBox(self, -1, _("Sources"))
        self.__btn_scan = wx.Button(self, -1, _("scan page"))
        self.__lbl_1 = wx.StaticText(self, -1, _("or"))
        self.__btn_load = wx.Button(self, -1, _("load file"))
        self.__lbl_doc_type = wx.StaticText(self, -1, _("document type:"))
        self._SelBOX_doc_type = wx.Choice(self, -1, choices=[])
        self.__lbl_doc_comment = wx.StaticText(self, -1, _("document comment:"))
        self._TBOX_doc_comment = wx.TextCtrl(self, -1, "")
        self.__lbl_doc_date = wx.StaticText(self, -1, _("document date:"))
        self._TBOX_doc_date = wx.TextCtrl(self, -1, "")
        self._LBOX_doc_pages = wx.ListBox(self, -1, choices=[], style=wx.LB_SINGLE|wx.LB_HSCROLL|wx.LB_NEEDED_SB)
        self.__btn_show_page = wx.Button(self, -1, _("show page"))
        self.__btn_del_page = wx.Button(self, -1, _("delete page"))
        self._TBOX_description = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_LINEWRAP|wx.TE_WORDWRAP|wx.NO_BORDER)
        self._ChBOX_reviewed = wx.CheckBox(self, -1, _("mark as reviewed"))
        self.__btn_save = wx.Button(self, -1, _("save"))
        self.__btn_discard = wx.Button(self, -1, _("start over"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._scan_btn_pressed, self.__btn_scan)
        self.Bind(wx.EVT_BUTTON, self._show_btn_pressed, self.__btn_show_page)
        self.Bind(wx.EVT_BUTTON, self._del_btn_pressed, self.__btn_del_page)
        self.Bind(wx.EVT_BUTTON, self._save_btn_pressed, self.__btn_save)
        self.Bind(wx.EVT_BUTTON, self._startover_btn_pressed, self.__btn_discard)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgScanIdxPnl.__set_properties
        self.__btn_scan.SetToolTipString(_("Acquire a page from an image source. This may bring up an intermediate dialog."))
        self.__btn_scan.SetDefault()
        self.__btn_load.SetToolTipString(_("Acquire a page from the filesystem."))
        self._SelBOX_doc_type.SetToolTipString(_("Required: "))
        self._SelBOX_doc_type.SetSelection(0)
        self.__btn_show_page.SetToolTipString(_("select a page to view from above list"))
        self.__btn_del_page.SetToolTipString(_("select a page to remove from above list"))
        self._TBOX_description.SetToolTipString(_("A free-text document description."))
        self._ChBOX_reviewed.SetToolTipString(_("Check this to mark the document as reviewed upon import. The default can be set by an option."))
        self.__btn_save.SetToolTipString(_("Save finished document."))
        self.__btn_discard.SetToolTipString(_("Start over (discards current data)."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgScanIdxPnl.__do_layout
        __szr_1 = wx.BoxSizer(wx.VERTICAL)
        __szr_2 = wx.BoxSizer(wx.VERTICAL)
        __szr_btm = wx.BoxSizer(wx.HORIZONTAL)
        __szr_top_left = wx.BoxSizer(wx.HORIZONTAL)
        __szr_top_right = wx.StaticBoxSizer(self.__szr_top_right_staticbox, wx.VERTICAL)
        __szr_page_actions = wx.BoxSizer(wx.HORIZONTAL)
        __szr_top_middle = wx.StaticBoxSizer(self.__szr_top_middle_staticbox, wx.VERTICAL)
        __szr_top_left_szr = wx.StaticBoxSizer(self.__szr_top_left_szr_staticbox, wx.VERTICAL)
        __szr_top_left_szr.Add(self.__btn_scan, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_top_left_szr.Add(self.__lbl_1, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        __szr_top_left_szr.Add(self.__btn_load, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_top_left.Add(__szr_top_left_szr, 0, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        __szr_top_middle.Add(self.__lbl_doc_type, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        __szr_top_middle.Add(self._SelBOX_doc_type, 0, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        __szr_top_middle.Add(self.__lbl_doc_comment, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        __szr_top_middle.Add(self._TBOX_doc_comment, 0, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE, 3)
        __szr_top_middle.Add(self.__lbl_doc_date, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        __szr_top_middle.Add(self._TBOX_doc_date, 0, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE, 3)
        __szr_top_left.Add(__szr_top_middle, 1, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        __szr_top_right.Add(self._LBOX_doc_pages, 0, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE, 3)
        __szr_page_actions.Add(self.__btn_show_page, 0, wx.ADJUST_MINSIZE, 0)
        __szr_page_actions.Add(self.__btn_del_page, 0, wx.ADJUST_MINSIZE, 0)
        __szr_top_right.Add(__szr_page_actions, 1, wx.TOP|wx.EXPAND, 4)
        __szr_top_left.Add(__szr_top_right, 1, wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        __szr_2.Add(__szr_top_left, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        __szr_2.Add(self._TBOX_description, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        __szr_btm.Add(self._ChBOX_reviewed, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        __szr_btm.Add(self.__btn_save, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_btm.Add(self.__btn_discard, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_2.Add(__szr_btm, 0, wx.LEFT|wx.BOTTOM|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        __szr_1.Add(__szr_2, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(__szr_1)
        __szr_1.Fit(self)
        __szr_1.SetSizeHints(self)
        # end wxGlade

    def _scan_btn_pressed(self, event): # wxGlade: wxgScanIdxPnl.<event_handler>
        print "Event handler `_scan_btn_pressed' not implemented"
        event.Skip()

    def _show_btn_pressed(self, event): # wxGlade: wxgScanIdxPnl.<event_handler>
        print "Event handler `_show_btn_pressed' not implemented"
        event.Skip()

    def _del_btn_pressed(self, event): # wxGlade: wxgScanIdxPnl.<event_handler>
        print "Event handler `_del_btn_pressed' not implemented"
        event.Skip()

    def _save_btn_pressed(self, event): # wxGlade: wxgScanIdxPnl.<event_handler>
        print "Event handler `_save_btn_pressed' not implemented"
        event.Skip()

    def _startover_btn_pressed(self, event): # wxGlade: wxgScanIdxPnl.<event_handler>
        print "Event handler `_startover_btn_pressed' not implemented"
        event.Skip()

# end of class wxgScanIdxPnl


