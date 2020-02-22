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


class wxgTagImageEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgTagImageEAPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self.SetScrollRate(10, 10)
		
		_gszr_main = wx.FlexGridSizer(3, 2, 1, 3)
		
		__lbl_name = wx.StaticText(self, wx.ID_ANY, _("Tag name"))
		__lbl_name.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		
		self._TCTRL_description = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_description.SetToolTip(_("A name for the tag.\n\nNote that there cannot be two tags with the same name."))
		_gszr_main.Add(self._TCTRL_description, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		
		__lbl_fname = wx.StaticText(self, wx.ID_ANY, _("File name"))
		_gszr_main.Add(__lbl_fname, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		
		self._TCTRL_filename = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_filename.SetToolTip(_("An example file name for this image. Mainly used for deriving a suitable file extension."))
		_gszr_main.Add(self._TCTRL_filename, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		
		__lbl_image = wx.StaticText(self, wx.ID_ANY, _("Image"))
		__lbl_image.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_image, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		
		__szr_image = wx.BoxSizer(wx.HORIZONTAL)
		_gszr_main.Add(__szr_image, 1, wx.EXPAND, 0)
		
		self._BMP_image = wx.lib.statbmp.GenStaticBitmap(self, wx.ID_ANY, wx.Bitmap(wx.Image(100, 100, clear = True)), style=wx.BORDER_SIMPLE)
		self._BMP_image.SetToolTip(_("The image to use for the tag.\n\nDo not use a big image because the tag will be downscaled anyway."))
		__szr_image.Add(self._BMP_image, 0, wx.ALIGN_CENTER | wx.ALL, 3)
		
		self._BTN_pick_image = wx.Button(self, wx.ID_ANY, _("&Pick"), style=wx.BU_EXACTFIT)
		self._BTN_pick_image.SetToolTip(_("Pick the file from which to load the tag image."))
		__szr_image.Add(self._BTN_pick_image, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		
		_gszr_main.AddGrowableCol(1)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		
		self.Layout()

		self.Bind(wx.EVT_BUTTON, self._on_pick_image_button_pressed, self._BTN_pick_image)
		# end wxGlade

	def _on_pick_image_button_pressed(self, event):  # wxGlade: wxgTagImageEAPnl.<event_handler>
		print("Event handler '_on_pick_image_button_pressed' not implemented!")
		event.Skip()

# end of class wxgTagImageEAPnl
