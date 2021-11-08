# flatten_covid19_cell_def_xml.py - convert a PhysiCell_settings.xml with inheritance 
#    of <cell_definitions> into one without inheritance, i.e., verbose leaf <cell_definition>s.
#
# Note: leaf cell defs are hard-coded in this script for now.
#
# $ grep cell_def PhysiCell_settings-with-complete-default-params.xml|grep parent
# 		<cell_definition name="lung epithelium" parent_type="default" ID="1">
# 		<cell_definition name="immune" parent_type="default" ID="2">
# 		<cell_definition name="CD8 Tcell" parent_type="immune" ID="3">
# 		<cell_definition name="macrophage" parent_type="immune" ID="4">
# 		<cell_definition name="neutrophil" parent_type="immune" ID="5">
# 		<cell_definition name="DC" parent_type="immune" ID="6">
# 		<cell_definition name="CD4 Tcell" parent_type="immune" ID="7">
# 		<cell_definition name="fibroblast" parent_type="immune" ID="8">
#
# --> after:
# $ grep cell_def flat.xml|grep parent
# 		<cell_definition ID="1" name="lung epithelium" parent="default">
# 		<cell_definition ID="3" name="CD8 Tcell" parent="default">
# 		<cell_definition ID="4" name="macrophage" parent="default">
# 		<cell_definition ID="5" name="neutrophil" parent="default">
# 		<cell_definition ID="6" name="DC" parent="default">
# 		<cell_definition ID="7" name="CD4 Tcell" parent="default">
# 		<cell_definition ID="8" name="fibroblast" parent="default">
#
# Author: Randy Heiland
#

import xml.etree.ElementTree as ET
import sys

argc = len(sys.argv)
if argc < 2:
    print("--- Provide the hierarchical config filename.\n")
    sys.exit()
orig_fname = sys.argv[1]
print("orig_fname=",orig_fname)

#--------------------------------------------------
# For now, just manually define all "leaf" cell defs. For the covid19 model, it's any cell def with parent_type="default" or parent_type="immune". (grep "<cell_def" PhysiCell_settings.xml)
# leaf_cell_defs = {"lung epithelium":"1", "CD8 Tcell":"3", "macrophage":"4", "neutrophil":"5", "DC":"6", "CD4 Tcell":"7", "fibroblasts":"8", "residual":"9"}
# print("\nleaf_cell_defs dict: ",leaf_cell_defs,"\n")
# print("\nleaf_cell_defs dict keys: ",leaf_cell_defs.keys(),"\n")


print("\n===================================================================================")
print("\n--- Phase 0: Create leaf_cell_dict (just the leaf cells).\n")

leaf_cell_dict = {}

# Get the original hierarchical .xml
tree = ET.parse(orig_fname)  
xml_root = tree.getroot()
cell_defs = tree.find('cell_definitions')

for cell_def in list(cell_defs):  # for each cell_definition
    if ('parent_type' in cell_def.attrib.keys()) and (cell_def.attrib['name'] != 'immune'):
    # leaf_cell_dict = {"lung epithelium":"1", "CD8 Tcell":"3", "macrophage":"4", "neutrophil":"5", "DC":"6", "CD4 Tcell":"7", "fibroblasts":"8", "residual":"9"}
        leaf_cell_dict[cell_def.attrib['name']] = cell_def.attrib['ID']
        # print("found: ",cell_def.attrib['name'], ", ID=",cell_def.attrib['ID'])
print("leaf_cell_dict = ",leaf_cell_dict)
# sys.exit()


print("\n===================================================================================")
print("\n--- Phase 1: Check if all substrates appear in the <phenotype><secretion> for 'default' cell_definition.\n")

# Get the original hierarchical .xml
tree = ET.parse(orig_fname)  
xml_root = tree.getroot()
menv = tree.find('microenvironment_setup')

substrates = []
for var in menv:  # for each substrate
    # if (cell_def.attrib['name'] != 'default') and ('parent_type' in cell_def.attrib.keys() ): # and ('immune' in cell_def.attrib['parent_type'] ) :
    if var.tag == 'variable':
        substrates.append(var.attrib['name'])
        # print("found: ",var.attrib['name'], ", ID=",var.attrib['ID'])
print("all defined substrates = ",substrates)
# sys.exit()

tree = ET.parse(orig_fname)  
xml_root = tree.getroot()
cell_defs = tree.find('cell_definitions')
for cell_def in list(cell_defs):
    if (cell_def.attrib['name'] == 'default'):
        default_substrates = []
        print("--- all substrates listed in default//phenotype//secretion:")
        uep = cell_def.find('phenotype//secretion')
        for sub in uep:
            # print(sub.attrib['name'])
            default_substrates.append(sub.attrib['name'])
print("all 'default' substrates = ",default_substrates)
if set(substrates) == set(default_substrates):
    print("Yes, the default cell_def defines secretion for all substrates.")
else:
    print("\n******************* ")
    print("*** Warning: there is a mismatch in the defined substrates and the phenotype//secretion substrates in the default cell_def.")
    print("*******************\n")
    print("substrates: ",substrates)
    print(" vs.")
    print("default secretion substrates: ",default_substrates)
    print("\n Missing: ")
    if len(set(substrates)) > len(set(default_substrates)):
        print(set(substrates) - set(default_substrates))
    else:
        print(set(default_substrates) - set(substrates))
    print()
    print("\n *** You may need to fix this and try again. \n\n")
    # sys.exit()

#--------------------------------------------------
print("\n===================================================================================")
print("\n--- Phase 2: create a new .xml containing N copies (N=# of leaf cell defs) of 'default' cell_definition, with desired names.\n")

#tree0 = tree
#flat_root = xml_root
# default_cell_def = xml_root.find("cell_definitions//cell_definition[@name='default']")
cell_defs = tree.find('cell_definitions')
# root_node = cell_defs.getroot()
#--------------------------------------------------
print("--- Remove all but default cell_defs")
for cell_def in list(cell_defs):
    # print(cell_def.tag, cell_def.attrib['name'])
    if (cell_def.attrib['name'] != 'default'):
        print("removing ", cell_def.attrib['name'])
        cell_defs.remove(cell_def)
        # ET.SubElement(root_node,default_cell_def)
        # cell_defs.insert(0,default_cell_def)

#--------------------------------------------------
# Get a copy of the "default" cell_def
default_cell_def = xml_root.find("cell_definitions//cell_definition[@name='default']")
print("--- Insert duplicate default cell_def for each leaf")

for leaf in leaf_cell_dict.keys():
    print(leaf)
#    print(cell_def.tag, cell_def.attrib['name'])
    cell_defs.insert(0,default_cell_def)

new_xml_file = "flat_N_defaults.xml"
tree.write(new_xml_file)
print("\n-----> ",new_xml_file)
# sys.exit()

#--------------------------------------------------
# Get the previously written flattened .xml
tree = ET.parse(new_xml_file)  
xml_root = tree.getroot()
cell_defs = tree.find('cell_definitions')

leaf_name = list(leaf_cell_dict.keys())
leaf_ID = list(leaf_cell_dict.values())

print("--- Change cell_def name for *each* leaf")
print("leaf_name = ",leaf_name)
idx = -1
# leaf_name = list(leaf_cell_dict.keys())
for cell_def in list(cell_defs):
# for cell_def in leaf_cell_dict.keys():
    # print("cell_def=",cell_def)
# for leaf in leaf_cell_defs:
    if idx >= 0:
        cell_def.attrib['name'] = leaf_name[idx]
        cell_def.attrib['ID'] = leaf_ID[idx]
        print(idx,cell_def.attrib['name'],cell_def.attrib['ID'])
        # cell_def.attrib['ID'] = leaf_cell_defs[leaf_name[idx]]
        # insert parent = "default" attribute
        # cell_def.set("parent","default")

        # print(cell_def.attrib['name'])
    idx += 1
    # cell_def.attrib['name'] = leaf

#tree = tree0
# default_cell_def = xml_root.find("cell_definitions//cell_definition[@name='default']")
# ET.SubElement(cell_defs, default_cell_def)

new_xml_file = "flat_N.xml"
tree.write(new_xml_file)
print("\n-----> ",new_xml_file)

print("\nDone. Please check the output file: " + new_xml_file + "\n")
# sys.exit()

#--------------------------------------------------
#  Now read the params from the original "immune" cell_definition and update them in each leaf immune cell def
#  in the flattened .xml just created.
print("\n===================================================================================")
print("--- Phase 3: edit the new .xml so each immune *leaf* cell type has its parent's (immune) params\n")

"""
for example:
				<secretion>
					<substrate name="pro-inflammatory cytokine">
						<uptake_rate units="1/min">0.01</uptake_rate>
					</substrate> 	
					<substrate name="chemokine">
						<uptake_rate units="1/min">0.01</uptake_rate>
					</substrate> 	
					<substrate name="debris">
						<uptake_rate units="1/min">0.1</uptake_rate>
"""


# Get the previously written flattened .xml
tree_flat = ET.parse(new_xml_file)
xml_flat_root = tree_flat.getroot()


def recurse_node(root, xmlpath, substrate_name, cell_name):
    global save_param_val, xml_flat_root, leaf_immune_cell_defs
    # print("--- recurse_node:  root.tag=",root.tag,"<<<")
    xmlpath = xmlpath + "//" + root.tag[root.tag.rfind('}')+1:]
    param_val = ''
    # substrate_name = ""
    if (root.tag == "substrate") and (len(root.attrib) > 0):   # don't want substrate for chemotaxis, just secretion
        # e.g.,  <substrate name="debris">
        # print("recurse_node: ========>> found substrate (for secretion), attrib=",root.attrib)
        substrate_name = root.attrib["name"]
        # print("recurse_node: ========>> substrate_name =",substrate_name ,"\n")
        xmlpath = xmlpath.replace("substrate", "substrate[@name='" + substrate_name + "']" )
    for child in root:
        param_val = ' '.join(child.text.split())
        if param_val != '':
            # print('param value=',param_val, ' for ',end='')
            save_param_val = param_val
            # uep.find('.//cell_definition[1]//phenotype//mechanics//cell_cell_adhesion_strength').text = str(self.float27.value)
        recurse_node(child, xmlpath, substrate_name, cell_name)
    if len(list(root)) == 0:  # we are finally at the bottom of the recursion; the element of interest.
        # e.g.  //phenotype//motility//options//chemotaxis//direction  =  1
        #       //phenotype//secretion//substrate//uptake_rate  =  0.01    (WRONG - also need to know substrate *name*)
        # print(xmlpath)
        # print(xmlpath,' = ',save_param_val)

        # e.g., default_cell_def = xml_root.find("cell_definitions//cell_definition[@name='default']")
        # fullpath = "cell_definitions//cell_definition[@name='macrophage']" + xmlpath
        fullpath = "cell_definitions//cell_definition[@name='" + cell_name + "']" + xmlpath
        # print("fullpath=",fullpath)
        uep = xml_flat_root.find(fullpath)
        try:
            uep.text  = save_param_val
        except:
            print("Error trying to assign: uep.text =",save_param_val)
            print("You need to repair (probably insert) the missing XML element based on:")
            print("fullpath=",fullpath)
            sys.exit()
        # print("------ updated uep.text !!!")

        # update_all_immune_cell_def_params(xmlpath, save_param_val, substrate_name)


#
# Recursively walk through just the "immune" cell_def (in the original hierarchical .xml) and for
# each parameter value that's defined, copy that value into *each* leaf immune cell_def (macrophage, etc.)
# of the most recently updated (flattened) .xml
#

# hardcode for now:
leaf_immune_cell_defs = ["CD8 Tcell", "macrophage", "neutrophil", "DC", "CD4 Tcell","fibroblast"]
# leaf_immune_cell_defs = ["macrophage"]

idx = -1
tree_orig = ET.parse(orig_fname)
# tree = ET.parse("new_flat_config1.xml")  
xml_orig = tree_orig.getroot()
uep = None
uep_immune = xml_orig.find("cell_definitions//cell_definition[@name='immune']")
for cell_def_name in leaf_immune_cell_defs:  # not optimal, but I don't care
    for child in uep_immune:  # recursively visit all params in <phenotype>
        if child.tag != 'custom_data':
            # print("------- calling recurse_node on child=",child)
            recurse_node(child, "", "", cell_def_name)  
print("\nDone.")

new_xml_file = "flat_immune_leafs.xml"
tree_flat.write(new_xml_file)
print("\nDone. Please check the output file: " + new_xml_file + "\n")
# sys.exit()

#--------------------------------------------------
print("\n===================================================================================")
print("--- Phase 4: edit the new .xml so each non-immune (leaf) cell type has its parent's (default) params\n")

#
# Recursively walk through each leaf cell_def (in the original hierarchical .xml) and for
# each parameter value that's defined, copy that value into the corresponding leaf cell_def 
# (epi, residual, macrophage, etc.) of the most recently updated .xml
#

# Get the previously written flattened .xml
tree_flat = ET.parse(new_xml_file)  
xml_flat_root = tree_flat.getroot()  # we'll update xml_flat_root (and write to a new output file)

# Get the original hierarchical .xml
tree_orig = ET.parse(orig_fname)  
xml_orig = tree_orig.getroot()

# leaf_cell_defs = {"lung epithelium":"1", "CD8 Tcell":"3", "macrophage":"4", "neutrophil":"5", "DC":"6", "CD4 Tcell":"7", "fibroblasts":"8", "residual":"9"}
# hardcode for now:
# leaf_cell_defs = ["lung epithelium", "residual", "macrophage" ]
leaf_cell_defs = ["CD8 Tcell", "macrophage", "neutrophil", "DC", "CD4 Tcell","fibroblasts", "lung epithelium", "residual"]
for cd in xml_orig.findall('cell_definitions//cell_definition'):
    idx += 1
    if cd.attrib["name"] in leaf_cell_defs:
        uep = cd
        print("\n>>>>>>>>>>> processing ",cd.attrib["name"])   # 2  (0=default, 1=lung epi)
        # immune_uep = root.find('.//cell_definitions')
        for child in cd:
            # print("------- calling recurse_node on child=",child)
            # recurse_node(child,"",cd.attrib["name"])
            recurse_node(child, "", "", cd.attrib["name"])

print("\nDone.")

new_xml_file = "flat_final.xml"
tree_flat.write(new_xml_file)

with open(new_xml_file, 'r+') as f:
    new_xml = f.read()
    f.seek(0, 0)
    f.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + new_xml)

print("---> wrote ",new_xml_file, "(copy it to PhysiCell_settings.xml if desirable)\n")