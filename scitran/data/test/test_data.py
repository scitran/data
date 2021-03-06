# @Author: Kevin S Hahn

"""Test nimsdata package."""

import os
import glob
import numpy as np

from nose.plugins.attrib import attr
from numpy.testing.decorators import skipif
from nose.tools import ok_, eq_, raises, assert_raises

import scitran.data as scidata
import scitran.data.tempdir as tempfile

# data is stored separately in nimsdata_testdata
# located at the top level of the testing directory
DATADIR = os.path.join(os.path.dirname(__file__), 'testdata')
if not os.path.isdir(DATADIR):
    DATADIR = None

# check that all types definied in MODULES.json can
# be accessed via <tier>_properties_by_type_list
# these tests serve two purposes
# 1. test the top level function to get various propreties by type list
# 2. test that each module defined in modules.json have properties define
# makes use of dict_merge and module_by_type
class test_properties_by_type_list(object):

    def setUp(self):
        types = scidata.data.MODULES
        self.type_list = []
        for t in types:
            if '.' in t:
                type_tuple = t.split('.')
            else:
                type_tuple = (t, None)
            self.type_list.append(type_tuple)

    def test_fail_module_by_type(self):
        assert_raises(scidata.DataError, scidata.data.module_by_type, ('fake', 'type'))

    def test_fail_dict_merge(self):
        assert_raises(scidata.DataError, scidata.dict_merge, [], [])

    def test_acquisition(self):
        ok_(scidata.acquisition_properties_by_type_list(self.type_list))

    def test_session(self):
        ok_(scidata.session_properties_by_type_list(self.type_list))

    def test_project(self):
        ok_(scidata.project_properties_by_type_list(self.type_list))


# Test the parse interface, without getting into any of the parsers
# make sure errors are being raised in the right places
# makes use of _get_handler, and _parse_dataset
class test_parse(object):

    @skipif(not DATADIR)
    def setUp(self):
        pass

    def test_get_handler(self):
        READERS = scidata.data.READERS
        assert_raises(scidata.DataError, scidata.get_handler, 'fake.fake.fake', READERS)   # doesn't exost
        assert_raises(scidata.DataError, scidata.get_handler, 'fake.fake', READERS)        # FIXME
        assert_raises(scidata.DataError, scidata.get_handler, 'fake', READERS)             # FIXME

    @skipif(not DATADIR)
    def test_input_not_found(self):
        assert_raises(scidata.DataError, scidata.parse, './fake.tgz')

    @skipif(not DATADIR)
    def test_ignore_json_without_filetype(self):
        assert_raises(scidata.DataError, scidata.parse, './fake.tgz', ignore_json=True)

    @skipif(not DATADIR)
    def test_no_json_in_tgz(self):
        assert_raises(scidata.DataError, scidata.parse, './nojson.tgz')

    @skipif(not DATADIR)
    def test_invalid_input(self):
        assert_raises(scidata.DataError, scidata.parse, './')
        assert_raises(scidata.DataError, scidata.parse, __file__)

class test_all_readers(object):

    @skipif(not DATADIR)
    def setUp(self):
        self.readers = scidata.data.READERS

    @skipif(not DATADIR)
    def all_readers(object):
        # good test data must follow specific naming convention
        for filetype in self.readers.iterkeys():
            parser = scidata.get_handler(filetype)


# test the write interface, without actually getting into any of the writers
class test_write(object):

    @skipif(not DATADIR)
    def setUp(self):
        testdata = os.path.join(DATADIR, 'ge_dcm_mr_localizer.tgz')
        self.ds = scidata.parse(testdata, load_data=True)

    @skipif(not DATADIR)
    def test_nifti_write(self):
        with tempfile.TemporaryDirectory() as tempdir:
            outbase = os.path.join(tempdir, 'trashme')
            scidata.write(self.ds, self.ds.data, filetype='nifti', outbase=outbase)
            print glob.glob(outbase + '*')
            assert (len(glob.glob(outbase + '*')) >= 1)

    @skipif(not DATADIR)
    def test_no_filetype(self):
        assert_raises(scidata.DataError, scidata.write, self.ds, self.ds.data, filetype=None, outbase='trashme')

    @skipif(not DATADIR)
    def test_empty_meta(self):
        eq_(scidata.write(None, self.ds.data, filetype='nifti', outbase='trashme'), [])

    @skipif(not DATADIR)
    def test_empty_data(self):
        eq_(scidata.write(self.ds, None, filetype='nifti', outbase='trashme'), [])

# how to write tests for the abstract classes NIMSReader and NIMSWriter
# they are non instantiable, and have no class methods that can be tested
# XXX. i'm not sure what the best approcah is.
