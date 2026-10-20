"""Scénarios Git réels ; Python/pip et les tests applicatifs sont simulés.

Aucun réseau ni service systemd n'est utilisé par ces tests.
"""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "update.sh"


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source"
        self.repo = self.root / "Wikidéb'IA"
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-b", "main", str(self.source))
        self.git("-C", str(self.source), "config", "user.email", "deploy@example.invalid")
        self.git("-C", str(self.source), "config", "user.name", "Deployment test")
        (self.source / ".gitignore").write_text(".venv/\n.state/\nprivate/\ncorpus/\n")
        (self.source / "requirements-runtime.txt").write_text("")
        (self.source / "wikidebia").write_text(
            '#!/bin/bash\n[[ ! -e "$(dirname "$0")/fail-doctor" ]]\n'
        )
        (self.source / "wikidebia").chmod(0o700)
        (self.source / "version").write_text("1")
        self.commit("initial")
        self.git("clone", str(self.source), str(self.repo))
        self.initial = self.head()
        (self.repo / "private/pywikibot").mkdir(parents=True)
        (self.repo / "private/pywikibot/user-config.py").write_text("secret sentinel")
        (self.repo / "corpus").mkdir()
        (self.repo / "corpus/example").write_text("corpus sentinel")
        # Le faux interpréteur crée un venv sans télécharger de dépendances.
        # Il rejette les tests lorsqu'un commit contient fail-validation.
        self.python = self.root / "python-fixture"
        self.python.write_text(
            '#!/bin/bash\nset -eu\n'
            'if [[ "${1:-}" == -m && "${2:-}" == venv ]]; then\n'
            '  mkdir -p "$3/bin"\n'
            '  cp "$0" "$3/bin/python"\n'
            'elif [[ "${1:-}" == -m && "${2:-}" == pytest ]]; then\n'
            '  [[ ! -e fail-validation ]]\n'
            'fi\n'
        )
        self.python.chmod(0o700)
        self.env["DEPLOY_PYTHON"] = str(self.python)
        if os.geteuid() == 0:
            # Permettre les tests sur un runner root sans changer le script livré.
            bin_dir = self.root / "bin"
            bin_dir.mkdir()
            (bin_dir / "id").write_text("#!/bin/sh\necho 1000\n")
            (bin_dir / "id").chmod(0o700)
            self.env["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], env=self.env, stderr=subprocess.DEVNULL, text=True
        ).strip()

    def commit(self, message):
        self.git("-C", str(self.source), "add", ".")
        self.git("-C", str(self.source), "commit", "-m", message)
        return self.git("-C", str(self.source), "rev-parse", "HEAD")

    def head(self):
        return self.git("-C", str(self.repo), "rev-parse", "HEAD")

    def update(self):
        return subprocess.run(
            ["bash", str(SCRIPT), str(self.repo)], env=self.env,
            capture_output=True, text=True,
        )

    def test_success_preserves_private_data_and_second_run_is_noop(self):
        (self.source / "version").write_text("2")
        target = self.commit("new version")
        result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.head(), target)
        self.assertEqual((self.repo / ".state/deployed-commit").read_text().strip(), target)
        self.assertEqual((self.repo / "private/pywikibot/user-config.py").read_text(), "secret sentinel")
        self.assertEqual((self.repo / "corpus/example").read_text(), "corpus sentinel")
        # Si le deuxième passage relançait pip/tests, cet interpréteur échouerait.
        self.python.write_text("#!/bin/sh\nexit 99\n")
        self.assertEqual(self.update().returncode, 0)

    def test_failed_validation_keeps_installed_commit(self):
        (self.source / "fail-validation").touch()
        self.commit("invalid version")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.head(), self.initial)
        self.assertFalse((self.repo / ".state/deployed-commit").exists())

    def test_local_changes_are_preserved(self):
        (self.repo / "version").write_text("local edit")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual((self.repo / "version").read_text(), "local edit")
        self.assertEqual(self.head(), self.initial)

    def test_untracked_files_block_update(self):
        (self.repo / "untracked").write_text("keep me")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual((self.repo / "untracked").read_text(), "keep me")

    def test_local_commit_is_not_reset(self):
        self.git("-C", str(self.repo), "-c", "user.email=local@example.invalid",
                 "-c", "user.name=Local", "commit", "--allow-empty", "-m", "local")
        local = self.head()
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.head(), local)

    def test_remote_cannot_replace_private_data(self):
        (self.source / "private").mkdir()
        (self.source / "private/new-file").touch()
        self.git("-C", str(self.source), "add", "-f", "private/new-file")
        self.commit("forbidden private path")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.head(), self.initial)

    def test_doctor_failure_does_not_mark_success(self):
        (self.source / "fail-doctor").touch()
        target = self.commit("doctor failure")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.head(), target)  # Limite documentée : pas de rollback.
        self.assertFalse((self.repo / ".state/deployed-commit").exists())

    def test_wrong_branch_is_rejected(self):
        self.git("-C", str(self.repo), "checkout", "-b", "other")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.head(), self.initial)

    def test_concurrent_update_is_skipped(self):
        import fcntl
        with (self.repo / ".git/wikidebia-deploy.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("déploiement est déjà en cours", result.stdout)
        self.assertFalse((self.repo / ".state/deployed-commit").exists())


if __name__ == "__main__":
    unittest.main()
