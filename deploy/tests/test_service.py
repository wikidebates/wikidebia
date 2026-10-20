from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest


spec = spec_from_file_location("render_service", Path(__file__).resolve().parents[1] / "render-service.py")
service = module_from_spec(spec)
spec.loader.exec_module(service)


class ServiceTests(unittest.TestCase):
    def test_server_path_with_apostrophe_and_accent(self):
        repo = "/home/users/webmaster/files/Wikidéb'IA"
        unit = service.render(repo, "main")
        self.assertIn(f'WorkingDirectory={repo}/.', unit)
        self.assertIn(f'"{repo}" "main"', unit)

    def test_special_characters_remain_literal(self):
        repo = '/home/test/a space/%h/$HOME/"quoted"/back\\slash'
        unit = service.render(repo, "main")
        self.assertIn('WorkingDirectory=/home/test/a space/%%h/$HOME/"quoted"/back\\slash/.', unit)
        self.assertIn('"/home/test/a space/%%h/$$HOME/\\"quoted\\"/back\\\\slash" "main"', unit)

    def test_control_characters_cannot_inject_unit_settings(self):
        with self.assertRaises(ValueError):
            service.render("/home/test\nUser=root", "main")

    def test_relative_path_is_rejected(self):
        with self.assertRaises(ValueError):
            service.render("relative/path", "main")
