# Copyright 2018 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for chromite.lib.repo_manifest."""

import io
import os
import pickle
from xml.etree import ElementTree

from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.utils import repo_manifest


MANIFEST_OUTER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<manifest>%s</manifest>
"""

INCLUDES_XML = """
  <include name="include.xml"/>
  <include name="include_me_too.xml"/>
"""

REMOTES_XML = """
  <remote name="simple_remote"
          fetch="http://simple.example.com"/>
  <remote name="complex_remote" alias="cplx"
          fetch="http://example.com"
          pushurl="http://example.com/push"
          review="http://review.example.com"
          revision="refs/heads/main"/>
"""

DEFAULT_XML = '<default remote="simple_remote" upstream="default_upstream"/>'

SIMPLE_PROJECT_XML = '<project name="simple/project"/>'

COMPLEX_PROJECT_XML = """
  <project name="complex/project" path="src/complex" revision="cafe"
           remote="complex_remote" upstream="refs/heads/main">
    <annotation name="branch-mode" value="pin"/>
  </project>
"""

MANIFEST_XML = MANIFEST_OUTER_XML % (
    REMOTES_XML + DEFAULT_XML + SIMPLE_PROJECT_XML + COMPLEX_PROJECT_XML
)


def ManifestToString(manifest):
    """Return the given Manifest's XML data as a string."""
    buf = io.BytesIO()
    manifest.Write(buf)
    return buf.getvalue().decode("utf-8")


class XMLTestCase(cros_test_lib.TestCase):
    """Mixin for XML tests."""

    def AssertXMLAlmostEqual(self, xml1, xml2) -> None:
        """Check that two XML strings are semanitcally equal."""

        def Normalize(xml):
            elem = ElementTree.fromstring(xml)
            return ElementTree.tostring(elem, encoding="unicode")

        self.assertMultiLineEqual(Normalize(xml1), Normalize(xml2))

    def ETreeFromString(self, xml_data):
        """Return an ElementTree object with the given data."""
        return ElementTree.ElementTree(ElementTree.fromstring(xml_data))


class ManifestTest(cros_test_lib.TempDirTestCase, XMLTestCase):
    """Tests for repo_manifest.Manifest."""

    def setUp(self) -> None:
        self.manifest = repo_manifest.Manifest.FromString(MANIFEST_XML)

    def testInitEmpty(self) -> None:
        """Test Manifest.__init__ on the emptiest valid input."""
        etree = self.ETreeFromString(MANIFEST_OUTER_XML % "")
        repo_manifest.Manifest(etree)

    def testInitInvalidManifest(self) -> None:
        """Test Manifest.__init__ on invalid input."""
        etree = self.ETreeFromString("<foo/>")
        with self.assertRaises(repo_manifest.InvalidManifest):
            repo_manifest.Manifest(etree)

    def testInitUnsupportedFeatures(self) -> None:
        """Test Manifest.__init__ on input with unsupported features."""
        for inner_xml in (
            "<project><project/></project>",
            "<extend-project/>",
            "<remove-project/>",
            "<include/>",
        ):
            etree = self.ETreeFromString(MANIFEST_OUTER_XML % inner_xml)
            with self.assertRaises(repo_manifest.UnsupportedFeature):
                repo_manifest.Manifest(etree)
            repo_manifest.Manifest(etree, allow_unsupported_features=True)

    def testPickle(self) -> None:
        """Test Manifest picklability."""
        pickled = pickle.dumps(self.manifest)
        unpickled = pickle.loads(pickled)
        self.AssertXMLAlmostEqual(ManifestToString(unpickled), MANIFEST_XML)
        with self.assertRaises(repo_manifest.UnsupportedFeature):
            next(unpickled.Includes())

    def testPickleUnsupportedFeatures(self) -> None:
        """Test Manifest picklability when unsupported features are allowed."""
        manifest_xml = MANIFEST_OUTER_XML % INCLUDES_XML
        manifest = repo_manifest.Manifest.FromString(
            manifest_xml, allow_unsupported_features=True
        )
        pickled = pickle.dumps(manifest)
        unpickled = pickle.loads(pickled)
        self.AssertXMLAlmostEqual(ManifestToString(unpickled), manifest_xml)
        self.assertIsNotNone(next(unpickled.Includes()))

    def testFromFile(self) -> None:
        """Test Manifest.FromFile."""
        path = os.path.join(self.tempdir, "manifest.xml")
        osutils.WriteFile(path, MANIFEST_XML)
        manifest = repo_manifest.Manifest.FromFile(path)
        self.assertIsNotNone(manifest.GetUniqueProject("simple/project"))

    def testFromString(self) -> None:
        """Test Manifest.FromString."""
        manifest = repo_manifest.Manifest.FromString(MANIFEST_XML)
        self.assertIsNotNone(manifest.GetUniqueProject("simple/project"))

    def testWrite(self) -> None:
        """Test Manifest.Write."""
        manifest_data = ManifestToString(self.manifest)
        self.AssertXMLAlmostEqual(MANIFEST_XML, manifest_data)

    def testDefault(self) -> None:
        """Test Manifest.Default."""
        self.assertEqual(self.manifest.Default().remote, "simple_remote")

    def testDefaultMissing(self) -> None:
        """Test Manifest.Default with no <default>."""
        manifest = repo_manifest.Manifest.FromString(MANIFEST_OUTER_XML % "")
        self.assertIsNone(manifest.Default().remote)

    def testIncludes(self) -> None:
        manifest = repo_manifest.Manifest.FromString(
            MANIFEST_OUTER_XML % INCLUDES_XML, allow_unsupported_features=True
        )
        include_names = [i.name for i in manifest.Includes()]
        self.assertCountEqual(
            include_names, ["include.xml", "include_me_too.xml"]
        )

    def testRemotes(self) -> None:
        """Test Manifest.Remotes."""
        remote_names = [x.name for x in self.manifest.Remotes()]
        self.assertCountEqual(remote_names, ["simple_remote", "complex_remote"])

    def testGetRemote(self) -> None:
        """Test Manifest.GetRemote."""
        remote = self.manifest.GetRemote("simple_remote")
        self.assertEqual(remote.name, "simple_remote")

    def testGetRemoteMissing(self) -> None:
        """Test Manifest.GetRemote without named <remote>."""
        with self.assertRaises(ValueError):
            self.manifest.GetRemote("missing")

    def testHasRemote(self) -> None:
        """Test Manifest.HasRemote."""
        result = self.manifest.HasRemote("simple_remote")
        self.assertEqual(result, True)

    def testHasRemoteMissing(self) -> None:
        """Test Manifest.HasRemote without named <remote>."""
        result = self.manifest.HasRemote("missing")
        self.assertEqual(result, False)

    def testProjects(self) -> None:
        """Test Manifest.Projects."""
        project_names = [x.name for x in self.manifest.Projects()]
        self.assertCountEqual(
            project_names, ["simple/project", "complex/project"]
        )

    def testGetUniqueProject(self) -> None:
        """Test Manifest.GetUniqueProject."""
        project = self.manifest.GetUniqueProject("simple/project")
        self.assertEqual(project.name, "simple/project")

    def testGetUniqueProjectBranch(self) -> None:
        """Test Manifest.GetUniqueProject with an explicit branch."""
        project = self.manifest.GetUniqueProject("complex/project", "cafe")
        self.assertEqual(project.name, "complex/project")

    def testGetUniqueProjectMissing(self) -> None:
        """Test Manifest.GetUniqueProject without named <project>."""
        with self.assertRaises(ValueError):
            self.manifest.GetUniqueProject("missing/project")

    def testGetUniqueProjectMissingBranch(self) -> None:
        """Test Manifest.GetUniqueProject with valid project, missing branch."""
        with self.assertRaises(ValueError):
            self.manifest.GetUniqueProject("complex/project", "wrong_branch")


class ManifestElementExample(repo_manifest._ManifestElement):
    """_ManifestElement testing example."""

    # pylint: disable=protected-access

    ATTRS = ("name", "other_attr")
    TAG = "example"


class ManifestElementTest(XMLTestCase):
    """Tests for repo_manifest._ManifestElement."""

    # pylint: disable=attribute-defined-outside-init

    XML = '<example name="value"/>'

    def setUp(self) -> None:
        element = ElementTree.fromstring(self.XML)
        self.example = ManifestElementExample(None, element)

    def testPickle(self) -> None:
        """Test _ManifestElement picklability."""
        pickled = pickle.dumps(self.example)
        unpickled = pickle.loads(pickled)
        self.AssertXMLAlmostEqual(repr(unpickled), self.XML)

    def testGetters(self) -> None:
        """Test _ManifestElement.__getattr__."""
        self.assertEqual(self.example.name, "value")
        self.assertIsNone(self.example.other_attr)

    def testGettersInvalidAttr(self) -> None:
        """Test _ManifestElement.__getattr__ with invalid attr."""
        with self.assertRaises(AttributeError):
            _ = self.example.invalid

    def testSetters(self) -> None:
        """Test _ManifestElement.__setattr__."""
        self.example.name = "new"
        self.example.other_attr = "other"
        EXPECTED = '<example name="new" other-attr="other"/>'
        self.AssertXMLAlmostEqual(repr(self.example), EXPECTED)

    def testDel(self) -> None:
        """Test _ManifestElement.__delattr__."""
        del self.example.name
        self.assertIsNone(self.example.name)


class RemoteTest(cros_test_lib.TestCase):
    """Tests for repo_manifest.Remote."""

    def setUp(self) -> None:
        self.manifest = repo_manifest.Manifest.FromString(MANIFEST_XML)
        self.simple = self.manifest.GetRemote("simple_remote")
        self.complex = self.manifest.GetRemote("complex_remote")

    def testGitName(self) -> None:
        self.assertEqual(self.simple.GitName(), "simple_remote")

    def testGitNameAlias(self) -> None:
        self.assertEqual(self.complex.GitName(), "cplx")

    def testPushURL(self) -> None:
        self.assertEqual(self.simple.PushURL(), "http://simple.example.com")
        self.assertEqual(self.complex.PushURL(), "http://example.com/push")


class ProjectTest(cros_test_lib.TestCase):
    """Tests for repo_manifest.Project."""

    def setUp(self) -> None:
        self.manifest = repo_manifest.Manifest.FromString(MANIFEST_XML)
        self.simple = self.manifest.GetUniqueProject("simple/project")
        self.complex = self.manifest.GetUniqueProject("complex/project")

    def testPath(self) -> None:
        """Test Project.Path."""
        self.assertEqual(self.simple.Path(), "simple/project")
        self.assertEqual(self.complex.Path(), "src/complex")

    def testRemoteName(self) -> None:
        """Test Project.RemoteName."""
        self.assertEqual(self.simple.RemoteName(), "simple_remote")
        self.assertEqual(self.complex.RemoteName(), "complex_remote")

    def testRemote(self) -> None:
        """Test Project.Remote."""
        self.assertEqual(self.simple.Remote().name, "simple_remote")

    def testRevision(self) -> None:
        """Test Project.Revision."""
        self.assertIsNone(self.simple.Revision())
        self.assertEqual(self.complex.Revision(), "cafe")

    def testAnnotations(self) -> None:
        """Test Project.Annotations."""
        self.assertEqual(self.simple.Annotations(), {})
        self.assertEqual(self.complex.Annotations(), {"branch-mode": "pin"})
