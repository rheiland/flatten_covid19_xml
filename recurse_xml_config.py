import xml.etree.ElementTree as ET
import sys

argc = len(sys.argv)
if argc < 2:
    print("--- provide an xml filename.\n")
    sys.exit()
fname = sys.argv[1]
print("fname=",fname)

#tree = ET.parse('nanobio_settings.xml')
#tree = ET.parse('test1.xml')
#tree = ET.parse('/Users/heiland/git/mcds2isa/HUVEC/HUVEC_v4_SHF_test.xml')
#tree = ET.parse('PhysiCell_settings-v4-inherit.xml')
tree = ET.parse(fname)
root = tree.getroot()

def parseXML(root,sm):
    sm = sm + "/" + root.tag[root.tag.rfind('}')+1:]
    # if 'cell_definitions' in root.tag:
    # if 'cell_definition' in root.tag:
    if  root.tag == 'cell_definitions':
        print("--- found cell_definitions ---")
    elif  root.tag == 'cell_definition':
        print("--- found cell_definition: ",root.attrib['name'])
        # print(dir(root))
    for child in root:
        parseXML(child,sm)
    if len(list(root)) == 0:
        print(sm, ' = ',root.text)
    # else:
        # print(root.tag)

parseXML(root,"")
#uep = root.find('.//cell_definitions//cell_definition')