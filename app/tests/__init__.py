#-*- coding:utf-8 -*-
"""
$Id$
"""
import os
import unittest
from django.test.simple import doctest, DocTestRunner, doctestOutputChecker

import test_ft

def suite():
    res = unittest.TestSuite()

    res.addTest(doctest.DocTestSuite(test_ft,
                                     checker=doctestOutputChecker,
                                     runner=DocTestRunner,
                                     globs={'getLast': getLast,
                                            'test_stuff': os.path.dirname(__file__) +'/stuff/'
                                            }))

    return res
    
def getLast(cls):
    obj = cls.objects.all().order_by('-id')[0]
    return obj
