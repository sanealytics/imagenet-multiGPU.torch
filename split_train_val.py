import os, errno
import shutil
import math
import random

def move(className, f, tgt):
  srcDir = "{}/{}".format(source, className)
  tgtDir = "{}/{}".format(target, tgt)
  tgtClassDir = "{}/{}".format(tgtDir, className)
  print("Moving {} from {} -> {}".format(f, \
    srcDir, \
    tgtClassDir))
  if not os.path.exists(tgtDir):
    print("Making", tgtDir)
    os.mkdir(tgtDir)
  if not os.path.exists(tgtClassDir):
    print("Making", tgtClassDir)
    os.mkdir(tgtClassDir)
  # To move or to copy???
  os.rename( \
  #shutil.copyfile( \
    "{}/{}".format(srcDir, f), \
    "{}/{}".format(tgtClassDir, f))

def split(source, target, splitProb):
  train = open('train.txt', 'w')
  val   = open('val.txt'  , 'w')
  classes = 0
  for className in os.listdir(source): # Could do in parallel but bah
  #for className in ["YK3"]: #os.listdir(source): # Could do in parallel but bah
    for root, directories, files in os.walk("{}/{}".format(source, className)):
      numberOfFiles = len(files)
      if numberOfFiles >= 10: # threshold
        shuffled = random.sample(files, numberOfFiles) # Shuffle
        numberOfTrain = 0
        numberOfVal = 0
        for idx in range(numberOfFiles):
          if (idx < (splitProb * numberOfFiles)):
            move(className, shuffled[idx], "train") # Will work for edge case of 1 example as well
            train.write('"{}/{}/{}", {}\n'.format(source, className, shuffled[idx], className))
            numberOfTrain += 1
          else:
            move(className, shuffled[idx], "val")
            val.write('"{}/{}/{}", {}\n'.format(source, className, shuffled[idx], className))
            numberOfVal += 1
        if numberOfVal == 0: # Should never happen if threshold > 1
          print("WARNING: Imbalanced class, balancing manually")
          move(className, shuffled[0], "val")
          val.write('"{}/{}/{}", {}\n'.format(source, className, shufled[0], className))
        classes = classes + 1
        assert(numberOfTrain > 0)
        assert(numberOfVal > 0)
  train.close()
  val.close()
  return classes

source = 'data'
target = 'split'
splitProb = .8
classes = split(source, target, splitProb)
print classes, " classes split"


