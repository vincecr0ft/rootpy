#!/usr/bin/env python

from rootpy.tree import Tree, TreeModel
from rootpy.io import open
from rootpy.types import *
from rootpy.vector import LorentzVector
from random import gauss, randint
import ROOT

f = open("test.root", "recreate")


# define the model
class Event(TreeModel):

    # properties of particle "a"
    a_x = FloatCol()
    a_y = FloatCol()
    a_z = FloatCol()

    # properties of particle "b"
    b_x = FloatCol()
    b_y = FloatCol()
    b_z = FloatCol()

    # a collection of particles
    col_x = ROOT.vector("float")
    col_y = ROOT.vector("float")
    col_z = ROOT.vector("float")
    col_n = IntCol()

    # a TLorentzVector
    p = LorentzVector

    i = IntCol()

tree = Tree("test", model=Event)

# fill the tree
for i in xrange(10000):
    tree.a_x = gauss(.5, 1.)
    tree.a_y = gauss(.3, 2.)
    tree.a_z = gauss(13., 42.)

    tree.b_x = gauss(.5, 1.)
    tree.b_y = gauss(.3, 2.)
    tree.b_z = gauss(13., 42.)

    n = randint(1, 10)
    for j in xrange(n):
        tree.col_x.push_back(gauss(.5, 1.))
        tree.col_y.push_back(gauss(.3, 2.))
        tree.col_z.push_back(gauss(13., 42.))
    tree.col_n = n
    
    tree.p.SetPtEtaPhiM(gauss(.5, 1.),
                        gauss(.5, 1.),
                        gauss(.5, 1.),
                        gauss(.5, 1.))

    tree.i = i
    tree.fill(reset=True)
tree.write()

f.Close()
f = open("test.root")

tree = f.test

# define objects by prefix:
tree.define_object(name='a', prefix='a_')
tree.define_object(name='b', prefix='b_')


# define a mixin class to add functionality to a tree object
class Particle(object):

    def who_is_your_daddy(self):

        print "You are!"

# define collections of objects by prefix
tree.define_collection(name='particles',
                       prefix='col_',
                       size='col_n',
                       mixin=Particle)

# loop over "events" in tree
for event in tree:
    print "a.x: %f" % event.a.x
    print "b.y: %f" % event.b.y
    # loop over "particles" in current event
    for p in event.particles:
        print "p.x: %f" % p.x
        p.who_is_your_daddy()
    print event.p.Eta()

f.close()
