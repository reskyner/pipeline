# script auto-generated by phenix.molprobity


from __future__ import division
import cPickle
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui (object) :
  def __init__ (self, title) :
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window (self) :
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window (self, *args) :
    self.window.destroy()
    self.window = None

  def confirm_data (self, data) :
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists (self, data) :
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui (coot_extension_gui) :
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None) :
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__ (self, data_file=None, data=None) :
    assert ([data, data_file].count(None) == 1)
    if (data is None) :
      data = load_pkl(data_file)
    if not self.confirm_data(data) :
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets (self, data_key, box) :
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots (self, *args) :
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots (self, *args) :
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui (coot_extension_gui) :
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list (object) :
  def __init__ (self, columns, column_types, rows, box,
      default_size=(380,200)) :
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)) :
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns) :
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange (self, treeview) :
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots (show_dots, overlaps_only) :
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects) :
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects) :
      set_display_generic_object(object_number, 0)

def load_pkl (file_name) :
  pkl = open(file_name, "rb")
  data = cPickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', '  66 ', 'PRO', 0.04642028481035706, (-13.898000000000001, -7.753000000000001, -27.186999999999998)), ('B', '  40 ', 'THR', 0.026458871455515346, (-33.91700000000001, -16.004, -8.938)), ('B', '  66 ', 'PRO', 0.06338164633420192, (-1.475999999999999, 14.052, -17.082)), ('D', '  66 ', 'PRO', 0.0959318211997978, (-45.623, 4.582, -48.077))]
data['omega'] = []
data['rota'] = [('A', '  14 ', 'LYS', 0.0, (15.793, -0.14300000000000002, -2.339)), ('A', '  33 ', 'LYS', 0.08838377052032298, (-0.5069999999999999, -6.709, 7.8229999999999995)), ('A', '  33 ', 'LYS', 0.08838377052032298, (-0.5069999999999999, -6.709, 7.8229999999999995)), ('A', '  33 ', 'LYS', 0.08838377052032298, (-0.5069999999999999, -6.709, 7.8229999999999995)), ('A', '  38 ', 'ASP', 0.12473271961875457, (11.056, 2.118, 3.235)), ('A', '  43 ', 'THR', 0.13022835327517823, (10.566000000000006, -0.4169999999999998, 8.811)), ('A', '  50 ', 'LYS', 0.29627283374804186, (-5.245, -10.659, -1.3049999999999997)), ('A', '  70 ', 'ARG', 0.017498276226217892, (-19.04, -6.903, -38.846)), ('A', ' 191 ', 'LEU', 0.0, (-24.949, 2.240999999999998, -12.569)), ('B', '  31 ', 'LEU', 0.0, (-13.544000000000008, -7.01, 5.137)), ('C', '  22 ', 'LEU', 0.21300510255632946, (-13.218000000000002, 12.276, -64.265)), ('C', '  31 ', 'LEU', 0.0, (-19.073, 14.963, -63.36)), ('C', '  53 ', 'THR', 0.19318259488995213, (-15.776000000000003, 22.615, -52.752)), ('C', ' 164 ', 'ASP', 0.005465054460793245, (-22.73400000000001, 39.99000000000001, -53.17699999999999)), ('C', ' 189 ', 'GLU', 0.22956810508059136, (-46.92399999999999, 32.429000000000016, -58.61899999999999)), ('D', '  43 ', 'THR', 0.008159601566148922, (-24.997999999999998, 39.527, -65.743)), ('D', '  72 ', 'LEU', 0.03273009118601763, (-55.139, -2.3520000000000016, -34.01)), ('D', ' 188 ', 'GLU', 0.28174422224820866, (-24.375, 1.4739999999999993, -36.029))]
data['cbeta'] = [('A', '  82 ', 'GLN', ' ', 0.30615209924792125, (-22.652, -8.087000000000002, -13.248999999999999)), ('B', '  82 ', 'GLN', ' ', 0.2585272516634744, (5.22, 4.032, -5.763)), ('D', ' 188 ', 'GLU', ' ', 0.34247366436853216, (-25.275000000000002, 0.5309999999999988, -35.255))]
data['probe'] = [(' B 301  EDO  H22', ' B 404  HOH  O  ', -0.801, (2.509, 23.17, -26.877)), (' D 150  GLY  O  ', ' D 401  HOH  O  ', -0.766, (-51.04, -6.522, -44.275)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.762, (-20.783, 25.069, -36.724)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.724, (-5.959, -19.338, -22.721)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.695, (-34.821, 18.206, -33.438)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.688, (-18.811, -9.122, -42.635)), (' D 194  ASP  OD1', ' D 196 EARG  HD3', -0.671, (-34.459, 12.34, -50.208)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.667, (2.403, 22.957, -26.014)), (' D 194  ASP  OD1', ' D 196 CARG  HD3', -0.663, (-34.051, 12.065, -49.895)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.661, (-11.013, 19.431, -7.28)), (' D 194  ASP  OD1', ' D 196 AARG  HD3', -0.648, (-34.047, 12.077, -49.907)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.646, (-7.534, 4.162, -25.262)), (' D 104  THR HG23', ' D 107  ALA  H  ', -0.624, (-49.765, 8.085, -62.567)), (' D  37  MET  SD ', ' D  41  GLY  O  ', -0.623, (-27.805, 42.513, -66.154)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.614, (-49.529, -3.699, -51.839)), (' D 149  ASN HD22', ' D 151  ASP  H  ', -0.591, (-54.384, -3.869, -44.653)), (' C 166  GLU  OE2', ' C 401  HOH  O  ', -0.59, (-26.118, 32.972, -48.592)), (' D 149  ASN  ND2', ' D 151  ASP  H  ', -0.589, (-54.657, -4.057, -44.617)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.585, (-31.617, 20.282, -50.655)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.581, (-35.846, 18.841, -33.713)), (' D 208  ASN  OD1', ' D 415  HOH  O  ', -0.581, (-46.158, 14.391, -30.659)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.571, (-42.414, 16.412, -41.074)), (' C  15  GLN  N  ', ' C 404  HOH  O  ', -0.57, (-20.497, -5.493, -52.847)), (' A  70  ARG  HD3', ' A 409  HOH  O  ', -0.558, (-20.149, -4.52, -36.034)), (' B 158  PRO  O  ', ' B 160  PRO  HD3', -0.537, (9.943, 18.445, -9.414)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.529, (-4.423, -4.337, -29.605)), (' B 132  MET  HE1', ' B 196 EARG  CZ ', -0.523, (-6.84, 1.84, -10.071)), (' B  58  THR  CB ', ' B 142  HIS  NE2', -0.521, (-17.056, 12.079, -6.931)), (' D 149  ASN  C  ', ' D 149  ASN HD22', -0.513, (-54.532, -3.103, -45.471)), (' A 132  MET  O  ', ' B 196 BARG  NH2', -0.509, (-6.664, -1.061, -10.513)), (' A 132  MET  O  ', ' B 196 AARG  NH2', -0.509, (-6.664, -1.061, -10.513)), (' A  71  THR  O  ', ' A  73  HIS  HD2', -0.507, (-22.031, -4.606, -41.485)), (' A 132  MET  O  ', ' B 196 DARG  NH2', -0.506, (-6.665, -1.053, -10.51)), (' A 132  MET  O  ', ' B 196 CARG  NH2', -0.506, (-6.664, -1.053, -10.51)), (' A  22  LEU HD11', ' A  25  GLU  HB2', -0.496, (-6.32, -15.012, 5.96)), (' A  70  ARG  CD ', ' A 409  HOH  O  ', -0.493, (-20.414, -4.876, -35.389)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.485, (-5.58, -19.816, -22.42)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.48, (-6.661, 6.722, -22.598)), (' C 206  HIS  HE1', ' D 125  GLU  OE1', -0.479, (-50.311, 13.734, -46.486)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.476, (-43.323, 13.826, -42.928)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.468, (-10.256, -3.952, -13.191)), (' C  58  THR  CB ', ' C 142  HIS  NE2', -0.462, (-20.839, 17.221, -41.303)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.457, (-39.181, 21.093, -37.363)), (' D 189  GLU  O  ', ' D 190  HIS  C  ', -0.457, (-23.815, 1.519, -43.213)), (' C 179  LEU HD23', ' C 205  LYS  HD2', -0.455, (-51.168, 18.313, -46.173)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.452, (-47.739, 19.329, -49.862)), (' C 200  TYR  CD1', ' D 203  ALA  HB2', -0.44, (-40.412, 18.747, -40.737)), (' A 206  HIS  HD2', ' B 200  TYR  OH ', -0.44, (-6.149, 10.517, -22.699)), (' C  74  TYR  HB3', ' C 426  HOH  O  ', -0.439, (-48.291, 27.804, -35.339)), (' A 119  TYR  CE1', ' A 158  PRO  HG3', -0.437, (-23.069, -11.908, -30.431)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.431, (-9.014, -1.782, -27.901)), (' C 206  HIS  HD2', ' D 200  TYR  OH ', -0.43, (-46.32, 11.411, -43.629)), (' A 206  HIS  HE1', ' B 125  GLU  OE1', -0.43, (-10.684, 13.65, -22.221)), (' A  87  MET  HB3', ' A  87  MET  HE3', -0.429, (-20.962, -0.321, -6.746)), (' A  49  VAL HG21', ' B  49  VAL HG11', -0.424, (-9.544, -4.85, 0.388)), (' C  80  VAL  HB ', ' C 168  VAL HG13', -0.424, (-33.97, 33.67, -49.132)), (' A  39  PRO  HG3', ' B 167  PHE  CG ', -0.423, (10.97, 5.984, -0.438)), (' A 179  LEU HD23', ' A 205  LYS  HD2', -0.423, (-14.79, 11.541, -24.379)), (' C  45 DTHR HG23', ' F   5 DHOH  O  ', -0.421, (-22.949, 4.006, -66.704)), (' C  45 ETHR HG23', ' F   5 EHOH  O  ', -0.42, (-22.749, 4.177, -66.697)), (' C  45 CTHR HG23', ' F   5 CHOH  O  ', -0.42, (-22.749, 4.177, -66.697)), (' D 149  ASN HD21', ' D 151  ASP  HB2', -0.419, (-56.437, -4.199, -43.921)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.416, (8.121, 0.437, -14.631)), (' C 127  SER  HB2', ' C 128  PRO  HD2', -0.414, (-29.47, 14.286, -39.185)), (' A 165  GLY  HA2', ' A 167  PHE  CE1', -0.409, (-26.426, -16.329, -9.401)), (' C 136  LEU  C  ', ' C 136  LEU HD13', -0.407, (-25.998, 13.305, -59.231)), (' B  23  ILE HD11', ' B  33  LYS  HB2', -0.403, (-17.683, -11.986, 5.68)), (' C  64  VAL  O  ', ' C  66  PRO  HD3', -0.402, (-34.865, 26.426, -41.544)), (' B  81  LYS  HA ', ' B  91  CYS  O  ', -0.401, (5.271, 2.788, -10.263))]
gui = coot_molprobity_todo_list_gui(data=data)
