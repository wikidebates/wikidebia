"""Pywikibot family for the French and English Wikidebates sites."""

from pywikibot import family


class Family(family.Family):
    """Wikidebates family."""

    name = "wikidebates"
    langs = {
        "fr": "fr.wikidebates.org",
        "en": "en.wikidebates.org",
    }

    def protocol(self, code: str) -> str:
        """Use HTTPS for every Wikidebates site."""
        return "https"

    def scriptpath(self, code: str) -> str:
        """Return the MediaWiki script path used by Wikidebates."""
        return "/w"
