# Py2EXE Studio — Made by Black Baccara Rose
# https://black-baccara-rose.netlify.app/
import os
import sys
import queue
import threading
import subprocess
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime

APP_NAME = "Py2EXE Studio"
AUTHOR = "Black Baccara Rose"
AUTHOR_URL = "https://black-baccara-rose.netlify.app/"

# --- Black Baccara Rose theme (dark / terminal / rose) ---
BG = "#050506"
PANEL = "#0b0b0f"
PANEL_2 = "#15151b"
BORDER = "#2a1620"
TEXT = "#e8e6ea"
MUTED = "#8a8190"
ACCENT = "#e11d48"
ACCENT_HOVER = "#ff3d6b"
ACCENT_DIM = "#7a1230"
INPUT_BG = "#07070a"
LOG_BG = "#030304"
GREEN = "#3ddc84"
RED = "#ff4d6d"
YELLOW = "#f6c768"
MONO = "Consolas"

# Embedded logo (from P.ico) — no external file needed, works inside the built .exe
LOGO_HEADER_B64 = (
    "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"
    "QmCC"
)
LOGO_ICON_B64 = (
    "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"
)


class Py2ExeStudio:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME}  //  {AUTHOR}")
        self.root.geometry("920x800")
        self.root.minsize(800, 720)
        self.root.configure(bg=BG)
        self._set_window_icon()

        self.source_var = tk.StringVar()
        self.icon_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        self.name_var = tk.StringVar()
        self.onefile_var = tk.BooleanVar(value=True)
        self.console_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Ready to build")
        self.progress_var = tk.DoubleVar(value=0)
        self.events = queue.Queue()
        self.building = False
        self.process = None
        self.cursor_on = True

        self._setup_styles()
        self._build_ui()
        self.root.after(100, self._poll_events)
        self.root.after(600, self._blink)
        self._log("Welcome to Py2EXE Studio.")
        self._log("Select a .py file, review the options, then click Build Executable.")
        self._log(f"Made by {AUTHOR} — {AUTHOR_URL}")

    def _set_window_icon(self):
        try:
            self.icon_img = tk.PhotoImage(data=LOGO_ICON_B64)
            self.root.iconphoto(True, self.icon_img)
        except Exception:
            pass

    # ------------------------------------------------------------ styles
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Studio.Horizontal.TProgressbar",
            troughcolor=PANEL_2, background=ACCENT, bordercolor=BORDER,
            lightcolor=ACCENT, darkcolor=ACCENT, thickness=8
        )
        style.configure(
            "Rose.Vertical.TScrollbar",
            background=PANEL_2, troughcolor=LOG_BG, bordercolor=LOG_BG,
            arrowcolor=ACCENT, lightcolor=PANEL_2, darkcolor=PANEL_2
        )
        style.map("Rose.Vertical.TScrollbar", background=[("active", ACCENT_DIM)])

    def _label(self, parent, text="", **kwargs):
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", PANEL),
                        fg=kwargs.pop("fg", TEXT), font=kwargs.pop("font", (MONO, 10)),
                        **kwargs)

    def _entry(self, parent, variable, **kwargs):
        return tk.Entry(parent, textvariable=variable, bg=INPUT_BG, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER, highlightcolor=ACCENT,
                        font=(MONO, 10), **kwargs)

    def _button(self, parent, text, command, primary=False, width=None):
        bg = ACCENT if primary else PANEL_2
        hover = ACCENT_HOVER if primary else "#211620"
        btn = tk.Button(parent, text=text, command=command, bg=bg,
                        fg="#ffffff" if primary else TEXT,
                        activebackground=hover, activeforeground="#ffffff",
                        disabledforeground="#c9a0ad",
                        relief="flat", bd=0, cursor="hand2", font=(MONO, 10, "bold"),
                        highlightthickness=1,
                        highlightbackground=ACCENT if primary else BORDER,
                        highlightcolor=ACCENT, padx=14, pady=9, width=width)

        def on_enter(_):
            if str(btn["state"]) != "disabled":
                btn.configure(bg=hover)

        def on_leave(_):
            btn.configure(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _check(self, parent, text, variable):
        lbl = tk.Label(parent, bg=PANEL, fg=TEXT, font=(MONO, 9), cursor="hand2")

        def render(*_):
            on = variable.get()
            lbl.configure(text=f"[{'x' if on else ' '}]  {text}",
                          fg=ACCENT_HOVER if on else TEXT)

        lbl.bind("<Button-1>", lambda e: variable.set(not variable.get()))
        variable.trace_add("write", render)
        render()
        return lbl

    def _section(self, parent, num, text):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 7))
        self._label(row, f"// {num} — ", bg=BG, fg=ACCENT,
                    font=(MONO, 9, "bold")).pack(side="left")
        self._label(row, text.upper(), bg=BG, fg=MUTED,
                    font=(MONO, 9, "bold")).pack(side="left")

    def _panel(self, parent, **pack):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="x", **pack)
        return frame

    def _open_author(self, _event=None):
        webbrowser.open(AUTHOR_URL)

    def _blink(self):
        self.cursor_on = not self.cursor_on
        self.prompt_label.configure(
            text="root@blackbaccara:~$ sudo bloom --force" + ("█" if self.cursor_on else " "))
        self.root.after(600, self._blink)

    # ------------------------------------------------------------ UI
    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=26, pady=(20, 12))

        try:
            self.logo_img = tk.PhotoImage(data=LOGO_HEADER_B64)
            logo = tk.Label(header, image=self.logo_img, bg=BG, bd=0)
        except Exception:
            logo = self._label(header, "Py2EX", bg=BG, fg=ACCENT, font=(MONO, 14, "bold"))
        logo.pack(side="left")

        title_area = tk.Frame(header, bg=BG)
        title_area.pack(side="left", padx=14)
        self.prompt_label = self._label(title_area, "root@blackbaccara:~$ sudo bloom --force█",
                                        bg=BG, fg=GREEN, font=(MONO, 9))
        self.prompt_label.pack(anchor="w")
        title_row = tk.Frame(title_area, bg=BG)
        title_row.pack(anchor="w")
        self._label(title_row, "Py2", bg=BG, font=(MONO, 21, "bold")).pack(side="left")
        self._label(title_row, "EXE", bg=BG, fg=ACCENT, font=(MONO, 21, "bold")).pack(side="left")
        self._label(title_row, " Studio", bg=BG, font=(MONO, 21, "bold")).pack(side="left")
        self._label(title_area, "Python script  →  Windows executable", bg=BG,
                    fg=MUTED, font=(MONO, 9)).pack(anchor="w")

        right = tk.Frame(header, bg=BG)
        right.pack(side="right", anchor="center")
        self._label(right, "[ BUILD TOOL ]", bg=BG, fg=GREEN,
                    font=(MONO, 9, "bold")).pack(anchor="e")
        by = tk.Frame(right, bg=BG)
        by.pack(anchor="e", pady=(3, 0))
        self._label(by, "made by ", bg=BG, fg=MUTED, font=(MONO, 8)).pack(side="left")
        link = self._label(by, AUTHOR, bg=BG, fg=ACCENT_HOVER,
                           font=(MONO, 8, "underline"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", self._open_author)

        tk.Frame(self.root, bg=ACCENT_DIM, height=1).pack(fill="x", padx=26, pady=(0, 14))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=26, pady=(0, 14))

        self._section(body, "01", "Source file")
        source_row = self._panel(body, pady=(0, 14))
        self._entry(source_row, self.source_var).pack(side="left", fill="x", expand=True,
                                                       padx=(12, 8), pady=12, ipady=7)
        self._button(source_row, "Browse .py", self._browse_source).pack(side="right", padx=(0, 12), pady=10)

        self._section(body, "02", "Build configuration")
        config = self._panel(body, pady=(0, 14))

        icon_row = tk.Frame(config, bg=PANEL)
        icon_row.pack(fill="x", padx=12, pady=(12, 7))
        self._label(icon_row, "Application icon", bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 14))
        self._entry(icon_row, self.icon_var).pack(side="left", fill="x", expand=True, ipady=6)
        self._button(icon_row, "Browse .ico", self._browse_icon).pack(side="left", padx=(8, 0))

        name_row = tk.Frame(config, bg=PANEL)
        name_row.pack(fill="x", padx=12, pady=7)
        self._label(name_row, "EXE name", bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 55))
        self._entry(name_row, self.name_var).pack(side="left", fill="x", expand=True, ipady=6)

        options = tk.Frame(config, bg=PANEL)
        options.pack(fill="x", padx=12, pady=(7, 12))
        self._check(options, "One-file executable", self.onefile_var).pack(side="left", padx=(0, 26))
        self._check(options, "Show console window", self.console_var).pack(side="left")

        self._section(body, "03", "Output location")
        out_row = self._panel(body, pady=(0, 14))
        self._entry(out_row, self.output_var).pack(side="left", fill="x", expand=True,
                                                    padx=(12, 8), pady=12, ipady=7)
        self._button(out_row, "Choose folder", self._browse_output).pack(side="right", padx=(0, 12), pady=10)

        actions = tk.Frame(body, bg=BG)
        actions.pack(fill="x", pady=(0, 13))
        self.build_btn = self._button(actions, "▶  BUILD EXECUTABLE", self._start_build, primary=True)
        self.build_btn.pack(side="left")
        self._button(actions, "Clear logs", self._clear_logs).pack(side="left", padx=8)
        self._button(actions, "Open output", self._open_output).pack(side="left")
        self._label(actions, "powered by PyInstaller", bg=BG, fg=MUTED,
                    font=(MONO, 9)).pack(side="right", anchor="center")

        status = self._panel(body, pady=(0, 12))
        status_top = tk.Frame(status, bg=PANEL)
        status_top.pack(fill="x", padx=12, pady=(10, 5))
        self.status_dot = self._label(status_top, "●", bg=PANEL, fg=GREEN, font=(MONO, 10))
        self.status_dot.pack(side="left")
        self._label(status_top, "  // BUILD STATUS", bg=PANEL, fg=MUTED,
                    font=(MONO, 9, "bold")).pack(side="left")
        self._label(status_top, textvariable=self.status_var, bg=PANEL,
                    fg=TEXT, font=(MONO, 9)).pack(side="right")
        self.progress = ttk.Progressbar(status, style="Studio.Horizontal.TProgressbar",
                                        variable=self.progress_var, maximum=100, mode="indeterminate")
        self.progress.pack(fill="x", padx=12, pady=(0, 11))

        log_head = tk.Frame(body, bg=BG)
        log_head.pack(fill="x", pady=(0, 6))
        self._label(log_head, "$ tail -f build.log", bg=BG, fg=GREEN,
                    font=(MONO, 10, "bold")).pack(side="left")
        self._label(log_head, "live output", bg=BG, fg=MUTED,
                    font=(MONO, 9)).pack(side="right")

        log_frame = tk.Frame(body, bg=LOG_BG, highlightbackground=BORDER, highlightthickness=1)
        log_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_frame, bg=LOG_BG, fg="#c9c2cf", insertbackground=ACCENT,
                                relief="flat", bd=0, wrap="word", font=(MONO, 9),
                                padx=12, pady=10, state="disabled", highlightthickness=0)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview,
                                  style="Rose.Vertical.TScrollbar")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.log_text.tag_configure("ts", foreground=MUTED)
        self.log_text.tag_configure("ok", foreground=GREEN)
        self.log_text.tag_configure("err", foreground=RED)
        self.log_text.tag_configure("cmd", foreground=ACCENT_HOVER)

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(side="bottom", fill="x", padx=26, pady=(0, 12), before=body)
        self._label(footer, "Tip: build on Windows for the most reliable Windows .exe output.",
                    bg=BG, fg=MUTED, font=(MONO, 8)).pack(side="left")
        credit = tk.Frame(footer, bg=BG)
        credit.pack(side="right")
        self._label(credit, "© ", bg=BG, fg=MUTED, font=(MONO, 8)).pack(side="left")
        link = self._label(credit, AUTHOR.upper(), bg=BG, fg=ACCENT_HOVER,
                           font=(MONO, 8, "bold underline"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", self._open_author)
        self._label(credit, " — internet is open to all {^-^}", bg=BG, fg=MUTED,
                    font=(MONO, 8)).pack(side="left")

    # ------------------------------------------------------------ actions
    def _browse_source(self):
        path = filedialog.askopenfilename(title="Choose Python script",
                                          filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if path:
            self.source_var.set(path)
            if not self.name_var.get().strip():
                self.name_var.set(Path(path).stem)
            self._log(f"Selected source: {path}")

    def _browse_icon(self):
        path = filedialog.askopenfilename(title="Choose application icon",
                                          filetypes=[("Icon files", "*.ico")])
        if path:
            self.icon_var.set(path)
            self._log(f"Selected icon: {path}")

    def _browse_output(self):
        path = filedialog.askdirectory(title="Choose output folder")
        if path:
            self.output_var.set(path)

    def _log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        tag = None
        if message.startswith("SUCCESS"):
            tag = "ok"
        elif message.startswith("ERROR") or " ERROR" in message[:20]:
            tag = "err"
        elif message.startswith("Command:") or message.startswith("Build started"):
            tag = "cmd"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}]  ", "ts")
        self.log_text.insert("end", f"{message}\n", tag) if tag else self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_logs(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _open_output(self):
        folder = self.output_var.get().strip()
        if not folder or not Path(folder).exists():
            messagebox.showwarning("Output folder", "Choose an existing output folder first.")
            return
        try:
            os.startfile(folder)
        except Exception as exc:
            messagebox.showerror("Cannot open folder", str(exc))

    def _start_build(self):
        if self.building:
            return
        source = Path(self.source_var.get().strip().strip('"'))
        output = Path(self.output_var.get().strip().strip('"'))
        icon_text = self.icon_var.get().strip().strip('"')
        name = self.name_var.get().strip()

        if not source.is_file() or source.suffix.lower() != ".py":
            messagebox.showerror("Source file required", "Select a valid .py file first.")
            return
        if not output.is_dir():
            messagebox.showerror("Output folder required", "Choose an existing output folder.")
            return
        if icon_text and (not Path(icon_text).is_file() or Path(icon_text).suffix.lower() != ".ico"):
            messagebox.showerror("Invalid icon", "Select a valid .ico file or leave the icon field empty.")
            return
        if not name:
            name = source.stem
            self.name_var.set(name)
        if any(c in name for c in r'\/:*?"<>|') or name in {".", ".."}:
            messagebox.showerror("Invalid EXE name", "Use a file name without: \\ / : * ? \" < > |")
            return

        try:
            import PyInstaller  # noqa: F401
        except ImportError:
            messagebox.showerror(
                "PyInstaller not installed",
                "Install dependencies first by running:\n\npy -m pip install -r requirements.txt"
            )
            return

        self.building = True
        self.build_btn.configure(state="disabled", text="BUILDING…")
        self.status_var.set("Building executable…")
        self.status_dot.configure(fg=YELLOW)
        self.progress.configure(mode="indeterminate")
        self.progress.start(10)
        self._log("-" * 55)
        self._log(f"Build started for {source.name}")
        self._log(f"Output folder: {output}")
        self._log(f"One-file mode: {'enabled' if self.onefile_var.get() else 'disabled'}")
        self._log(f"Console: {'visible' if self.console_var.get() else 'hidden'}")

        args = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
                "--name", name, "--distpath", str(output),
                "--workpath", str(output / "_py2exe_build" / "work"),
                "--specpath", str(output / "_py2exe_build" / "spec")]
        if self.onefile_var.get():
            args.append("--onefile")
        else:
            args.append("--onedir")
        if not self.console_var.get():
            args.append("--windowed")
        if icon_text:
            args.extend(["--icon", icon_text])
        args.append(str(source))

        thread = threading.Thread(target=self._run_build, args=(args, output, name), daemon=True)
        thread.start()

    def _run_build(self, args, output, name):
        try:
            self.events.put(("log", "Command: " + subprocess.list2cmdline(args)))
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
            self.process = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                bufsize=1, creationflags=creationflags
            )
            for line in self.process.stdout:
                self.events.put(("log", line.rstrip()))
            code = self.process.wait()
            expected = output / (name + ".exe") if self.onefile_var.get() else output / name / (name + ".exe")
            if code == 0 and expected.exists():
                self.events.put(("done", str(expected)))
            elif code == 0:
                self.events.put(("done", f"Build finished. Check output folder: {output}"))
            else:
                self.events.put(("error", f"PyInstaller exited with code {code}. Check the log above."))
        except Exception as exc:
            self.events.put(("error", str(exc)))

    def _poll_events(self):
        try:
            while True:
                event, payload = self.events.get_nowait()
                if event == "log":
                    self._log(payload)
                elif event == "done":
                    self._finish_build(True, payload)
                elif event == "error":
                    self._finish_build(False, payload)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_events)

    def _finish_build(self, success, message):
        self.building = False
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress_var.set(100 if success else 0)
        self.build_btn.configure(state="normal", text="▶  BUILD EXECUTABLE")
        if success:
            self.status_var.set("Build completed")
            self.status_dot.configure(fg=GREEN)
            self._log("SUCCESS: " + message)
            messagebox.showinfo("Build complete", message)
        else:
            self.status_var.set("Build failed")
            self.status_dot.configure(fg=RED)
            self._log("ERROR: " + message)
            messagebox.showerror("Build failed", message)


def main():
    root = tk.Tk()
    try:
        if os.name == "nt":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    Py2ExeStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
