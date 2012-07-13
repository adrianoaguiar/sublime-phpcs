import sublime, sublime_plugin, subprocess

# Todo:
# - Make the sidebar cope with multiple selections
# - Output the results of the sidebar run to a new window, like find
# - Output the results of the save run to a unique panel, like exec
# - Make the phpcs run async to speed things up

# Run phpcs, used in other commands
def runPhpCs(path):
    command = "phpcs --standard=Made " + path
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdOut = process.communicate()[0]
    returnCode = process.returncode
    return stdOut

# run phpcs as a window command from a hotkey
class PhpcsCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        fileName = view.file_name()
        if not fileName:
            sublime.error_message("You need to save the file to disk before running phpcs")
            return
        elif fileName.endswith(".php"):
            result = runPhpCs(fileName);
            if result:
                print result
                if view.settings().get("made_phpcs_triggerconsole"):
                    view.window().run_command("show_panel", {"panel": "console"});

# run phpcs from the sidebar
class PhpcsSidebarCommand(sublime_plugin.WindowCommand):
    def run(self, paths):
        result = runPhpCs(paths[0]);
        if result:
            print result
            if self.window.active_view().settings().get("made_phpcs_triggerconsole"):
                self.window.run_command("show_panel", {"panel": "console"});
