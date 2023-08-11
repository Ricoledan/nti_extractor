from langchain.tools import Tool
from lib.sparqlrunner import run_sparql
from lib.vocab_lookup import vocab_lookup

tools = [
    Tool(
        name="ItemLookup",
        func=(lambda x: vocab_lookup(x, entity_type="item")),
        description="useful for when you need to know the q-number for an item",
    ),
    Tool(
        name="PropertyLookup",
        func=(lambda x: vocab_lookup(x, entity_type="property")),
        description="useful for when you need to know the p-number for a property",
    ),
    Tool(
        name="SparqlQueryRunner",
        func=run_sparql,
        description="useful for getting results from a wikibase",
    ),
]