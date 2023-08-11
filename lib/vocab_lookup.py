import os
import requests
import configparser
from typing import Optional

config = configparser.ConfigParser()
config.read("./secrets.ini")

wikidata_user_agent_header = (
    None
    if not config.has_section("WIKIDATA")
    else config["WIKIDATA"]["WIKIDAtA_USER_AGENT_HEADER"]
)

openai_api_key = config["OPENAI"]["OPENAI_API_KEY"]
os.environ.update({"OPENAI_API_KEY": openai_api_key})


def get_nested_value(o: dict, path: list) -> any:
    current = o
    for key in path:
        try:
            current = current[key]
        except:
            return None
    return current


def vocab_lookup(
        search: str,
        entity_type: str = "item",
        url: str = "https://www.wikidata.org/w/api.php",
        user_agent_header: str = wikidata_user_agent_header,
        srqiprofile: str = None,
) -> Optional[str]:
    headers = {"Accept": "application/json"}
    if wikidata_user_agent_header is not None:
        headers["User-Agent"] = wikidata_user_agent_header

    if entity_type == "item":
        srnamespace = 0
        srqiprofile = "classic_noboostlinks" if srqiprofile is None else srqiprofile
    elif entity_type == "property":
        srnamespace = 120
        srqiprofile = "classic" if srqiprofile is None else srqiprofile
    else:
        raise ValueError("entity_type must be either 'property' or 'item'")

    params = {
        "action": "query",
        "list": "search",
        "srsearch": search,
        "srnamespace": srnamespace,
        "srlimit": 1,
        "srqiprofile": srqiprofile,
        "srwhat": "text",
        "format": "json",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        title = get_nested_value(response.json(), ["query", "search", 0, "title"])
        if title is None:
            return f"I couldn't find any {entity_type} for '{search}'. Please rephrase your request and try again"
        # if there is a prefix, strip it off
        return title.split(":")[-1]
    else:
        return "Sorry, I got an error. Please try again."
