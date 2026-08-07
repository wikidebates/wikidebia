from pathlib import Path
import json

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def _set_1252(root: Path, *, with_review: bool = True, first_outcome: str = "known_name"):
    create_fr_package(root)
    manifest = json.loads((root / "manifest.json").read_text())
    manifest.setdefault("normative_versions", {})["consolidated_norm"] = "1.2.52"
    if with_review:
        controls = manifest.setdefault("editorial_controls", {})
        controls["argument_name_discovery_revision"] = "1.2.52"
        controls["argument_name_discovery_path"] = "reviews/argument_name_discovery_review.json"
        (root / "reviews").mkdir(exist_ok=True)
        entries = []
        for page in manifest["pages"]:
            if page["page_type"] != "argument":
                continue
            known = page["page_id"] == "A0001" and first_outcome == "known_name"
            entries.append({
                "language": "fr",
                "page_id": page["page_id"],
                "title": page["canonical_title"],
                "page_origin": "new",
                "search_reviewed": True,
                "search_queries": [
                    f'"{page["canonical_title"]}" argument',
                    f'{page["canonical_title"]} conventional name literature',
                ],
                "search_scope_note": "Recherche française et terminologie académique internationale vérifiées.",
                "outcome": "known_name" if known else "none",
                "name": "Argument du bénéfice collectif" if known else None,
                "evidence": ([{
                    "source": "Ouvrage académique de référence",
                    "label_as_used": "Argument du bénéfice collectif",
                    "locator": "chapitre 2",
                    "url": None,
                }] if known else []),
                "same_reasoning_confirmed": bool(known),
                "non_invented_label_confirmed": True,
                "language_fit_confirmed": True,
                "rationale": "L'appellation est attestée pour le même raisonnement." if known else "Aucune appellation conventionnelle suffisamment attestée n’a été trouvée.",
            })
        dump(root / "reviews/argument_name_discovery_review.json", {
            "version": "wikidebia-argument-name-discovery-review-1.0",
            "normative_revision": "1.2.52",
            "debate_id": manifest["debate_id"],
            "entries": entries,
        })
    dump(root / "manifest.json", manifest)
    return manifest


def test_1252_requires_name_search_for_every_new_argument(tmp_path: Path):
    _set_1252(tmp_path, with_review=False)
    report = validate_package(tmp_path, scopes=["coherence"])
    assert any(f.code == "WDV-EDT-032" and "recherche" in f.message.lower() for f in report.findings)


def test_1252_known_name_is_allowed_when_attested(tmp_path: Path):
    manifest = _set_1252(tmp_path)
    page = next(p for p in manifest["pages"] if p["page_id"] == "A0001")
    path = tmp_path / page["file_path"]
    path.write_text(path.read_text().replace("{{Argument\n", "{{Argument\n|nom=Argument du bénéfice collectif\n", 1))
    report = validate_package(tmp_path, scopes=["coherence", "wikicode"])
    assert not any(f.code == "WDV-EDT-032" for f in report.findings)
    assert not any(f.code == "WDV-MWK-003" and f.path == page["file_path"] and "nom" in f.message.lower() for f in report.findings)


def test_1252_none_outcome_forbids_rendered_name(tmp_path: Path):
    manifest = _set_1252(tmp_path, first_outcome="none")
    page = next(p for p in manifest["pages"] if p["page_id"] == "A0001")
    path = tmp_path / page["file_path"]
    path.write_text(path.read_text().replace("{{Argument\n", "{{Argument\n|nom=Nom inventé\n", 1))
    report = validate_package(tmp_path, scopes=["coherence", "wikicode"])
    assert any(f.code in {"WDV-EDT-032", "WDV-MWK-003"} and "nom" in f.message.lower() for f in report.findings)
