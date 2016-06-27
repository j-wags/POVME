import peel
import numpy

filenames = ['frame_1.npy','frame_2.npy','frame_3.npy','frame_4.npy','frame_5.npy']

my_FME = peel.featureMapEnsemble.fromNumpyCoordFiles(filenames)
#my_FME = peel.featureMapEnsemble()
for filename in filenames:
    thisMap = peel.featureMap.fromNpyFile(filename, 1.)
    my_FME.addFeatureMap(thisMap)


print 'my_FME.getBitVector()'
print my_FME.getBitVector()
print 
#print 'my_FME.getCoord2BitVecPos()'
#print my_FME.getCoord2BitVecPos()
#print
print 'my_FME.getNumFeatureMaps()'
print my_FME.getNumFeatureMaps()

my_FME.saveToNPZ('output.npz')

for i in range(my_FME.getNumFeatureMaps()):
    for j in range(i,my_FME.getNumFeatureMaps()):
        overlap = numpy.sum(my_FME.getBitVector()[i] & my_FME.getBitVector()[j])
        print "overlap between frame %i and %i is %i" %(i, j, overlap)
                                                       
#import pylab
#pylab.imshow(my_FME.getBitVector(),
#             #origin='lower',
#             interpolation='nearest',
#             aspect='auto')
#pylab.show()
