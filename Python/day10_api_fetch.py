"""Day 10 — APIs with requests: first contact with PokeAPI."""
#%%
import requests
import pandas as pd


URL = "https://pokeapi.co/api/v2/pokemon"

response = requests.get(URL, params={"limit": 5, "offset": 0}, timeout=10)
response.raise_for_status()
data = response.json()


print("=== response status ===")
print(response.status_code)

print("\n=== response headers (selected) ===")
for k in ("Content-Type", "Date", "Server"):
    print(f"  {k}: {response.headers.get(k)}")

print("\n=== top-level keys of body ===")
print(list(data.keys()))

print("\n=== count, next, previous ===")
print(f"count    = {data['count']}")
print(f"next     = {data['next']}")
print(f"previous = {data['previous']}")

print("\n=== results ===")
for item in data["results"]:
    print(item)

print("\n=== as DataFrame ===")
df = pd.DataFrame(data["results"])
print(df)



# %%
"""Day 10 — APIs with requests: Session, headers, error handling."""

import logging
import requests
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


BASE_URL = "https://pokeapi.co/api/v2"


def build_session() -> requests.Session:
    """Construct a Session with sensible defaults for this client."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "de-roadmap-learn/1.0",
        "Accept": "application/json",
    })
    return s


def fetch_json(session: requests.Session, url: str, *, params: dict | None = None, timeout: int = 10) -> dict:
    """GET a URL and return parsed JSON, with proper error handling."""
    logger.info("GET %s params=%s", url, params)
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def main() -> None:
    session = build_session()

    # Happy path
    data = fetch_json(session, f"{BASE_URL}/pokemon", params={"limit": 5, "offset": 0})
    df = pd.DataFrame(data["results"])
    print("\n=== happy path ===")
    print(df)

    # 404 path — fetch a Pokémon that doesn't exist; expect HTTPError
    print("\n=== 404 path ===")
    try:
        fetch_json(session, f"{BASE_URL}/pokemon/notarealpokemon")
    except requests.exceptions.HTTPError as e:
        logger.warning("Caught HTTPError: status=%s url=%s", e.response.status_code, e.response.url)

    # Single-detail fetch — different shape: NOT paginated, single dict
    print("\n=== single-detail fetch (bulbasaur) ===")
    detail = fetch_json(session, f"{BASE_URL}/pokemon/bulbasaur")
    print(f"name:    {detail['name']}")
    print(f"height:  {detail['height']}")
    print(f"weight:  {detail['weight']}")
    print(f"types:   {[t['type']['name'] for t in detail['types']]}")
    print(f"# stats: {len(detail['stats'])}")


if __name__ == "__main__":
    main()



# %%
import logging
import requests
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


BASE_URL = "https://pokeapi.co/api/v2"


def build_session() -> requests.Session:
    """Construct a Session with sensible defaults for this client."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "de-roadmap-learn/1.0",
        "Accept": "application/json",
    })
    return s


def fetch_json(session: requests.Session, url: str, *, params: dict | None = None, timeout: int = 10) -> dict:
    """GET a URL and return parsed JSON, with proper error handling."""
    logger.info("GET %s params=%s", url, params)
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_all_paginated(session: requests.Session, start_url: str) -> list[dict]:
    """Follow `next` links until exhausted; return list of all results."""
    all_results: list[dict] = []
    url: str | None = start_url
    page_num = 0
    expected_count: int | None = None

    while url is not None:
        page_num += 1
        data = fetch_json(session, url)
        if expected_count is None:
            expected_count = data["count"]
        all_results.extend(data["results"])
        logger.info(
            "Page %d: fetched %d (total so far: %d / expected %d)",
            page_num, len(data["results"]), len(all_results), expected_count,
        )
        url = data.get("next")

    if expected_count is not None and len(all_results) != expected_count:
        logger.warning(
            "Pagination count mismatch: got %d, expected %d",
            len(all_results), expected_count,
        )

    return all_results


# Add to main() — REPLACE the happy-path block; keep 404 and detail blocks:
def main() -> None:
    session = build_session()

    print("\n=== paginated fetch — ALL Pokémon ===")
    start_url = f"{BASE_URL}/pokemon?limit=20"           # 20 per page → ~68 pages
    all_pokemon = fetch_all_paginated(session, start_url)
    df = pd.DataFrame(all_pokemon)
    logger.info("Fetched %d total records", len(df))
    print(df.head())
    print(f"...")
    print(df.tail())

    # 404 path — fetch a Pokémon that doesn't exist; expect HTTPError
    print("\n=== 404 path ===")
    try:
        fetch_json(session, f"{BASE_URL}/pokemon/notarealpokemon")
    except requests.exceptions.HTTPError as e:
        logger.warning("Caught HTTPError: status=%s url=%s", e.response.status_code, e.response.url)


if __name__ == "__main__":
    main()

# %%
import logging
import requests
import pandas as pd
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


BASE_URL = "https://pokeapi.co/api/v2"


def build_session() -> requests.Session:
    """Construct a Session with default headers and a retry adapter."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "de-roadmap-learn/1.0",
        "Accept": "application/json",
    })

    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        backoff_factor=1.0,
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s.mount("https://", adapter)
    s.mount("http://", adapter)

    return s


def fetch_json(session: requests.Session, url: str, *, params: dict | None = None, timeout: int = 10) -> dict:
    """GET a URL and return parsed JSON, with proper error handling."""
    logger.info("GET %s params=%s", url, params)
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_all_paginated(session: requests.Session, start_url: str) -> list[dict]:
    """Follow `next` links until exhausted; return list of all results."""
    all_results: list[dict] = []
    url: str | None = start_url
    page_num = 0
    expected_count: int | None = None

    while url is not None:
        page_num += 1
        data = fetch_json(session, url)
        if expected_count is None:
            expected_count = data["count"]
        all_results.extend(data["results"])
        logger.info(
            "Page %d: fetched %d (total so far: %d / expected %d)",
            page_num, len(data["results"]), len(all_results), expected_count,
        )
        url = data.get("next")

    if expected_count is not None and len(all_results) != expected_count:
        logger.warning(
            "Pagination count mismatch: got %d, expected %d",
            len(all_results), expected_count,
        )

    return all_results

def fetch_pokemon_details(session: requests.Session, names: list[str]) -> pd.DataFrame:
    """Fan-out: fetch detail records for a list of Pokémon names."""
    records = []
    for name in names:
        detail = fetch_json(session, f"{BASE_URL}/pokemon/{name}")
        records.append({
            "name":   detail["name"],
            "id":     detail["id"],
            "height": detail["height"],
            "weight": detail["weight"],
            "types":  ", ".join(t["type"]["name"] for t in detail["types"]),
            "base_xp": detail["base_experience"],
        })
    return pd.DataFrame(records)


def main() -> None:
    session = build_session()

    # Paginated fetch (Block 3 work)
    print("\n=== paginated fetch — first 100 Pokémon ===")
    start_url = f"{BASE_URL}/pokemon?limit=20"
    all_pokemon = fetch_all_paginated(session, start_url)
    list_df = pd.DataFrame(all_pokemon)

    # Fan-out: detail records for the first 10
    print("\n=== fan-out — details for first 10 ===")
    first_10_names = list_df["name"].head(10).tolist()
    details = fetch_pokemon_details(session, first_10_names)
    print(details)

    # 404 path (Block 2 work — keep this)
    print("\n=== 404 path ===")
    try:
        fetch_json(session, f"{BASE_URL}/pokemon/notarealpokemon")
    except requests.exceptions.HTTPError as e:
        logger.warning("Caught HTTPError: status=%s url=%s", e.response.status_code, e.response.url)


if __name__ == "__main__":
    main()
# %%
