import sys
import os
import hou


def generateAlembicNode(abcPath):
    root = hou.node("/obj/geo1")
    obj = root.createNode("alembic")
    obj.parm('fileName').set(abcPath)

def initFileNodes():
    obj = hou.node("/obj")
    obj.createNode("geo")


def run(*args, **kwargs):    
    # ==== args ====
    sourceDirectory = kwargs.get('srcDir', '')
    outDirectory =  kwargs.get('outDir', '')

    if(sourceDirectory == "" or outDirectory == ""):
        print("invalid params")
        return "invalid params"

    outFileName = 'out.hip'
    outDirectory = os.path.join(outDirectory, outFileName)

    hou.hipFile.save(outDirectory)
    hou.hipFile.load(outDirectory)

    # prepare base file
    initFileNodes()
    for file in os.listdir(sourceDirectory):
        if file.endswith(".abc"):
            generateAlembicNode(os.path.join(sourceDirectory, file))

    hou.hipFile.save(outDirectory)
    return "----- Houdini Scene File Generated ! -----"
