import os
import urllib.request
import urllib.parse
import json
import base64
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

LSM_API_URL = "https://api.lsm.org/recver/txo.php"
APP_NAME = "com.bibletrivia.1"
TOKEN = "web_c7554d1d-b36c-4e28-a9ab-7eceb4884217"
DEFAULT_COPYRIGHT = "Verses accessed from the Holy Bible Recovery Version (text-only edition) © Living Stream Ministry www.lsm.org"

# Check if user has credentials configured in ~/.lsm-verse.json
try:
    _cfg_path = os.path.expanduser("~/.lsm-verse.json")
    if os.path.exists(_cfg_path):
        with open(_cfg_path, "r", encoding="utf-8") as _f:
            _cfg = json.load(_f)
            if _cfg.get("appid") and _cfg.get("token"):
                APP_NAME = _cfg["appid"].strip()
                TOKEN = _cfg["token"].strip()
except Exception:
    pass

# In-memory verse cache
_VERSE_CACHE: Dict[str, Dict[str, Any]] = {}

def fetch_bible_verses(verse_ref: str, timeout: float = 3.5) -> Dict[str, Any]:
    """
    Fetches verse text from the Living Stream Ministry Recovery Version API.
    Returns a dict with 'ref', 'text', 'copyright', 'url', and 'source'.
    Falls back gracefully if offline or API is unavailable.
    """
    if not verse_ref or not verse_ref.strip():
        return {
            "ref": "",
            "text": "",
            "copyright": DEFAULT_COPYRIGHT,
            "url": "https://text.recoveryversion.bible"
        }

    clean_ref = verse_ref.strip()
    if clean_ref in _VERSE_CACHE:
        return _VERSE_CACHE[clean_ref]

    params = {
        "String": clean_ref,
        "Out": "json"
    }
    url = f"{LSM_API_URL}?{urllib.parse.urlencode(params)}"

    auth_str = f"{APP_NAME}:{TOKEN}"
    b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Accept": "application/json",
        "User-Agent": "BibleTriviaPartyGame/1.0"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                verses = data.get("verses", [])
                copyright_notice = data.get("copyright") or DEFAULT_COPYRIGHT
                
                if verses:
                    combined_text = " ".join(v.get("text", "") for v in verses).strip()
                    first_ref = verses[0].get("ref", clean_ref)
                    url_pfx = verses[0].get("urlpfx", "")
                    web_url = f"https://text.recoveryversion.bible/{url_pfx}" if url_pfx else "https://text.recoveryversion.bible"
                    
                    result = {
                        "ref": first_ref if len(verses) == 1 else clean_ref,
                        "text": combined_text,
                        "copyright": copyright_notice,
                        "url": web_url,
                        "source": "lsm_api"
                    }
                    _VERSE_CACHE[clean_ref] = result
                    return result

    except Exception as e:
        logger.debug("LSM API fetch fallback for '%s': %s", clean_ref, e)

    # Fallback structure preserving scripture reference and copyright
    fallback = {
        "ref": clean_ref,
        "text": "",
        "copyright": DEFAULT_COPYRIGHT,
        "url": "https://text.recoveryversion.bible",
        "source": "reference_only"
    }
    _VERSE_CACHE[clean_ref] = fallback
    return fallback
