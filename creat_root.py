import uproot 
import numpy as np 
import glob
import awkward as ak 
from multiprocessing import Pool
import time
import re
start_time = time.time()

file_list = glob.glob(f"/home/xavier/work/stageM2/code/root_files/*.root")  # creat a list with all root files in the directory
tree_name = "Ntuple"
num_cores = 6
output_file = "output.root"

def root_file(file_name):
    print(file_name)
    charge_match = re.search(r'Q([0-9.]+)', file_name)
    masse_match = re.search(r'_M([0-9]+)', file_name)
    charge= float(charge_match.group(1))
    masse = float(masse_match.group(1))
    print(masse ,charge)
    with uproot.open(file_name) as file:
        tree = file[tree_name]
        data = tree.arrays(library="ak")
        # calculation on Pt 
        mean_pt=ak.mean(data["Tracks.pt"])
        median_pt = ak.percentile(data["Tracks.pt"], 50)
        std_pt= np.sqrt((data["Tracks.pt"]-mean_pt)**2)

    return mean_pt, median_pt, std_pt, masse, charge


def multiprocess(file_list):
    with Pool(processes=num_cores) as pool:
        results = pool.map(root_file, file_list)
    mean = [mean for mean in results if mean is not None]

    indexed_means = np.array(mean)
    return indexed_means    

mean = multiprocess(file_list)
print(mean)
with uproot.recreate(output_file) as f:
    f["mean_pt"] = {"mean_tracks_pt": np.array(list(mean), dtype=np.float32),}  




end_time = time.time()
elapsed_time = end_time - start_time
print(f"time of calculation : {elapsed_time}s")