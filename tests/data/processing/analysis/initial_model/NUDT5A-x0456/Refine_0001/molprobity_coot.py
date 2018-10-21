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
data['rama'] = [('A', '  66 ', 'PRO', 0.044020720157784604, (-13.686, -7.656000000000001, -27.042999999999996)), ('B', '  66 ', 'PRO', 0.040545758628823994, (-1.4749999999999992, 14.187999999999999, -16.982)), ('C', '  66 ', 'PRO', 0.08483260091728834, (-35.261, 28.073000000000004, -38.236)), ('D', '  66 ', 'PRO', 0.08115458070465824, (-45.04500000000001, 4.7609999999999975, -47.964))]
data['omega'] = []
data['rota'] = [('A', '  14 ', 'LYS', 0.0, (15.851, -0.06700000000000012, -2.334)), ('A', '  70 ', 'ARG', 0.025534711680543925, (-18.71, -6.772000000000002, -38.696)), ('A', ' 191 ', 'LEU', 0.0006901256611748707, (-24.757000000000012, 2.3460000000000005, -12.406)), ('B', '  31 ', 'LEU', 0.000479780951845923, (-13.315, -6.954, 5.281)), ('B', '  38 ', 'ASP', 0.09469358084819283, (-29.694, -12.852, -6.343)), ('C', '  31 ', 'LEU', 0.0010858725130596623, (-18.502000000000002, 15.094999999999999, -63.3)), ('C', ' 136 ', 'LEU', 0.023149739538597232, (-26.649000000000015, 11.750000000000004, -58.72399999999999)), ('C', ' 191 ', 'LEU', 0.1326271931571055, (-41.69, 29.079, -57.796)), ('D', '  43 ', 'THR', 0.02447880688123405, (-24.231, 39.676, -65.363)), ('D', '  72 ', 'LEU', 0.0015677893096665617, (-54.422, -2.1630000000000007, -33.868)), ('D', ' 208 ', 'ASN', 0.0, (-45.531000000000006, 18.641, -31.115))]
data['cbeta'] = [('C', ' 190 ', 'HIS', ' ', 0.25429605757305346, (-43.35100000000001, 30.196000000000005, -62.03199999999999))]
data['probe'] = [(' D 196 DARG  HG3', ' D 196 DARG HH21', -0.934, (-35.572, 15.744, -50.163)), (' D 196 BARG  HG3', ' D 196 BARG HH21', -0.934, (-35.572, 15.744, -50.163)), (' D 196 DARG  HG3', ' D 196 DARG  NH2', -0.865, (-35.195, 15.36, -49.824)), (' D 196 BARG  HG3', ' D 196 BARG  NH2', -0.865, (-35.195, 15.36, -49.824)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.766, (-20.382, 25.244, -36.472)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.739, (-5.123, -19.399, -22.65)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.732, (-49.145, -4.312, -51.435)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.729, (-34.526, 18.145, -33.266)), (' D 194  ASP  OD1', ' D 196 CARG  HD3', -0.726, (-33.845, 12.528, -50.077)), (' D 194  ASP  OD1', ' D 196 AARG  HD3', -0.721, (-33.513, 12.219, -49.643)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.691, (-11.557, 19.628, -7.227)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.681, (-41.827, 16.601, -41.085)), (' C 166  GLU  OE2', ' C 401  HOH  O  ', -0.658, (-25.71, 32.842, -48.477)), (' B 194  ASP  OD2', ' B 196  ARG  NH2', -0.639, (-4.468, 0.112, -11.518)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.634, (-7.687, 4.821, -24.834)), (' C 112  GLU  OE2', ' C 401  HOH  O  ', -0.632, (-25.604, 31.897, -47.15)), (' B 301  EDO  H22', ' B 404  HOH  O  ', -0.617, (2.581, 23.402, -26.793)), (' D 104  THR HG23', ' D 107  ALA  H  ', -0.612, (-49.445, 8.249, -62.383)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.609, (-18.318, -8.667, -42.396)), (' D 196 BARG  CG ', ' D 196 BARG  NH2', -0.592, (-35.083, 15.124, -49.834)), (' D 196 DARG  CG ', ' D 196 DARG  NH2', -0.592, (-35.083, 15.124, -49.834)), (' A  70  ARG  HD3', ' A 409  HOH  O  ', -0.589, (-20.043, -4.303, -35.847)), (' D 188  GLU  HG3', ' D 189  GLU  HG3', -0.582, (-25.766, -0.165, -37.861)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.559, (-30.915, 20.526, -50.651)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.555, (-46.845, 19.441, -50.188)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.544, (-35.413, 18.864, -33.662)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.543, (-6.388, 6.916, -22.416)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.539, (-38.566, 20.972, -37.498)), (' D 152  ASP  OD2', ' D 154  GLU  N  ', -0.526, (-54.037, -8.452, -50.321)), (' D 132  MET  HE1', ' D 196 AARG  CZ ', -0.525, (-34.236, 13.251, -53.555)), (' D 132  MET  HE1', ' D 196 CARG  CZ ', -0.525, (-34.236, 13.251, -53.555)), (' D 189  GLU  O  ', ' D 190  HIS  C  ', -0.519, (-23.612, 1.888, -43.092)), (' A  71  THR  O  ', ' A  73  HIS  HD2', -0.509, (-21.656, -4.601, -41.373)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.495, (2.06, 23.159, -26.128)), (' A 132  MET  O  ', ' B 196  ARG  NH2', -0.481, (-6.14, -0.531, -10.631)), (' A 206  HIS  HD2', ' B 200  TYR  OH ', -0.48, (-6.11, 10.624, -22.862)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.475, (-8.767, -1.455, -27.703)), (' C  15  GLN  N  ', ' C 404  HOH  O  ', -0.475, (-20.253, -5.517, -52.667)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.473, (-42.718, 13.973, -42.876)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.468, (-5.27, -19.615, -22.406)), (' A 206  HIS  HE1', ' B 125  GLU  OE1', -0.467, (-10.727, 13.713, -22.389)), (' B  81  LYS  HA ', ' B  91  CYS  O  ', -0.463, (5.587, 2.825, -10.133)), (' D  37  MET  SD ', ' D  41  GLY  C  ', -0.462, (-27.628, 43.243, -64.97)), (' C 206  HIS  HE1', ' D 125  GLU  OE1', -0.453, (-49.973, 13.856, -46.859)), (' D  37  MET  SD ', ' D  41  GLY  O  ', -0.452, (-26.92, 43.15, -65.467)), (' B 196  ARG  NE ', ' B 422  HOH  O  ', -0.452, (-6.276, 3.569, -11.242)), (' B  23  ILE HD11', ' B  33  LYS  HB2', -0.45, (-17.838, -11.818, 5.493)), (' D 208  ASN  CG ', ' D 415  HOH  O  ', -0.448, (-45.64, 14.652, -30.325)), (' A  70  ARG  CD ', ' A 409  HOH  O  ', -0.442, (-19.915, -4.913, -35.225)), (' C 206  HIS  HD2', ' D 200  TYR  OH ', -0.44, (-45.724, 11.375, -43.807)), (' D 196 BARG  CG ', ' D 196 BARG HH21', -0.439, (-35.575, 15.763, -50.415)), (' D 196 DARG  CG ', ' D 196 DARG HH21', -0.439, (-35.575, 15.763, -50.415)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.437, (8.432, 0.926, -14.615)), (' C 132  MET  O  ', ' D 196 DARG  NH1', -0.437, (-31.672, 14.499, -51.355)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.436, (-10.527, -4.399, -13.147)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.434, (-31.475, 14.659, -51.697)), (' A 200  TYR  CD1', ' B 203  ALA  HB2', -0.423, (-8.644, 1.595, -24.956)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.422, (-4.567, -4.0, -29.116)), (' C  92  ILE HG13', ' C 191  LEU HD13', -0.41, (-40.774, 29.377, -53.363)), (' D 191  LEU  C  ', ' D 191  LEU HD12', -0.403, (-25.837, 5.481, -43.375))]
gui = coot_molprobity_todo_list_gui(data=data)
