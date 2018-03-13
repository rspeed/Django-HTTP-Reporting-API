import re
from pkg_resources import parse_version

from django.test import TestCase
from django.core.checks import Warning

import lookout



class TestVersion (TestCase):
	def test_known (self):
		self.assertNotEqual(None, lookout.__version__)
		self.assertNotEqual('unknown', lookout.__version__)


	@staticmethod
	def __valid_version (version) -> bool:
		"""
		Ensure that the version number is valid.

		1. Parse the version.
		2. Extract the base version (which removes pre-release cruft).
		3. Make sure it consists of only numbers and dots.
		"""
		try:
			version_parsed = parse_version(version)
		except TypeError:
			return False
		else:
			return bool(re.fullmatch(r'[\d.]+', version_parsed.base_version))


	def test_valid (self):
		""" Checks the value of ``lookout.__version__``. """
		self.assertTrue(self.__valid_version(lookout.__version__))


	def test_from_file (self):
		"""
		Checks the value returned by ``lookout.PackageVersion.from_file``.
		This test will fail if there isn't a VERSION.txt file in the ``lookout`` package directory.
		"""
		version = lookout.PackageVersion.from_file()
		self.assertTrue(self.__valid_version(version), "Didn't get a valid version identifier from `PackageVersion.from_file`.")


	def test_from_distribution (self):
		"""
		Checks the value returned by ``lookout.PackageVersion.from_distribution``.
		This test will fail if the package isn't installed.
		"""
		version = lookout.PackageVersion.from_distribution()
		self.assertTrue(self.__valid_version(version), "Didn't get a valid version identifier from `PackageVersion.from_distribution`.")



class TestConfigWarnings (TestCase):
	""" Ensures that ``DjangoLookoutConfig`` is informing Django about configuration issues. """
	def test_warnings (self):
		app = apps.get_containing_app_config(type(self).__module__)

		expected_warnings = [
			Warning(
				"'INVALID_TEST_KEY' is not a valid setting name for Django Lookout.",
				hint="The key must be all-caps and have an equivalent default setting.",
				obj=app
			),
			Warning(
				"'invalid_key_test' is not a valid setting name for Django Lookout.",
				hint="The key must be all-caps and have an equivalent default setting.",
				obj=app
			)
		]
		self.assertEqual(app.checks, expected_warnings)
