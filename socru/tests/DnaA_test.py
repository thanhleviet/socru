import unittest
import os
import shutil
from socru.DnaA  import DnaA

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','dnaa')

class TestDnaA(unittest.TestCase):
   
    def test_dnaa(self):
        d = DnaA(os.path.join(data_dir,'dnaa.fa'), os.path.join(data_dir,'database'), 1 )
        
        self.assertFalse(d.dnaa_orientation)
        self.assertEqual(d.fragment_with_dnaa, str(2))
        
    def test_dnaa_compressed(self):
        d = DnaA(os.path.join(data_dir,'dnaa.fa.gz'), os.path.join(data_dir,'database'), 1 )
        
        self.assertFalse(d.dnaa_orientation)
        self.assertEqual(d.fragment_with_dnaa, str(2))
    
        