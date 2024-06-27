import re
import sys
from typing import Type
import json
from genworlds.events.abstracts.event import AbstractEvent, NewsEvent
from genworlds.agents.abstracts.agent_state import AbstractAgentState
from newsagents.agents.custom_agent_state import CustomAgentState
from genworlds.agents.abstracts.thought import AbstractThought

from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from genworlds.utils.logging_factory import LoggingFile

class EventFillerThought(AbstractThought):
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
        #self.llm = Ollama(model=model_name)   # 实例化LLAMA2，提供模型的本地路径
 


    def run(self, trigger_event_class: Type[NewsEvent]):
        entity_schemas_full_string = "## Available Entities: \n\n"
        entity_schemas_full_string = "## Available Entities: \n\n"
        for entity_key, entity_value in self.agent_state.available_entities.items():
            entity_schemas_full_string += (
                "ID: "
                + str(entity_value['id'])  # 确保这里的索引是字符串
                + "\nName: "
                + str(entity_value['name'])  # 确保这里的索引是字符串
                + "\n"
            )

        def set_response_to_trigger_event(response):
            # 使用正则表达式提取 sender_id, target_id 和 news_id，可以匹配没有引号、单引号和双引号三种情况
            sender_id_match = re.search(r"^sender_id:\s*['\"]?([^'\"]+?)['\"]?\s*$", response, re.IGNORECASE | re.MULTILINE)
            target_id_match = re.search(r"^target_id:\s*['\"]?([^'\"]+?)['\"]?\s*$", response, re.IGNORECASE | re.MULTILINE)
            news_id_match = re.search(r"^news_id:\s*['\"]?([^'\"]+?)['\"]?\s*$", response, re.IGNORECASE | re.MULTILINE)
    
            # 如果找到了匹配的结果，提取相应的值；否则，从 self.agent_state 获取默认值
            sender_id = sender_id_match.group(1) if sender_id_match else self.agent_state.id
            target_id = target_id_match.group(1) if target_id_match else self.agent_state.id
            
            # 从 available_entities 中查找第一个 entity_type 为 'OBJECT' 的实体的 id
            news_entity_id = next((entity['id'] for entity in self.agent_state.available_entities.values() if entity['entity_type'] == 'OBJECT'), None)
            
            if news_id_match:
                news_id = news_id_match.group(1)
                if news_id != news_entity_id:
                    news_id = news_entity_id
            else:
                news_id = news_entity_id
    
            if isinstance(self.agent_state.news_content, list):
                news_content = ' '.join(self.agent_state.news_content).strip()
            else:
                news_content = self.agent_state.news_content.strip()

            trigger_event_class_properties = {
                "sender_id": sender_id,
                "target_id": target_id,
                "news_id": news_id,
                "news_content": news_content,
                "comment_content": None
            }
            return trigger_event_class_properties

            
        prompt = ChatPromptTemplate.from_messages(
            [
                (   "system", 
                    "You are {agent_name}. {agent_description}. You need to fill in the required fields from the available entities and their IDs."
                ),
                (
                    "system",
                    "You are embedded in a simulated world with those properties {agent_world_state}",
                ),
                (
                    "system",
                    "These are the entities available in this world and their IDs: \n{available_entities}",
                ),
                (   "system", 
                    "You received the news: \n {news_content}"
                ),
                (
                    "system",
                    "Now you received a trigger event, here is the triggering event schema: \n{triggering_event_schema}",
                ),
                ("human", "{footer}"),
            ]
        )
        # chain = create_structured_output_runnable(
        #     output_schema=trigger_event_class.schema(),
        #     llm=self.llm,
        #     prompt=prompt,
        #     verbose=True,
        # )
        input_context = {
                "agent_name": self.agent_state.name,
                "agent_description": self.agent_state.description,
                "agent_world_state": self.agent_state.host_world_prompt,
                "available_entities": entity_schemas_full_string,
                "news_content": self.agent_state.news_content,
                "triggering_event_schema": trigger_event_class.model_json_schema(),
                "footer": """
                    1. Your answer should contain the following format:
                        sender_id: {Sender's id}
                        target_id: {Target's id}
                        news_id: {News's id}
                    2. Infer from what you know and select the sender id, target id, and news id that triggered the event. These IDs cannot be None and must come from available entities and their IDs.
                    3. For AgentReceivesNewsEvent and  AgentHasUpdatedStateBasedOnNewsEvent, the sender id is the world entity id, and the target id is the agent entity id.
                """
        }
        output_parser = StrOutputParser()
        # chain = trigger_event_class.schema() | self.llm | prompt
        chain = prompt | self.llm | output_parser
        response = chain.invoke(input_context)
        print("responseeeee ", response)
        self.logger.info(f"Required: {response}")
        response = set_response_to_trigger_event(response)
        response = trigger_event_class.model_validate(response)
        return response
