import uproot 
import numpy as np 
import awkward as ak

file_name= "root_files/Q3_M100.root"
tree_name = "Ntuple/Tracks."
with uproot.open(file_name) as file:
    tree = file[tree_name]

    # Lire toutes les branches
    all_branches = tree.arrays(library="ak")
if ak.num(all_branches["Tracks.eta"]) > 0:
    numpy_array = ak.flatten(all_branches["Tracks.eta"]).to_numpy()  # Aplatir et convertir en NumPy
    mean_value = np.mean(numpy_array)
    print("Moyenne de Tracks.pt :", mean_value)
else:
    print("Aucune donnée dans Tracks.pt")

