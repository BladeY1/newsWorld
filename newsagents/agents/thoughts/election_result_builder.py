import re

from genworlds.agents.abstracts.thought import AbstractThought
from newsagents.agents.custom_agent_state import CustomAgentState
from langchain_openai import ChatOpenAI

from newsagents.agents.custom_state_manager import CustomStateManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from genworlds.utils.logging_factory import LoggingFile

class ElectionResultBuilderThought(AbstractThought):
    def __init__(
        self,
        agent_state: CustomAgentState,
        openai_api_key: str,
        model_name: str = "llama3",
    ):
        self.agent_state = agent_state
        self.model_name = model_name
        self.llm = ChatOpenAI(
            model=self.model_name, openai_api_key=openai_api_key, temperature=0.1
        )
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def run(self, news_content:str):
        # 根据当前agent.id获取代理的上一次选举结果
        def get_election_result(agent_id):
            """
            Fetch the election result for a given agent's ID from the US_2020_election.md document.
            
            Parameters:
            agent_id (str): The agent ID in the format 'StateName-agent'.
            
            Returns:
            str: The election result for the specified state in 2020.
            """
            # Extract state name from agent_id
            state = agent_id.split('-agent')[0]
            
            # Define the path to the markdown file
            file_path = '/home/newsworld/newsagents/docs/US_2020_election.md'
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Create a regex pattern to find the election result for the specified state
                pattern = rf'\*\*{state}:\s*(\w+)\*\*'
                match = re.search(pattern, content)
                
                if match:
                    return match.group(1)
                else:
                    return f"Election result for {state} not found."
            
            except FileNotFoundError:
                return f"File {file_path} not found."

        # 获取代理当前的情感和态度和上一次选举结果
 
        last_election_result = get_election_result(self.agent_state.id)

        def parse_output(output_text):
            """
            Parse the output text to extract the agent name and the selection result.
            
            Parameters:
            output_text (str): The output text containing the agent, selection, and reason.
            
            Returns:
            str: The selection result (Trump/Biden) for the given agent.
            """
            # Create a regex pattern to extract the selection result
            pattern = r'selection:\s*(\w+)'
            match = re.search(pattern, output_text)
            
            if match:
                selection = match.group(1)
                return selection
            else:
                return "Selection result not found in the output text."
                            
            # 构建输入提示
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "You are {agent_name}, {agent_description}\n"
                    "Now you need to complete the human requirements."
                ),
                # (
                #     "system",
                #     "You are situated within a simulated environment characterized by the following properties {agent_world_state}",
                # ),
                (
                    "system", 
                    "The news content you have received is: {news_content}."
                ),
                (
                    "system",
                    "Your current emotion is: {emotions}. \nYour current attitude is: {attitudes}."
                ),
                (
                    "system",
                    "Your last election results is: {last_election_result}. \n"
                ),
                ("human", "{footer}"),
            ]
        )
        input_context = {
            "agent_name": self.agent_state.name,
            "agent_description": self.agent_state.description,
            # "agent_world_state": self.agent_state.host_world_prompt,
            "news_content": news_content,
            "emotions": self.agent_state.emotion,
            "attitudes": self.agent_state.attitude,
            "last_election_result": last_election_result,
            "footer": """"
            1. Based on the news content, your current emotions and attitudes, and last election result in 2020, predict the outcome of the 2024 US election for the state you represent;
            2. Ensure all responses adhere to this template, Choose one of (Trump/Biden) based on the contextual input.
            3. Your responses must follow this template:
                selection: {(Trump/Biden)}
                reason: {reason}
            """
        }
        # chain = create_structured_output_runnable(
        #     output_schema=trigger_event_class.schema(),
        #     llm=self.llm,
        #     prompt=prompt,
        #     verbose=True,
        # )
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        response = chain.invoke(input_context)
        print("election res: ", response)
        response = parse_output(response)
        print(f"Selection result: {response}")
        return response