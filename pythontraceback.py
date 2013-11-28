import re

import sublime
import sublime_plugin

TRACEBACK_WINDOW_NAME = '* traceback *'
LINE_REGEXP = re.compile(r'"(.*)", line (\d+)')


class TracebackPasteCommand(sublime_plugin.WindowCommand):
    """Paste traceback into new window

    Paste clipboard contents (assuming clipboard contains python traceback,
    copied from console) to a dedicated transient window.
    """
    def run(self, *args):
        v = self.find_traceback_view()
        if not v:
            # Create new traceback view
            self.window.new_file(sublime.TRANSIENT)
            v = self.window.active_view()
            v.set_name(TRACEBACK_WINDOW_NAME)
            v.set_scratch(True)
        else:
            # Clear existing traceback view before pasting new traceback
            v.set_read_only(False)
            v.run_command("select_all")
            v.run_command("right_delete")

        v.run_command('paste')
        v.set_read_only(True)
        # Python syntax file fits well with tracebacks
        v.set_syntax_file('Packages/Python/Python.tmLanguage')
        self.window.focus_view(v)

    def find_traceback_view(self):
        for w in self.window.views():
            if w.name() == TRACEBACK_WINDOW_NAME:
                return w
        return None


class TracebackGotoLine(sublime_plugin.TextCommand):
    """Open file under cursor in traceback window and set curser on
    appropriate line.
    """
    def run(self, edit):
        for region in self.view.sel():
            line = self.view.line(region)
            line_contents = self.view.substr(line)

            filename, linenum = self.parse_line(line_contents)
            if filename is None:
                sublime.status_message("Traceback line is not identified.")
                continue

            self.open_file(filename, linenum)

    def parse_line(self, line):
        not_found = None, None
        if not line:
            return not_found

        m = LINE_REGEXP.search(line)
        if not m:
            return not_found

        filename, lnum = m.groups()
        return filename, int(lnum)

    def open_file(self, filename, linenum):
        window = sublime.active_window()
        window.open_file("%s:%s" % (filename, linenum),
                         sublime.ENCODED_POSITION)


class ActionContextHandler(sublime_plugin.EventListener):
    """Provide special `python_traceback` context in traceback window

    So that plugin could provide traceback specific bindings.
    """
    def on_query_context(self, view, key, op, operand, match_all):
        if not key.startswith('python_traceback'):
            return None

        return view.name() == TRACEBACK_WINDOW_NAME
