import re
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain import PromptTemplate, LLMChain
from models.custom_search import DeepSearch
from langchain.agents import BaseSingleActionAgent, AgentOutputParser, LLMSingleActionAgent, AgentExecutor
from typing import List, Tuple, Any, Union, Optional, Type
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import StringPromptTemplate
from langchain.callbacks.manager import CallbackManagerForToolRun
from models.custom_llm import CustomLLM


agent_template = """
You are a {role} now. There is some known information: 
{related_content}
{background_infomation}
{question_guide}: {input}

{answer_format}
"""

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        # 没有互联网查询信息
        if len(intermediate_steps) == 0:
            background_infomation = "\n"
            role = "Naive robit"
            question_guide = "I have a question: "
            answer_format = "If you know the answer, please give your answer! If you don't know the answer, just answer \"DeepSearch('search word')\", and replace 'search word' with the keyword you think you need to search for, and don't answer anything else. \n\nPlease answer the questions I raised above!"

        # 返回了背景信息
        else:
            # 根据 intermediate_steps 中的 AgentAction 拼装 background_infomation
            background_infomation = "\n\nYou also have this known information for reference: \n\n"
            action, observation = intermediate_steps[0]
            background_infomation += f"{observation}\n"
            role = "smart AI Assistant"
            question_guide = "Please answer my questions based on the known information"
            answer_format = ""

        kwargs["background_infomation"] = background_infomation
        kwargs["role"] = role
        kwargs["question_guide"] = question_guide
        kwargs["answer_format"] = answer_format
        return self.template.format(**kwargs)

class CustomSearchTool(BaseTool):
    name: str = "DeepSearch"
    description: str = ""

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        return DeepSearch.search(query = query)

    async def _arun(self, query: str):
        raise NotImplementedError("DeepSearch does not support async")

class CustomAgent(BaseSingleActionAgent):
    @property
    def input_keys(self):
        return ["input"]

    def plan(self, intermedate_steps: List[Tuple[AgentAction, str]],
            **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        return AgentAction(tool="DeepSearch", tool_input=kwargs["input"], log="")

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # group1 = 调用函数名字
        # group2 = 传入参数
        match = re.match(r'^[\s\w]*(DeepSearch)\(([^\)]+)\)', llm_output, re.DOTALL)

        # 如果 llm 没有返回 DeepSearch() 则认为直接结束指令
        if not match:
            return AgentFinish(
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )
        # 否则的话都认为需要调用 Tool
        else:
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


class DeepAgent:
    tool_name: str = "DeepSearch"
    agent_executor: any
    tools: List[Tool]
    llm_chain: any

    def query(self, related_content: str = "", query: str = ""):
        tool_name = self.tool_name
        result = self.agent_executor.run(related_content=related_content, input=query ,tool_name=self.tool_name)
        return result

    def __init__(self, **kwargs):
        llm = CustomLLM()
        tools = [
                    Tool.from_function(
                        func=DeepSearch.search,
                        name="DeepSearch",
                        description="")
                ]
        self.tools = tools
        tool_names = [tool.name for tool in tools]
        output_parser = CustomOutputParser()
        prompt = CustomPromptTemplate(template=agent_template,
                                      tools=tools,
                                      input_variables=["related_content","tool_name", "input", "intermediate_steps"])

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        self.llm_chain = llm_chain

        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
        self.agent_executor = agent_executor


if __name__ == "__main__":
    from custom_llm import CustomLLM

    llm = CustomLLM()
    tools = [
                Tool.from_function(
                    func=DeepSearch.search,
                    name="DeepSearch",
                    description=""
                )
            ]
    tool_names = [tool.name for tool in tools]
    output_parser = CustomOutputParser()
    prompt = CustomPromptTemplate(template=agent_template,
                                  tools=tools,
                                  input_variables=["related_content","tool_name", "input", "intermediate_steps"])

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
    print(agent_executor.run(related_content="", input="Elon Musk news", tool_name="DeepSearch"))

