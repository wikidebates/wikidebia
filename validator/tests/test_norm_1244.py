import hashlib

from wikidebia_validator.editorial import _validate_intro_references
from wikidebia_validator.report import Report


class Context:
    def __init__(self, body: str, exceptions=None):
        self.page = "{{Débat\n|sujet=Dieu\n|sujet-complet=l’existence de Dieu\n|introduction={{Sous-partie\n|titre=Définition\n|contenu=Fait documenté<ref>" + body + "</ref>.\n}}\n|articles-Wikipédia={{Article Wikipédia|page=Dieu}}\n|arguments-pour=\n|arguments-contre=\n|rubriques=Philosophie\n|mots-clés=Dieu\n|date-création=2026-08-04\n}}\n"
        self.review = {"entries": [{"language": "fr", "reference_note_punctuation_reviewed": True, "terminal_period_sentence_exceptions": exceptions or []}]}
        self.report = Report("0.4.48", "test-fixture-1244", ["editorial"])
    def manifest(self):
        return {"normative_versions": {"consolidated_norm": "1.2.30"}, "pages": [{"page_type": "debate", "language": "fr", "file_path": "output/fr/debate.wiki"}]}
    def exists(self, rel): return rel in {"output/fr/debate.wiki", "reviews/introduction_review.json"}
    def read_text(self, rel): return self.page
    def load_json(self, rel): return self.review


def controls():
    return {"introduction_references": {"required": True, "punctuation_policy_revision": "1.2.44"}, "introduction_review_path": "reviews/introduction_review.json", "inline_reference_punctuation_policy_revision": "1.2.44"}


def test_simple_reference_notice_must_not_end_with_period():
    ctx = Context("Jean Dupont, « Titre », ''Revue'', 2012.")
    metrics = _validate_intro_references(ctx, ctx.manifest(), controls())
    assert metrics["fr"]["terminal_period_reference_notes"]
    assert any(item.code == "WDV-DOC-008" for item in ctx.report.findings)


def test_simple_reference_notice_without_period_is_valid():
    ctx = Context("Jean Dupont, « Titre », ''Revue'', 2012")
    metrics = _validate_intro_references(ctx, ctx.manifest(), controls())
    assert metrics["fr"]["terminal_period_reference_notes"] == []
    assert not any(item.code == "WDV-DOC-008" for item in ctx.report.findings)


def test_complete_sentence_period_requires_matching_attestation():
    body = "Cette étude expose en détail la méthode employée."
    exception = {"body_sha256": hashlib.sha256(body.encode()).hexdigest(), "complete_sentence": True, "sentence_evidence": "expose en détail la méthode"}
    ctx = Context(body, [exception])
    metrics = _validate_intro_references(ctx, ctx.manifest(), controls())
    assert metrics["fr"]["terminal_period_reference_notes"] == []
    assert not any(item.code == "WDV-DOC-008" for item in ctx.report.findings)
