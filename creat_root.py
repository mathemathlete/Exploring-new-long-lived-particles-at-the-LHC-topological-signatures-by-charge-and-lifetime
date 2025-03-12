import uproot 
import numpy as np 
import glob
import awkward as ak 
from multiprocessing import Pool
import time
import re

file_list = glob.glob(f"root_files/*.root")  # creat a list with all root files in the directory
tree_name = "Ntuple"
num_cores = 6
output_file = "output.root"

def root_file(file_name):
    charge_match = re.search(r'Q([0-9.]+)', file_name)
    masse_match = re.search(r'_M([0-9]+)', file_name)
    charge= float(charge_match.group(1))
    masse = float(masse_match.group(1))
    with uproot.open(file_name) as file:
        tree = file[tree_name]
        data = tree.arrays(library="ak")
        # calculation 
        mean=ak.mean(data["Tracks.pt"])
        std= ak.std(data["Tracks.pt"])

    return charge,masse, mean, std


def multiprocess(file_list):
    with Pool(processes=num_cores) as pool:
        results = pool.map(root_file, file_list)
    vector = [vector for vector in results if vector is not None]
   
    vector = np.array(vector)

    print(vector)
    return vector



if __name__ == "__main__":
    start_time = time.time()



    vector= multiprocess(file_list)

    print(vector[:,0])
    with uproot.recreate(output_file) as f:
        f["tree"] = { "charge" : vector[:,0], "mass": vector[:,1], "mean_pt" : vector[:,2], "std_pt" :vector[:,3]}



    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"time of calculation : {elapsed_time}s")