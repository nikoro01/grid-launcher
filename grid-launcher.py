#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import os
import subprocess
import configparser

class GridLauncher(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Apps")
        self.set_default_size(400, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        self.add(main_box)
        
        close_btn = Gtk.Button(label="✕ Закрыть")
        close_btn.set_size_request(-1, 60)
        close_btn.connect("clicked", self.on_close)
        main_box.pack_start(close_btn, False, False, 0)
        
        self.grid = Gtk.FlowBox()
        self.grid.set_valign(Gtk.Align.START)
        self.grid.set_max_children_per_line(3)
        self.grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.grid.set_homogeneous(True)
        
        self.load_apps()
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.grid)
        main_box.pack_start(scrolled, True, True, 0)
        
        self.setup_css()
        
    def setup_css(self):
        css = b"""
        window {
            background-color: rgba(30, 30, 30, 0.95);
            border-radius: 12px;
        }
        button {
            font-size: 18px;
            padding: 15px;
            background-color: #D32F2F;
            color: white;
            border-radius: 8px;
            min-height: 50px;
        }
        flowboxchild {
            padding: 10px;
            background-color: #424242;
            border-radius: 8px;
        }
        flowboxchild button {
            background-color: #616161;
            color: #FFFFFF;
        }
        flowboxchild button:hover {
            background-color: #757575;
        }
        label {
            color: #FFFFFF;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
    def load_apps(self):
        apps = []
        desktop_dirs = [
            '/usr/share/applications',
            os.path.expanduser('~/.local/share/applications')
        ]
        
        for desktop_dir in desktop_dirs:
            if not os.path.exists(desktop_dir):
                continue
            for filename in os.listdir(desktop_dir):
                if not filename.endswith('.desktop'):
                    continue
                filepath = os.path.join(desktop_dir, filename)
                try:
                    config = configparser.ConfigParser(interpolation=None)
                    config.read(filepath, encoding='utf-8')
                    
                    if 'Desktop Entry' not in config:
                        continue
                    
                    entry = config['Desktop Entry']
                    name = entry.get('Name', '')
                    exec_cmd = entry.get('Exec', '')
                    icon_name = entry.get('Icon', '')
                    no_display = entry.get('NoDisplay', 'false').lower() == 'true'
                    
                    if name and exec_cmd and not no_display:
                        apps.append({
                            'name': name,
                            'exec': exec_cmd,
                            'icon': icon_name,
                            'file': filepath
                        })
                except:
                    continue
        
        apps.sort(key=lambda x: x['name'].lower())
        
        for app in apps:
            button = Gtk.Button()
            button.set_size_request(100, 100)
            
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            vbox.set_halign(Gtk.Align.CENTER)
            vbox.set_valign(Gtk.Align.CENTER)
            
            icon = self.get_icon(app['icon'])
            if icon:
                image = Gtk.Image.new_from_pixbuf(icon)
                vbox.pack_start(image, False, False, 0)
            
            label = Gtk.Label(label=app['name'][:12])
            label.set_line_wrap(True)
            label.set_max_width_chars(12)
            vbox.pack_start(label, False, False, 0)
            
            button.add(vbox)
            button.connect("clicked", self.on_app_clicked, app['exec'])
            
            self.grid.add(button)
    
    def get_icon(self, icon_name):
        if not icon_name:
            return None
        
        icon_theme = Gtk.IconTheme.get_default()
        
        try:
            if os.path.isabs(icon_name) and os.path.exists(icon_name):
                return GdkPixbuf.Pixbuf.new_from_file_at_size(icon_name, 48, 48)
            
            pixbuf = icon_theme.load_icon(icon_name, 48, Gtk.IconLookupFlags.FORCE_SIZE)
            return pixbuf
        except:
            return None
    
    def on_app_clicked(self, button, exec_cmd):
        exec_cmd = exec_cmd.split('%')[0].strip()
        subprocess.Popen(exec_cmd, shell=True)
        Gtk.main_quit()
    
    def on_close(self, button):
        Gtk.main_quit()

if __name__ == "__main__":
    win = GridLauncher()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
