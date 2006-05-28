#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4cvs on Sun May 28 15:57:29 2006

import wx

class wxgSplittedEMRTreeBrowserPnl(wx.Panel):

    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmEMRBrowser

        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._splitter_browser = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.__pnl_right_side = wx.Panel(self._splitter_browser, -1, style=wx.NO_BORDER)
        self.__pnl_left_side = wx.Panel(self._splitter_browser, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._pnl_emr_tree = gmEMRBrowser.cScrolledEMRTreePnl(self.__pnl_left_side, -1)
        self._TCTRL_item_details = wx.TextCtrl(self.__pnl_right_side, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP|wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.HORIZONTAL)
        __szr_right_side = wx.BoxSizer(wx.VERTICAL)
        __szr_left_side = wx.BoxSizer(wx.VERTICAL)
        __szr_left_side.Add(self._pnl_emr_tree, 1, wx.EXPAND, 0)
        self.__pnl_left_side.SetAutoLayout(True)
        self.__pnl_left_side.SetSizer(__szr_left_side)
        __szr_left_side.Fit(self.__pnl_left_side)
        __szr_left_side.SetSizeHints(self.__pnl_left_side)
        __szr_right_side.Add(self._TCTRL_item_details, 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.__pnl_right_side.SetAutoLayout(True)
        self.__pnl_right_side.SetSizer(__szr_right_side)
        __szr_right_side.Fit(self.__pnl_right_side)
        __szr_right_side.SetSizeHints(self.__pnl_right_side)
        self._splitter_browser.SplitVertically(self.__pnl_left_side, self.__pnl_right_side)
        __szr_main.Add(self._splitter_browser, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        __szr_main.SetSizeHints(self)
        # end wxGlade

# end of class wxgSplittedEMRTreeBrowserPnl

