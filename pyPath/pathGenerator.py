import os
import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox
import json
# Translation dictionary
translations = {
    'en': {
        "Project Directory Creation": "Project Directory Creation",
        "Project Number:": "Project Number:",
        "Project Name:": "Project Name:",
        "Select Path": "Select Path",
        "No path selected": "No path selected",
        "Create Project Directory": "Create Project Directory",
        "Add Entry": "Add Entry",
        "Remove Entry": "Remove Entry",
        "Save Directory Structure": "Save Directory Structure",
        "Input": "Input",
        "Enter new directory name:": "Enter new directory name:",
        "Confirm Delete": "Confirm Delete",
        "Are you sure you want to delete the selected entry?": "Are you sure you want to delete the selected entry?",
        "Directory structure saved to dir_structure.json": "Directory structure saved to dir_structure.json"
    },
    'de': {
        "Project Directory Creation": "ProjektVerzeichnisErstellung",
        "Project Number:": "Projektnummer:",
        "Project Name:": "Projektname:",
        "Select Path": "Pfad auswählen",
        "No path selected": "Kein Pfad ausgewählt",
        "Create Project Directory": "Projektverzeichnis erstellen",
        "Add Entry": "Eintrag hinzufügen",
        "Remove Entry": "Eintrag entfernen",
        "Save Directory Structure": "Verzeichnisstruktur speichern",
        "Input": "Eingabe",
        "Enter new directory name:": "Neuen Verzeichnisnamen eingeben:",
        "Confirm Delete": "Löschen bestätigen",
        "Are you sure you want to delete the selected entry?": "Sind Sie sicher, dass Sie den ausgewählten Eintrag löschen möchten?",
        "Directory structure saved to dir_structure.json": "Verzeichnisstruktur in dir_structure.json gespeichert"
    }
}

# Current language
current_language = 'de'

def _(text):
    return translations[current_language].get(text, text)

class pyPath:
    def __init__(self):
        self.dirStructure = self.load_dir_structure("dir_structure.json")
        if not self.dirStructure:
            self.dirStructure = {
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

        # Create the main application window
        self.root = tk.Tk()
        self.root.title(_("Project Directory Creation"))
        self.root.geometry("400x500")

        # Frame for project details
        project_frame = ttk.Frame(self.root)
        project_frame.pack(pady=5, fill=tk.X)

        # Project number
        self.project_number_label = tk.Label(project_frame, text=_("Project Number:"))
        self.project_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.project_number_entry = tk.Entry(project_frame)
        self.project_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Project name
        self.project_name_label = tk.Label(project_frame, text=_("Project Name:"))
        self.project_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.project_name_entry = tk.Entry(project_frame)
        self.project_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Configure the second column to expand
        project_frame.columnconfigure(1, weight=1)

        # Add a button to open the file dialog
        self.select_button = tk.Button(
            self.root, text=_("Select Path"), command=self.select_path
        )
        self.select_button.pack(pady=5)

        # Add a label to display the selected path
        self.path_label = tk.Label(self.root, text=_("No path selected"))
        self.path_label.pack(pady=5)

        self.create_button = tk.Button(
            self.root, text=_("Create Project Directory"), command=self.createDirectories
        )
        self.create_button.pack(pady=5)

        treeView_frame = ttk.Frame(self.root)
        treeView_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.treeView = ttk.Treeview(treeView_frame)
        self.treeView.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollBar = ttk.Scrollbar(
            treeView_frame, orient="vertical", command=self.treeView.yview
        )
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeView.configure(yscrollcommand=self.scrollBar.set)

        # Add buttons for adding and removing entries
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, pady=5)

        # Add buttons for adding and removing entries
        self.add_button = tk.Button(
            button_frame, text=_("Add Entry"), command=self.add_entry
        )
        self.add_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.remove_button = tk.Button(
            button_frame, text=_("Remove Entry"), command=self.remove_entry
        )
        self.remove_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(
            self.root, text=_("Save Directory Structure"), command=self.save_dir_structure
        )
        self.save_button.pack(pady=5)

        self.insert_items(self.dirStructure)

        self.root.mainloop()

        self.CWD = os.getcwd()


    def createDirectories(self, dirStructure=None, base_path=None):
        if dirStructure is None:
            dirStructure = self.dirStructure
        if base_path is None:
            base_path = os.path.join(self.path, self.project_number_entry.get() + "_" + self.project_name_entry.get())

        for directory, substructure in dirStructure.items():
            new_path = os.path.join(base_path, directory)
            os.makedirs(new_path, exist_ok=True)

            if isinstance(substructure, dict):
                self.createDirectories(substructure, new_path)

    def createJsonFile(self):
        with open("dirStructure.txt", "w") as dirFile:
            dirFile.write(json.dumps(self.dirStructure))

    def readJsonFile(self):
        with open("dirStructure.txt", "r") as dirFile:
            self.dirStructure = json.load(dirFile)
            for parent, child in self.dirStructure.items():
                self.insert_items(self.dirStructure)

    # Function to open file dialog and get the selected path
    def select_path(self):
        self.path = filedialog.askdirectory()  # This opens a directory selection dialog
        if self.path:  # If a path is selected, update the label
            self.path_label.config(text=self.path)

    def insert_items(self, structure, parent=""):
        for directory, substructure in structure.items():
            node_id = self.treeView.insert(parent, "end", text=directory)
            if isinstance(substructure, dict):
                self.insert_items(substructure, parent=node_id)

    def add_entry(self):
        selected_item = self.treeView.selection()
        if selected_item:
            parent_item = selected_item[0]
        else:
            parent_item = ""

        new_entry = simpledialog.askstring(_("Input"), _("Enter new directory name:"))
        if new_entry:
            self.treeView.insert(parent_item, "end", text=new_entry)
            self.update_dir_structure()

    def remove_entry(self):
        selected_item = self.treeView.selection()
        if selected_item:
            confirm = messagebox.askyesno(
                _("Confirm Delete"), _("Are you sure you want to delete the selected entry?")
            )
            if confirm:
                self.treeView.delete(selected_item[0])
                self.update_dir_structure()

    def update_dir_structure(self):
        def get_structure(item):
            children = self.treeView.get_children(item)
            if not children:
                return {}
            structure = {}
            for child in children:
                text = self.treeView.item(child, "text")
                structure[text] = get_structure(child)
            return structure

        self.dirStructure = get_structure("")

    def save_dir_structure(self):
        with open("dir_structure.json", "w") as f:
            json.dump(self.dirStructure, f, indent=4)
        messagebox.showinfo(
            _("Save Directory Structure"),
            _("Directory structure saved to dir_structure.json"),
        )

    def load_dir_structure(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return None
