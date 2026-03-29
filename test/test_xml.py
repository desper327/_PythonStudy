import xml.etree.ElementTree as ET


tree=ET.parse(r'C:\Users\wb.zhangyang21\Overpass\tmp\modelExport.xml')
root=tree.getroot()
model_override = root.find("Material/DefaultMaterialShader")
print(model_override.tag)
print(model_override.text)
print(model_override.items())
print(model_override.attrib)
print(dir(model_override))