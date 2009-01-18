import wx
import os.path


class MainWindow(wx.Frame):
    def __init__(self, filename='noname.txt'):
        super(MainWindow, self).__init__(None, size=(400,200))
        self.filename = filename
        self.dirname = '.'
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

    def CreateInteriorWindowComponents(self):
        ''' Create "interior" window components. In this case it is just a
            simple multiline text control. '''
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

    def CreateExteriorWindowComponents(self):
        ''' Create "exterior" window components, such as menu and status
            bar. '''
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
        
        # First create the file menu
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ABOUT, '&About', 'Information about this program',
                self.OnAbout),
             (wx.ID_OPEN, '&Open', 'Open a new file', self.OnOpen),
             (wx.ID_SAVE, '&Save', 'Save the current file', self.OnSave),
             (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.OnSaveAs),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
                
                
                
        
        
        # Next create the edit menu
        editMenu=wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_COPY, '&Copy', 'Copy',
                self.OnCopy),
             (wx.ID_PASTE, '&Paste', 'Paste', self.OnPaste),
             (wx.ID_CUT, '&Cut', 'Cut', self.OnCut),
             (wx.ID_PREFERENCES, '&Preferences', 'Set preference',
                self.OnPref)]:
            
                item = editMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        
            
        
        
        
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File') # Add the fileMenu to the MenuBar
        menuBar.Append(editMenu,'&Edit') # Add the Edit menu
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle('Editor %s'%self.filename)


    # Helper methods:

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle() # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    # Event handlers:

    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, 'A sample editor\n'
            'in wxPython', 'About Sample Editor', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.control.GetValue())
        textfile.close()

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.OPEN,
                                   **self.defaultFileDialogOptions()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(textfile.read())
            textfile.close()

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE,
                                   **self.defaultFileDialogOptions()):
            self.OnSave(event)
            
    def OnCopy(self,event):
        #Done this way for compatibility reasons
        # For Motif and MS Windows could use Copy()
        where = self.control.GetSelection()
        if where[0] == where[1]:
            pass
        else:
            tmp = self.control.GetString(where[0],where[-1])
            cont = wx.TextDataObject()
            cont.SetText(tmp)

            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(cont)
            wx.TheClipboard.Close()
            
             
    def OnPaste(self,event):
        if self.control.CanPaste():    
            self.control.Paste()
        else:
            pass
            
    def OnCut(self,event):
        if self.control.CanCut():
            self.control.Cut()
        else:
            pass
            
    def OnPref(self,event):
        pass

app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()