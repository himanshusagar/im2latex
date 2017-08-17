#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Copyright 2017 Sumeet S Singh

    This file is part of im2latex solution by Sumeet S Singh.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the Affero GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Affero GNU General Public License for more details.

    You should have received a copy of the Affero GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on Sun Jul  9 11:44:46 2017
Tested on python 2.7

@author: Sumeet S Singh
"""
import tensorflow as tf
import tf_commons as tfc
from tf_commons import K

## Tensors with ED == 0
h1 = tf.constant([[[1,2,3],[4,5,6]],
                  [[7,8,9],[10,11,12]],
                  [[13,14,15],[16,17,18]]  ])
l1 = tf.constant([[3, 3],
                  [3, 3],
                  [3, 3]])
print 'Shapes: h1:%s, l1:%s'%(K.int_shape(h1), K.int_shape(l1))
h2 = tf.constant([[[1,2,3,0,0,0,0],[4,5,6,0,0,0,0]],
                  [[7,8,100,9,0,0,0],[100,10,100,11,12,0,0]],
                  [[13,14,15,100,100,100,0],[100,16,17,18,0,0,0]]  ])
l2 = tf.constant([[3, 3],
                  [4, 5],
                  [6, 4]])
print 'Shapes: h2:%s, l2:%s'%(K.int_shape(h2), K.int_shape(l2))
h1_s, l1_s = tfc.squash_3d(3, 2, h1, l1, 100)
print 'Shapes: h1_s:%s, l1_s:%s'%(K.int_shape(h1_s), K.int_shape(l1_s))
h2_s, l2_s = tfc.squash_3d(3, 2, h2, l2, 100)
print 'Shapes: h2_s:%s, l2_s:%s'%(K.int_shape(h2_s), K.int_shape(l2_s))
ed1 = tfc.k_edit_distance(3, 2, h2, l2, h1, l1, 100)
mean1 = tf.reduce_mean(ed1)
ed1_s = tfc.k_edit_distance(3, 2, h2_s, l2_s, h1_s, l1_s, 100)
mean1_s = tf.reduce_mean(ed1_s)

def flatten(h,l):
    B, k, T = K.int_shape(h)
    return tf.reshape(h, (B*k, -1)), tf.reshape(l, (B*k,))

_h1, _l1 = flatten(h1, l1)
_h1_s, _l1_s = flatten(h1_s, l1_s)
_h2, _l2 = flatten(h2, l2)
_h2_s, _l2_s = flatten(h2_s, l2_s)

_ed1 = tfc.edit_distance(6, _h2, _l2, _h1, _l1, 100)
_mean1 = tf.reduce_mean(_ed1)
_ed1_s = tfc.edit_distance(6, _h2_s, _l2_s, _h1_s, _l1_s, 100)
_mean1_s = tf.reduce_mean(_ed1_s)

## Tensor with ED > 0
h2_2 = tf.constant([[[1,2,3,99,0,0,0],[4,5,6,0,0,0,0]],
                  [[7,8,100,99,0,0,0],[100,10,100,11,12,0,0]],
                  [[13,100,15,100,100,100,0],[100,16,17,18,0,0,0]]  ])
l2_2 = tf.constant([[4, 3],
                  [4, 5],
                  [6, 4]])
h2_2_s, l2_2_s = tfc.squash_3d(3, 2, h2_2, l2_2, 100)
_h2_2, _l2_2 = flatten(h2_2, l2_2)
_h2_2_s, _l2_2_s = flatten(h2_2_s, l2_2_s)

ed2 = tfc.k_edit_distance(3, 2, h2_2, l2_2, h1, l1, 100)
ed2_s = tfc.k_edit_distance(3, 2, h2_2_s, l2_2_s, h1_s, l1_s, 100)
sum2 = tf.reduce_sum(ed2)
sum2_s = tf.reduce_sum(ed2_s)
print 'Shape of ed1=%s'%(K.int_shape(ed1),)
print 'Shape of ed2_s=%s'%(K.int_shape(ed2_s),)
_ed2 = tfc.edit_distance(6, _h2_2, _l2_2, _h1, _l1, 100)
_ed2_s = tfc.edit_distance(6, _h2_2_s, _l2_2_s, _h1_s, _l1_s, 100)
_sum2 = tf.reduce_sum(_ed2)
_sum2_s = tf.reduce_sum(_ed2_s)


with tf.Session():
    print ed1.eval()
    assert mean1.eval() == 0.
    print _ed1.eval()
    assert _mean1.eval() == 0.
    print ed1_s.eval()
    assert mean1_s.eval() == 0.
    print _ed1_s.eval()
    assert _mean1_s.eval() == 0.
    print ed2.eval()
    assert sum2.eval() == 1.
    print _ed2.eval()
    assert _sum2.eval() == 1.
    print ed2_s.eval()
    assert sum2_s.eval() == 1.
    print _ed2_s.eval()
    assert _sum2_s.eval() == 1.

