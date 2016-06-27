python binding_site_overlap.py -f POVME_frame_*npy
../../arun python cluster.py -m POVME_Tanimoto_matrix_.npy -i indexMapToFrames.csv -t POVME_:../../POVME/examples/POVME_example/4NSS.pdb 
