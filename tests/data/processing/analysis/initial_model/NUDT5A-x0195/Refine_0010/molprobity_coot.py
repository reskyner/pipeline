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
data['rama'] = [('A', '  66 ', 'PRO', 0.04801433255268725, (-13.905, -7.749000000000002, -27.179)), ('B', '  66 ', 'PRO', 0.08059004065862224, (-1.4630000000000014, 14.042, -17.068)), ('D', ' 190 ', 'HIS', 0.006776447602571425, (-22.29, 2.1450000000000014, -42.48699999999999)), ('D', ' 190 ', 'HIS', 0.006769621067438944, (-22.29, 2.1450000000000014, -42.48699999999999))]
data['omega'] = []
data['rota'] = [('A', '  14 ', 'LYS', 0.0, (15.754000000000007, -0.1850000000000001, -2.457)), ('A', '  33 ', 'LYS', 0.25190821848070194, (-0.49299999999999966, -6.712, 7.819999999999999)), ('A', '  33 ', 'LYS', 0.25190821848070194, (-0.49299999999999966, -6.712, 7.819999999999999)), ('A', '  33 ', 'LYS', 0.25190821848070194, (-0.49299999999999966, -6.712, 7.819999999999999)), ('A', '  38 ', 'ASP', 0.17679564728984015, (11.083000000000002, 2.1050000000000004, 3.213)), ('A', '  43 ', 'THR', 0.21337833585962215, (10.580000000000004, -0.37199999999999966, 8.834)), ('A', '  70 ', 'ARG', 0.02408770608405123, (-19.042, -6.897, -38.852)), ('A', ' 189 ', 'GLU', 0.016510587546097237, (-29.520000000000003, 4.876, -14.782)), ('A', ' 189 ', 'GLU', 0.016510587546097237, (-29.520000000000003, 4.876, -14.782)), ('A', ' 189 ', 'GLU', 0.016510587546097237, (-29.520000000000003, 4.876, -14.782)), ('A', ' 191 ', 'LEU', 1.82109670137487e-05, (-25.036, 2.3539999999999996, -12.66)), ('A', ' 191 ', 'LEU', 1.82109670137487e-05, (-25.036, 2.3539999999999996, -12.66)), ('A', ' 191 ', 'LEU', 0.0035228354264305365, (-25.003000000000007, 2.2219999999999978, -12.386)), ('A', ' 191 ', 'LEU', 0.0035228354264305365, (-25.003000000000007, 2.2219999999999978, -12.386)), ('A', ' 191 ', 'LEU', 0.0035228354264305365, (-25.003000000000007, 2.2219999999999978, -12.386)), ('B', '  31 ', 'LEU', 0.0, (-13.515, -6.999, 5.15)), ('C', '  22 ', 'LEU', 0.2212917474947419, (-13.256000000000006, 12.280999999999995, -64.293)), ('C', '  31 ', 'LEU', 0.003964875041466896, (-19.063000000000002, 14.956000000000001, -63.38699999999999)), ('C', ' 164 ', 'ASP', 0.006876234478390146, (-22.661, 39.991, -53.14)), ('C', ' 189 ', 'GLU', 0.27052571263708663, (-46.914000000000016, 32.39799999999999, -58.605)), ('D', '  43 ', 'THR', 0.03333339980778477, (-24.931999999999995, 39.522, -65.745)), ('D', '  72 ', 'LEU', 0.12929002879645926, (-55.08599999999998, -2.3150000000000017, -33.984)), ('D', '  72 ', 'LEU', 0.12929002879645926, (-55.08599999999998, -2.3150000000000017, -33.984))]
data['cbeta'] = [('D', ' 188 ', 'GLU', ' ', 0.2511822590939635, (-25.215, 0.6239999999999979, -35.212))]
data['probe'] = [(' C  54 DARG  NH2', ' F  59 DHOH  O  ', -0.885, (-16.942, 15.744, -52.784)), (' C  54 CARG  NH2', ' F  59 CHOH  O  ', -0.885, (-16.942, 15.744, -52.784)), (' C  54 EARG  NH2', ' F  59 EHOH  O  ', -0.885, (-16.942, 15.744, -52.784)), (' A 191 CLEU  O  ', ' A 191 CLEU HD22', -0.883, (-24.039, 4.478, -13.681)), (' A 191 ELEU  O  ', ' A 191 ELEU HD22', -0.883, (-24.039, 4.478, -13.681)), (' A 191 DLEU  O  ', ' A 191 DLEU HD22', -0.883, (-24.039, 4.478, -13.681)), (' A 191 ELEU  C  ', ' A 191 ELEU  CD2', -0.767, (-23.641, 2.916, -14.184)), (' A 191 DLEU  C  ', ' A 191 DLEU  CD2', -0.767, (-23.641, 2.916, -14.184)), (' A 191 CLEU  C  ', ' A 191 CLEU  CD2', -0.767, (-23.641, 2.916, -14.184)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.753, (-18.445, -9.593, -42.285)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.724, (-20.784, 25.09, -36.729)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.721, (-34.824, 18.187, -33.44)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.719, (-5.937, -19.333, -22.72)), (' D 149 EASN  ND2', ' D 151 EASP  H  ', -0.703, (-54.967, -4.017, -45.061)), (' D 149 CASN  ND2', ' D 151 CASP  H  ', -0.703, (-54.967, -4.017, -45.061)), (' D 149 DASN  ND2', ' D 151 DASP  H  ', -0.703, (-54.967, -4.017, -45.061)), (' D 149 AASN  ND2', ' D 151 AASP  H  ', -0.702, (-54.968, -4.015, -45.06)), (' D 149 BASN  ND2', ' D 151 BASP  H  ', -0.702, (-54.968, -4.015, -45.06)), (' D 149 CASN HD21', ' D 151 CASP  HB2', -0.69, (-56.446, -3.969, -44.513)), (' D 149 DASN HD21', ' D 151 DASP  HB2', -0.69, (-56.446, -3.969, -44.513)), (' D 149 EASN HD21', ' D 151 EASP  HB2', -0.69, (-56.446, -3.969, -44.513)), (' D 149 AASN HD21', ' D 151 AASP  HB2', -0.689, (-56.447, -3.97, -44.514)), (' D 149 BASN HD21', ' D 151 BASP  HB2', -0.689, (-56.447, -3.97, -44.514)), (' C  55 ELYS  CB ', ' C  57 EGLN  N  ', -0.683, (-14.373, 18.925, -45.669)), (' C  55 DLYS  CB ', ' C  57 DGLN  N  ', -0.683, (-14.373, 18.925, -45.669)), (' C  55 CLYS  CB ', ' C  57 CGLN  N  ', -0.683, (-14.373, 18.925, -45.669)), (' D 149 AASN HD22', ' D 151 AASP  H  ', -0.662, (-54.053, -3.709, -44.612)), (' D 149 BASN HD22', ' D 151 BASP  H  ', -0.662, (-54.053, -3.709, -44.612)), (' D 149 CASN HD22', ' D 151 CASP  H  ', -0.661, (-54.051, -3.709, -44.609)), (' D 149 EASN HD22', ' D 151 EASP  H  ', -0.661, (-54.051, -3.709, -44.609)), (' D 149 DASN HD22', ' D 151 DASP  H  ', -0.661, (-54.051, -3.709, -44.609)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.655, (-49.567, -3.651, -51.855)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.648, (-7.522, 4.163, -25.243)), (' A 191 CLEU  CD2', ' A 191 CLEU  O  ', -0.626, (-23.391, 3.342, -14.199)), (' A 191 DLEU  CD2', ' A 191 DLEU  O  ', -0.626, (-23.391, 3.342, -14.199)), (' A 191 ELEU  CD2', ' A 191 ELEU  O  ', -0.626, (-23.391, 3.342, -14.199)), (' A 191 ELEU  C  ', ' A 191 ELEU HD22', -0.623, (-23.726, 3.327, -13.433)), (' A 191 CLEU  C  ', ' A 191 CLEU HD22', -0.623, (-23.726, 3.327, -13.433)), (' A 191 DLEU  C  ', ' A 191 DLEU HD22', -0.623, (-23.726, 3.327, -13.433)), (' D 149 DASN  C  ', ' D 149 DASN HD22', -0.616, (-54.518, -3.12, -45.425)), (' D 149 CASN  C  ', ' D 149 CASN HD22', -0.616, (-54.518, -3.12, -45.425)), (' D 149 EASN  C  ', ' D 149 EASN HD22', -0.616, (-54.518, -3.12, -45.425)), (' D 149 AASN  C  ', ' D 149 AASN HD22', -0.615, (-54.518, -3.12, -45.426)), (' D 149 BASN  C  ', ' D 149 BASN HD22', -0.615, (-54.518, -3.12, -45.426)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.611, (-42.383, 16.456, -41.09)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.591, (-11.52, 19.387, -7.126)), (' D 104  THR HG23', ' D 107  ALA  H  ', -0.552, (-49.731, 8.082, -62.554)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.546, (-31.636, 20.284, -50.644)), (' A 191 DLEU  C  ', ' A 191 DLEU HD23', -0.541, (-23.084, 2.441, -14.03)), (' A 191 CLEU  C  ', ' A 191 CLEU HD23', -0.541, (-23.084, 2.441, -14.03)), (' A 191 ELEU  C  ', ' A 191 ELEU HD23', -0.541, (-23.084, 2.441, -14.03)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.53, (-35.889, 18.817, -33.663)), (' D 194  ASP  OD1', ' D 196 EARG  HD3', -0.528, (-34.632, 12.459, -50.062)), (' C  15  GLN  N  ', ' C 404  HOH  O  ', -0.528, (-20.655, -5.666, -52.835)), (' A 189 EGLU  HB3', ' A 191 ELEU  CD1', -0.525, (-27.606, 2.802, -15.621)), (' A 189 DGLU  HB3', ' A 191 DLEU  CD1', -0.525, (-27.606, 2.802, -15.621)), (' B  58  THR  CB ', ' B 142  HIS  NE2', -0.525, (-16.63, 12.077, -7.199)), (' A 189 CGLU  HB3', ' A 191 CLEU  CD1', -0.525, (-27.606, 2.802, -15.621)), (' D 194  ASP  OD1', ' D 196 CARG  HD3', -0.523, (-34.047, 12.297, -49.758)), (' D  72 BLEU  CD1', ' D  72 BLEU  N  ', -0.517, (-56.978, -2.722, -34.939)), (' D  72 ALEU  CD1', ' D  72 ALEU  N  ', -0.517, (-56.978, -2.722, -34.939)), (' D 194  ASP  OD1', ' D 196 AARG  HD3', -0.514, (-34.04, 12.308, -49.76)), (' B 132  MET  HE1', ' B 196 EARG  CZ ', -0.508, (-6.789, 1.824, -10.079)), (' D  72 BLEU  N  ', ' D  72 BLEU HD12', -0.508, (-56.767, -1.996, -35.039)), (' D  72 ALEU  N  ', ' D  72 ALEU HD12', -0.508, (-56.767, -1.996, -35.039)), (' A  70  ARG  HD3', ' A 409  HOH  O  ', -0.501, (-20.214, -4.571, -35.988)), (' C  54 EARG  HB3', ' C  54 EARG  NH2', -0.501, (-16.114, 17.183, -51.125)), (' C  54 CARG  HB3', ' C  54 CARG  NH2', -0.501, (-16.114, 17.183, -51.125)), (' C  54 DARG  HB3', ' C  54 DARG  NH2', -0.501, (-16.114, 17.183, -51.125)), (' C  54 DARG  HB3', ' C  54 DARG HH21', -0.498, (-16.541, 17.377, -51.069)), (' C  54 EARG  HB3', ' C  54 EARG HH21', -0.498, (-16.541, 17.377, -51.069)), (' C  54 CARG  HB3', ' C  54 CARG HH21', -0.498, (-16.541, 17.377, -51.069)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.494, (-4.825, -4.113, -29.538)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.491, (8.295, 0.455, -14.846)), (' A 189 DGLU  HB3', ' A 191 DLEU HD13', -0.491, (-27.908, 3.114, -15.035)), (' A 189 CGLU  HB3', ' A 191 CLEU HD13', -0.491, (-27.908, 3.114, -15.035)), (' A 189 EGLU  HB3', ' A 191 ELEU HD13', -0.491, (-27.908, 3.114, -15.035)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.484, (-10.325, -4.249, -13.602)), (' A 132  MET  O  ', ' B 196 BARG  NH2', -0.484, (-6.401, -0.927, -10.829)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.48, (-5.57, -19.826, -22.39)), (' A 119  TYR  CE1', ' A 158  PRO  HG3', -0.476, (-23.019, -11.963, -30.488)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.473, (-6.381, 6.656, -22.601)), (' A 132  MET  O  ', ' B 196 AARG  NH2', -0.472, (-6.557, -0.995, -10.321)), (' A 132  MET  O  ', ' B 196 CARG  NH2', -0.472, (-6.556, -0.993, -10.32)), (' A 132  MET  O  ', ' B 196 DARG  NH2', -0.472, (-6.556, -0.993, -10.32)), (' D 149 EASN  C  ', ' D 149 EASN  ND2', -0.467, (-54.598, -3.24, -45.662)), (' D 149 DASN  C  ', ' D 149 DASN  ND2', -0.467, (-54.598, -3.24, -45.662)), (' D 149 CASN  C  ', ' D 149 CASN  ND2', -0.467, (-54.598, -3.24, -45.662)), (' D 149 BASN  C  ', ' D 149 BASN  ND2', -0.465, (-54.598, -3.24, -45.663)), (' D 149 AASN  C  ', ' D 149 AASN  ND2', -0.465, (-54.598, -3.24, -45.663)), (' A  71  THR  O  ', ' A  73  HIS  HD2', -0.461, (-22.08, -4.626, -41.471)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.458, (-43.301, 13.825, -42.931)), (' B 158  PRO  O  ', ' B 160  PRO  HD3', -0.458, (10.249, 18.121, -8.878)), (' A  22  LEU HD11', ' A  25  GLU  HB2', -0.453, (-6.312, -15.009, 6.215)), (' C 200  TYR  CD1', ' D 203  ALA  HB2', -0.453, (-40.401, 18.737, -40.753)), (' D  72 ELEU  N  ', ' D  72 ELEU HD12', -0.449, (-57.128, -2.252, -34.675)), (' C 206  HIS  HE1', ' D 125  GLU  OE1', -0.449, (-50.582, 13.745, -46.868)), (' D  72 DLEU  N  ', ' D  72 DLEU HD12', -0.449, (-57.128, -2.252, -34.675)), (' D  72 CLEU  N  ', ' D  72 CLEU HD12', -0.449, (-57.128, -2.252, -34.675)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.448, (2.228, 23.235, -26.241)), (' D  37  MET  SD ', ' D  41  GLY  O  ', -0.446, (-27.717, 42.604, -65.827)), (' C  80  VAL  HB ', ' C 168  VAL HG13', -0.434, (-33.977, 33.687, -49.125)), (' A 206  HIS  HD2', ' B 200  TYR  OH ', -0.432, (-6.155, 10.509, -22.696)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.43, (-39.193, 21.097, -37.345)), (' A 206  HIS  HE1', ' B 125  GLU  OE1', -0.43, (-10.681, 13.682, -22.271)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.429, (-47.618, 19.546, -49.857)), (' D 189 BGLU  O  ', ' D 190 BHIS  C  ', -0.427, (-24.031, 1.896, -42.82)), (' D 189 AGLU  O  ', ' D 190 AHIS  C  ', -0.427, (-24.031, 1.896, -42.82)), (' A  49  VAL HG21', ' B  49  VAL HG11', -0.425, (-9.546, -4.857, 0.407)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.419, (-9.029, -1.783, -27.889)), (' C  74  TYR  HB3', ' C 426  HOH  O  ', -0.413, (-48.506, 27.59, -35.289)), (' D  72 ELEU  CD1', ' D  72 ELEU  N  ', -0.411, (-56.688, -2.386, -34.83)), (' D  72 DLEU  CD1', ' D  72 DLEU  N  ', -0.411, (-56.688, -2.386, -34.83)), (' D  72 CLEU  CD1', ' D  72 CLEU  N  ', -0.411, (-56.688, -2.386, -34.83)), (' C  54 DARG  CB ', ' C  54 DARG HH21', -0.405, (-16.795, 17.411, -51.067)), (' C  54 EARG  CB ', ' C  54 EARG HH21', -0.405, (-16.795, 17.411, -51.067)), (' C  54 CARG  CB ', ' C  54 CARG HH21', -0.405, (-16.795, 17.411, -51.067)), (' A  18  ILE HD11', ' A  37  MET  HE2', -0.404, (13.147, -3.513, 6.514)), (' A 167  PHE  CD2', ' B  39  PRO  HG2', -0.401, (-29.539, -14.175, -11.826)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.401, (-32.159, 14.681, -51.338))]
gui = coot_molprobity_todo_list_gui(data=data)
