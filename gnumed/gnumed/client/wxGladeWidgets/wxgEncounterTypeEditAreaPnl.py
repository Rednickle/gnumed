# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxgEncounterTypeEditAreaPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgEncounterTypeEditAreaPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._TCTRL_l10n_name = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_name = wx.TextCtrl(self, wx.ID_ANY, "")

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgEncounterTypeEditAreaPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._TCTRL_l10n_name.SetToolTip(_("Required: A name for this encounter type in your local language."))
		self._TCTRL_name.SetToolTip(_("Optional: A system-wide description for this encounter type. If you leave this empty the local name will be used.\n\nIt is useful to choose an English term but that is not mandatory. One advantage to using a system-wide type description is that different people can have the system description translated into their language and still use the same encounter type."))
		self._TCTRL_name.Enable(False)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgEncounterTypeEditAreaPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(2, 2, 1, 3)
		__lbl_l10n_name = wx.StaticText(self, wx.ID_ANY, _("Local name"))
		__lbl_l10n_name.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_l10n_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_l10n_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_name = wx.StaticText(self, wx.ID_ANY, _("Encounter type"))
		_gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableCol(1)
		self.Layout()
		# end wxGlade

# end of class wxgEncounterTypeEditAreaPnl
