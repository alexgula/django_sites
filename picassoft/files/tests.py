# coding=utf-8
# Tests (to be run with django-nose, although they could easily be adapted to work with unittest)
import shutil
import tempfile
from django.core.files.base import ContentFile as C
from django.core.files import File
from nose.tools import assert_equal

from .storage import OverwritingStorage

class TestOverwritingDefaultStorage(object):
    def setup(self):
        self.location = tempfile.mktemp(prefix="overwriting_storage_test")
        self.storage = OverwritingStorage(location=self.location)

    def teardown(self):
        shutil.rmtree(self.location)

    def test_new_file(self):
        s = self.storage
        assert not s.exists("foo")
        s.save("foo", C("new"))
        assert_equal(s.open("foo").read(), "new")

    def test_overwriting_existing_file_with_string(self):
        s = self.storage

        s.save("foo", C("old"))
        name = s.save("foo", C("new"))
        assert_equal(s.open("foo").read(), "new")
        assert_equal(name, "foo")

    def test_overwrite_with_file(self):
        s = self.storage

        input_file = s.location + "/input_file"
        with open(input_file, "w") as input:
            input.write("new")

        s.save("foo", C("old"))
        name = s.save("foo", File(open(input_file)))

        assert_equal(s.open("foo").read(), "new")
        assert_equal(name, "foo")

    def test_upload_fails(self):
        s = self.storage

        class Explosion(Exception):
            pass

        class ExplodingContentFile(C):
            def __init__(self):
                super(ExplodingContentFile, self).__init__("")

            def chunks(self):
                yield "bad chunk"
                raise Explosion("explode!")

        s.save("foo", C("old"))

        try:
            s.save("foo", ExplodingContentFile())
            raise Exception("Oh no! ExplodingContentFile didn't explode.")
        except Explosion:
            pass

        assert_equal(s.open("foo").read(), "old")
