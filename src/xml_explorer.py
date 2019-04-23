import os
import xml.etree.ElementTree as ET

classes_conhecidas = ["copo","papel","sacola","embalagem"]
classes = []

# pegando a o caminho a pasta e os arquivos
for root, dirs, files in os.walk("."):  
    for filename in files:
        if ".xml" in filename:
            mydoc = ET.parse(filename)
            root = mydoc.getroot()
            # print(type(root))
            for child in root:
                # print(child.tag)
                if(child.tag == "object"):
                    # print(child.tag)
                    for i in child:
                        if (i.tag == "name"):
                            # print("classe = {}".format(i.text))
                            if(i.text not in classes):
                                classes.append(i.text)
                                if(i.text not in classes_conhecidas):
                                    print(i.text)
                                    if("cop" in i.text):
                                        print("era pra ser copo mas é {}".format(i.text))
                                    elif("pap" in i.text):
                                        print("era pra ser papel mas é ".format(i.text))
                                    elif("sa" in i.text):
                                        print("era pra ser sacola mas é ".format(i.text))
                                    elif("em" in i.text):
                                        print("era pra ser embalagem mas é ".format(i.text))
                                   
print(classes)