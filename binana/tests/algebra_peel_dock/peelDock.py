
import itertools
import peel
import numpy
import sys
import os
import scipy.ndimage.interpolation as sni
import cPickle
import csv

features = ['aromatic','hbondAcceptor','hbondDonor','hydrophilic','hydrophobic','occupancy','adjacency']

#receptorDir = 'POVME_outputs_20140816shapes'
receptorDir = './'
#ligandDir = 'ligandFM_20140816shapes'
#ligandDir = 'ligandPdbs'
#outputDir = 'dockingResults_20140816shapes_peelDock_fullRadius'
ligandDir = './'
outputDir = './'
#receptorName = sys.argv[1]
#ligandName = sys.argv[2]
receptorName = '2B52'
ligandName = '2B52-results_5645.pdb'

receptorData = {}
#ligandData = {}
for feature in features:
    #thisReceptorName = 'proteinFM/%s%s_.npy' %(receptorName, feature)
    thisReceptorName = '%s/%s%s_.npy' %(receptorDir, receptorName, feature)
    thisReceptorData = numpy.load(thisReceptorName)
    receptorData[feature] = peel.featureMap.fromPovmeList(thisReceptorData, 1.)


#with open('%s/%s.pdb' %(ligandDir, ligandName)) as my_file:
    #ligandData = cPickle.load(my_file)

ligandFile = '%s/%s' %(ligandDir,ligandName)
ligandObj = peel.PDB()
ligandObj.LoadPDB(ligandFile)
ligandPeel = peel.peel(ligandObj, peel.defaultParams, isLigand=True)

my_algebra = peel.algebra()

#scoreMaps, scores = my_algebra.scoreAll(receptorData, ligandData)



number = str(5)
nsteps = str(500)

outputFile = number + "_" + nsteps
#os.system('/lv_scratch/j5wagner/projects/POVME_docking_inputs/points_on_sphere/4d_points_on_sphere.o ' + number + " " + nsteps + " > " + outputFile + '.out')
spherePoints = numpy.genfromtxt(outputFile + '.out',skip_header=3, skip_footer=0, usecols=(4,5,6,7), 
comments='}')
#spherePoints[0,:] = numpy.array([0.,1.,0.,0.])
spherePoints = numpy.array([[0.,1.,0.,0.]])
#spherePoints = [[0,1,0,0]]
print spherePoints



n_cubes = 50
#ligandDim = ligandData['aromatic'].getShape()
#receptorDim = receptorData['aromatic'].shape
#receptorSize = receptorData['aromatic'].getData().size
#print ligandDim, receptorDim, receptorSize
#cubeLength = (receptorSize / n_cubes) ** .33333333
#print cubeLength
#x = []
#y = []
#z = []
#for n in numpy.arange(0,receptorDim[0]-ligandDim[0],cubeLength):
#	x.append(n)
#for n in numpy.arange(0,receptorDim[1]-ligandDim[1],cubeLength):
#	y.append(n)
#for n in numpy.arange(0,receptorDim[2]-ligandDim[2],cubeLength):
#	z.append(n)
#translation_list = list(itertools.product(range(-8,9,2),range(-8,9,2),range(-8,9,2)))
#print translation_list
my_score_functions = ['hbondDonor_A * hbondAcceptor_B',]
#my_score_functions = ['hydrophobic_A * hydrophobic_B',
#                     'hydrophilic_A * hydrophilic_B', 
#                     'hydrophilic_A * hydrophobic_B', 
#                     'hydrophobic_A * hydrophilic_B', 
#                     'hbondDonor_A * hbondAcceptor_B',
#                     'hbondAcceptor_A * hbondDonor_B',
#                     'hbondAcceptor_A * hbondAcceptor_B',
#                     'hbondDonor_A * hbondDonor_B',
#                     'aromatic_A * aromatic_B',
#                     'occupancy_A * occupancy_B',
#                     'adjacency_A * occupancy_B',
#                     'occupancy_A * adjacency_B',
#                     'adjacency_A * adjacency_B']
my_algebra.setScoreFuncs(my_score_functions)
translation_list=[(0,0,0)]
a = my_algebra.dockOne(receptorData, receptorData, translation_list, spherePoints)
#a = my_algebra.dockPeel(receptorData, ligandPeel, translation_list, spherePoints)
#a = my_algebra.dockPeel(receptorData, receptorData, translation_list, spherePoints)

ogp = numpy.array([[i[0][0], i[0][1], i[0][2], i[2][0]] for i in a])

#print ogp

myfm = peel.featureMap.fromOffGridPts(ogp, 1.0)

myfm.write_pdb('hbonds.pdb')

with open('%s/results_%s.cPickle' %(outputDir, ligandName), 'w') as fo:
    cPickle.dump(a, fo)



'''import peel
import numpy
import sys
import cPickle

features = ['aromatic','hbondAcceptor','hbondDonor','hydrophilic','hydrophobic','hydrophobicity','occupancy']

receptorName = sys.argv[1]
ligandName = sys.argv[2]

receptorData = {}
#ligandData = {}
for feature in features:
    thisReceptorName = 'proteinFM/%s%s_.npy' %(receptorName, feature)
    thisReceptorData = numpy.load(thisReceptorName)
    receptorData[feature] = peel.featureMap.fromPovmeList(thisReceptorData, 1.)


with open('ligandFM/%s_featureMaps.cPickle' %(ligandName)) as my_file:
    ligandData = cPickle.load(my_file)

my_algebra = peel.algebra()

scoreMaps, scores = my_algebra.scoreAll(receptorData, ligandData)

print my_algebra.getScoreFuncs()
print scores
'''
