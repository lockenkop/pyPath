import os

from pyPath.pathGenerator import pyPath

pather = pyPath()

dirStructure = pather.readJsonFile()


def test_createPath():
    for parent, child in dirStructure.items():
        pather.createPath(parent, child)

    assert os.path.exists(os.path.join(pather.CWD, parent))
