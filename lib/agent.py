from langchain import LLMChain
from langchain.agents import LLMSingleActionAgent, AgentExecutor, AgentOutputParser
from langchain.chat_models import ChatOpenAI

from lib.custom_output_parser import CustomOutputParser
from lib.prompt_template import prompt
from lib.tool import tools

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]

output_parser = CustomOutputParser()

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)
