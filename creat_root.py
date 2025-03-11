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

    return mean, std, masse, charge


def multiprocess(file_list):
    with Pool(processes=num_cores) as pool:
        results = pool.map(root_file, file_list)
    mean = [mean for mean in results if mean is not None]
    std = [std for std in results if std is not None]
    masse = [masse for masse in results if masse is not None]
    charge = [charge for charge in results if charge is not None] 


    indexed_means = np.array(mean)
    indexed_std = np.array(std)
    indexed_mass = np.array(masse)
    indexed_charge = np.array(charge)

    return indexed_means, indexed_std, indexed_mass, indexed_charge



if __name__ == "__main__":
    start_time = time.time()



    mean,std,mass,charge = multiprocess(file_list)
    print(mean)
    with uproot.recreate(output_file) as f:
        # f["mean_pt"] = {"mean_pt": np.array(list(mean), dtype=np.float32)}  
        f["tree"] = { "charge" : charge, "mass": mass, "mean_pt" : mean, "std" :std}



    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"time of calculation : {elapsed_time}s")