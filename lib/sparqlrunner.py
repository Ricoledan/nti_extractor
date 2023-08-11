import requests
import configparser
import json
from typing import List, Dict, Any

from lib.vocab_lookup import get_nested_value

config = configparser.ConfigParser()
config.read("./secrets.ini")

wikidata_user_agent_header = (
    None
    if not config.has_section("WIKIDATA")
    else config["WIKIDATA"]["WIKIDAtA_USER_AGENT_HEADER"]
)


def run_sparql(
        query: str,
        url="https://query.wikidata.org/sparql",
        user_agent_header: str = wikidata_user_agent_header,
) -> List[Dict[str, Any]]:
    headers = {"Accept": "application/json"}
    if wikidata_user_agent_header is not None:
        headers["User-Agent"] = wikidata_user_agent_header

    response = requests.get(
        url, headers=headers, params={"query": query, "format": "json"}
    )

    if response.status_code != 200:
        return "That query failed. Perhaps you could try a different one?"
    results = get_nested_value(response.json(), ["results", "bindings"])
    return json.dumps(results)
