# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class mainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"學習認證自動登入", pos = wx.DefaultPosition, size = wx.Size( 500,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.elearnID_Text = wx.StaticText( self, wx.ID_ANY, u"輸入E政府帳號 :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.elearnID_Text.Wrap( -1 )

		bSizer1.Add( self.elearnID_Text, 0, wx.ALL|wx.EXPAND, 5 )

		self.elearnID_Box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.elearnID_Box, 0, wx.ALL|wx.EXPAND, 5 )

		self.elearnPW_Text = wx.StaticText( self, wx.ID_ANY, u"輸入E政府密碼:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.elearnPW_Text.Wrap( -1 )

		bSizer1.Add( self.elearnPW_Text, 0, wx.ALL|wx.EXPAND, 5 )

		self.elearnPW_Box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.elearnPW_Box, 0, wx.ALL|wx.EXPAND, 5 )


		gSizer2.Add( bSizer1, 0, wx.EXPAND, 3 )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.tchcID_Text = wx.StaticText( self, wx.ID_ANY, u"輸入台中市月嫂平台帳號 :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tchcID_Text.Wrap( -1 )

		bSizer3.Add( self.tchcID_Text, 0, wx.ALL|wx.EXPAND, 5 )

		self.tchcID_Box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.tchcID_Box, 0, wx.ALL|wx.EXPAND, 5 )

		self.tchcPW_Text = wx.StaticText( self, wx.ID_ANY, u"輸入台中市月嫂平台密碼 : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tchcPW_Text.Wrap( -1 )

		bSizer3.Add( self.tchcPW_Text, 0, wx.ALL|wx.EXPAND, 5 )

		self.tchcPW_Box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.tchcPW_Box, 0, wx.ALL|wx.EXPAND, 5 )


		gSizer2.Add( bSizer3, 1, wx.EXPAND, 3 )


		bSizer6.Add( gSizer2, 0, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.status_Text = wx.StaticText( self, wx.ID_ANY, u"狀態:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.status_Text.Wrap( -1 )

		bSizer7.Add( self.status_Text, 0, wx.ALL, 5 )

		self.status_Box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.status_Box, 1, wx.ALL|wx.EXPAND, 5 )

		self.start_Btn = wx.Button( self, wx.ID_ANY, u"開始登錄認證", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.start_Btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.start_Btn.Bind( wx.EVT_BUTTON, self.start )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def start( self, event ):
		event.Skip()


if __name__ == '__main__':
    app = wx.App()
    frm = mainFrame(None)
    frm.Show()
    app.MainLoop()