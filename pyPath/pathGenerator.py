import os
import tkinter as tk
from tkinter import filedialog, ttk
import json


class pyPath:
    def __init__(self):
        self.CWD = os.getcwd()

        self.dirStructure = {}
        self.dirStructure_fallback = {
            "00_Allgemeines": "",
            "01_Vertragsunterlagen": "",
            "02_Schriftverkehr": "",
            "03_Zuarbeiten": {  # child True
                "Bahngeodaten": "",
                "Baugrund": "",
                "Schall": "",
                "TRE": "",
                "V3_Meldungen": "",
                "Vermess": "",
                "Übergabe": "",
            },
            "04_Dokumentation": "",
            "05_Protokolle": "",
            "06_CAD": {  # child True
                "Konstruktion": "",
                "ProVI": {  # child True
                    "Arbverz": ""
                },
            },
            "07_EPmitKosten": "",
            "08_GP": "",
            "09_AP": "",
            "10_AU": "",
            "11_Bestand": "",
            "12_Material": "",
            "13_TILOS": "",
        }

    def createPath(self, element, childs):
        cwd = self.CWD
        # check if this element has childs
        if isinstance(childs, dict):
            # recurse for every child, where child is the new element
            for child, subchild in childs.items():
                self.createPath(child, subchild, cwd=os.path.join(cwd, element))
        else:
            # if there are no childs we are at max recursions needed and can just create the directory
            pathToCreate = os.path.join(cwd, element)
            os.makedirs(pathToCreate, exist_ok=True)

    def createDirectories(self):
        for element, childs in self.dirStructure.items():
            self.createPath(element, childs)

    def createJsonFile(self):
        with open("dirStructure.txt", "w") as dirFile:
            dirFile.write(json.dumps(self.dirStructure_fallback))

    def readJsonFile(self):
        with open("dirStructure.txt", "r") as dirFile:
            dirStructure = json.load(dirFile)
            for parent, child in dirStructure.items():
                self.displayTreeview(parent, child)

    # Function to open file dialog and get the selected path
    def select_path(self):
        path = filedialog.askdirectory()  # This opens a directory selection dialog
        if path:  # If a path is selected, update the label
            self.path_label.config(text=path)

    def displayTreeview(self, parent, child, parentID=""):
        # check if this element has childs
        if isinstance(child, dict):
            # create the parent first
            if not parentID:
                parentID = self.treeView.insert("", tk.END, text=parent)
            print(f"inserted {parent} in {parentID}")
            # recurse for every child, where child is the new element
            for parent, child in child.items():
                self.displayTreeview(parent, child, parentID=parentID)
        else:
            # latest parent
            self.treeView.insert(parentID, tk.END, parent, text=parent)
            print(f"inserted {parent} in {parentID}")

    def createGui(self):
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Path Selection Dialog")
        self.root.geometry("400x400")

        # Add a button to open the file dialog
        self.select_button = tk.Button(
            self.root, text="Select Path", command=self.select_path
        )
        self.select_button.pack(pady=10)

        # Add a label to display the selected path
        self.path_label = tk.Label(self.root, text="No path selected")
        self.path_label.pack(pady=5)

        self.create_button = tk.Button(
            self.root, text="create directories", command=self.createDirectories
        )
        self.create_button.pack(pady=5)

        self.write_dir_file_button = tk.Button(
            self.root, text="write dir file", command=self.createJsonFile
        )
        self.write_dir_file_button.pack(pady=5)

        self.read_dir_file_button = tk.Button(
            self.root, text="read dir file", command=self.readJsonFile
        )
        self.read_dir_file_button.pack(pady=5)
        # Start the Tkinter event loop

        self.treeView = ttk.Treeview(self.root)
        self.treeView.pack(side="right")

        self.root.mainloop()
