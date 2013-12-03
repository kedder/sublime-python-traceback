PythonTraceback
===============

PythonTraceback is a plug-in for Sublime Text, that allows easy navigation in
your python tracebacks.  Copy a traceback from your terminal to clipboard,
switch to Sublime Text and press `Ctrl+t`, `Ctrl+v`. New scratch buffer will be
opened with the traceback. Place the cursor on a line you want to navigate to
and press `Alt+d`: file will be opened at the line, specified in traceback.

While traceback window is open (but not necessarily active), you can navigate up
and down in traceback by pressing `Alt-k` and `Alt-j` respectively.

Pressing `Ctrl+t`, `Ctrl+v` again will replace traceback buffer with new
traceback from the clipboard.

If you are working on a project, traceback lines, that match your project'
files, will be specially marked by little dots in gutter to make it simple to
spot "own" files.

PythonTraceback will try hard to find local file that matches one, specified in
traceback, even if it does not exists directly. If at least partial path can be
found in one of your project folders, PythonTraceback will open the file for
you. This is very useful for analyzing tracebacks from remote machines, where
application is located in different directory.


Defined commands
----------------

PythonTraceback defines the following commands:

Command                 | Title                      | Default Key Binding
:-----------------------|:---------------------------|:----------------------------------------------------
`traceback_paste`       | Traceback: Paste Traceback | `Ctrl+t`, `Ctrl+v` on PC or `⌘-t`, `⌘+v` on OSX
`traceback_goto_line`   | Traceback: Go To Line      | `Alt+d`
`traceback_go_up`       | Traceback: Go Up           | `Alt+k`
`traceback_go_down`     | Traceback: Go Down         | `Alt+j`
