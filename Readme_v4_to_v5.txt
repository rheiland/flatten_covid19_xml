~/git/pc4covid19-rheiland-master/data$ grep "<variab" PhysiCell_settings-v4-inherit-orig.xml
                <variable name="virion" units="virion/micron^3" ID="0">
                <variable name="assembled virion" units="virion/micron^3" ID="1">
                <variable name="interferon 1" units="mol/micron^3" ID="2">
                <variable name="pro-inflammatory cytokine" units="mol/micron^3" ID="3">
                <variable name="chemokine" units="mol/micron^3" ID="4">
                <variable name="debris" units="mol/micron^3" ID="5">

~/git/pc4covid19-rheiland-master/data$ grep "<variab" PhysiCell_settings-v5-inherit.xml
                <variable name="virion" units="virion/micron^3" ID="0">
                <variable name="assembled virion" units="virion/micron^3" ID="1">
                <variable name="interferon 1" units="mol/micron^3" ID="2">
                <variable name="pro-inflammatory cytokine" units="mol/micron^3" ID="3">
                <variable name="chemokine" units="mol/micron^3" ID="4">
                <variable name="debris" units="mol/micron^3" ID="5">
                <variable name="pro-pyroptosis cytokine" units="mol/micron^3" ID="6">
                <variable name="anti-inflammatory cytokine" units="mol/micron^3" ID="7">
                <variable name="collagen" units="mol/micron^3" ID="8">
                <variable name="Ig" units="mol/micron^3" ID="9">
                <variable name="ROS" units="mol/micron^3" ID="10">

~/git/pc4covid19-rheiland-master/data$ grep "<cell_definition " PhysiCell_settings-v4-inherit-orig.xml
		<cell_definition name="default" ID="0">
		<cell_definition name="lung epithelium" parent_type="default" ID="1">
		<cell_definition name="immune" parent_type="default" ID="2">
		<cell_definition name="CD8 Tcell" parent_type="immune" ID="3">
		<cell_definition name="macrophage" parent_type="immune" ID="4">
		<cell_definition name="neutrophil" parent_type="immune" ID="5">
		<cell_definition name="DC" parent_type="immune" ID="6">
		<cell_definition name="CD4 Tcell" parent_type="immune" ID="7">

~/git/pc4covid19-rheiland-master/data$ grep "<cell_definition " PhysiCell_settings-v5-inherit.xml
		<cell_definition name="default" ID="0">
		<cell_definition name="lung epithelium" parent_type="default" ID="1">
		<cell_definition name="immune" parent_type="default" ID="2">
		<cell_definition name="CD8 Tcell" parent_type="immune" ID="3">
		<cell_definition name="macrophage" parent_type="immune" ID="4">
		<cell_definition name="neutrophil" parent_type="immune" ID="5">
		<cell_definition name="DC" parent_type="immune" ID="6">
		<cell_definition name="CD4 Tcell" parent_type="immune" ID="7">
		<cell_definition name="fibroblast" parent_type="immune" ID="8">
		<cell_definition name="residual" parent_type="default" ID="9">
------------------------

Insert <uptake_rate> into each <secretion>//<substrate> in "default".

~/git/pc4covid19-rheiland-master/data$ cp PhysiCell_settings_v5_insert_uptake_rates.xml PhysiCell_settings.xml



