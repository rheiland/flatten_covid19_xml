
# Manually insert missing params into "default" cell_definition in <secretion>, e.g. multiple:
<uptake_rate units="1/min">0.0</uptake_rate>
<secretion_rate units="1/min">0</secretion_rate>
then:

~/git/pc4covid19-rheiland-master/data$
cp PhysiCell_settings-insert-default-uptake_rates.xml PhysiCell_settings.xml
python flatten_covid19_cell_def_xml.py   # assumes that it uses PhysiCell_settings.xml!
or,
python flatten_covid19_cell_def_xml-v4.py   # assumes that it uses PhysiCell_settings.xml!

#   Run the output file thru a XML validator, e.g., 
https://www.freeformatter.com/xml-validator-xsd.html  (just don't provide an XSD)

python create_cell_types.py flat.xml
cp flat.xml PhysiCell_settings.xml 
# Make sure it has: <folder>.</folder> AND <omp_num_threads>=4
cp cell_types.py ../bin

# may need to re-run xml2jupyter:
#   python xml2jupyter.py PhysiCell_settings.xml
#   diff microenv_params.py ../bin/microenv_params.py
#   diff user_params.py ../bin/user_params.py
#   cp user_params.py ../bin
#   cp microenv_params.py ../bin

# may need to update data/initial.xml
