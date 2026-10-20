from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

spec = spec_from_file_location("render_publication", Path(__file__).resolve().parents[1] / "render-publication-service.py")
service = module_from_spec(spec)
spec.loader.exec_module(service)


class PublicationServiceTests(unittest.TestCase):
    def test_service_executes_only_the_explicit_publication_relay(self):
        root = "/home/users/webmaster/files/Wikidéb'IA"
        rendered = service.render(root)
        self.assertIn('"'+root+'/wikidebia" fr-publication-relay --execute', rendered)
        self.assertIn("WorkingDirectory="+root+"/.", rendered)
        self.assertNotIn("update.sh", rendered)

    def test_unit_injection_is_rejected(self):
        with self.assertRaises(ValueError):
            service.render("/home/test\nUser=root")

    def test_shell_and_systemd_metacharacters_remain_literal(self):
        rendered = service.render('/home/test/a space/%h/$HOME/"quoted"')
        self.assertIn('%%h/$$HOME/\\"quoted\\"/wikidebia', rendered)
