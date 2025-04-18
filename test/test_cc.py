import numpy as np
import tempfile
import unittest
from twixtools import read_twix
import twixzip
from twixzip.twixzip import suppress_stdout_stderr


infile = 'example_data/gre.dat'


class test_scc(unittest.TestCase):

    def test(self):

        with suppress_stdout_stderr():
            twix = read_twix(infile, keep_acqend=True)[-1]

        nc = twix['mdb'][1].mdh.UsedChannels

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_dat:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(
                    infile=infile, outfile=out_h5.name, cc_mode='scc', ncc=nc)
                twixzip.reconstruct_twix(
                    infile=out_h5.name, outfile=out_dat.name)

            with suppress_stdout_stderr():
                twix = read_twix(infile, keep_acqend=True)[-1]
                twix_new = read_twix(out_dat.name, keep_acqend=True)[-1]

            for mdb, mdb_new in zip(twix['mdb'], twix_new['mdb']):
                if mdb.is_flag_set('ACQEND'):
                    continue
                elif mdb.is_flag_set('SYNCDATA'):
                    continue

                self.assertTrue(mdb.mdh == mdb_new.mdh,
                                'scc: mdhs do not match')
                self.assertTrue(np.allclose(mdb.data, mdb_new.data),
                                'scc: mdb data not within tolerance')


class test_gcc(unittest.TestCase):

    def test(self):

        with suppress_stdout_stderr():
            twix = read_twix(infile, keep_acqend=True)[-1]

        nc = twix['mdb'][1].mdh.UsedChannels

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_dat:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(
                    infile=infile, outfile=out_h5.name, cc_mode='gcc', ncc=nc)
                twixzip.reconstruct_twix(
                    infile=out_h5.name, outfile=out_dat.name)

            with suppress_stdout_stderr():
                twix = read_twix(infile, keep_acqend=True)[-1]
                twix_new = read_twix(out_dat.name, keep_acqend=True)[-1]

            for mdb, mdb_new in zip(twix['mdb'], twix_new['mdb']):
                if mdb.is_flag_set('ACQEND'):
                    continue
                elif mdb.is_flag_set('SYNCDATA'):
                    continue

                self.assertTrue(mdb.mdh == mdb_new.mdh,
                                'gcc: mdhs do not match')
                self.assertTrue(np.allclose(mdb.data, mdb_new.data),
                                'gcc: mdb data not within tolerance')


if __name__ == '__main__':
    unittest.main()
