import json
import re

import sys
from time import sleep
from typing import List, Optional
from genworlds.agents.abstracts.thought import AbstractThought
from newsagents.agents.custom_agent_state import CustomAgentState, PopulationCategory
from langchain_openai import ChatOpenAI

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
#from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.structured_output import (
    create_structured_output_runnable
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.messages import AIMessage
from genworlds.utils.logging_factory import LoggingFile

class EmotionAttitudeBuilderThought(AbstractThought):
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
        class EmotionAttitudeResult(BaseModel):
            """Result containing the generated emotion and attitude."""

            emotions: dict = Field(
                ...,
                description="The generated emotion based on the news content and agent state.",
            )
            attitudes: dict = Field(
                ...,
                description="The generated attitude based on the news content and agent state.",
            )
        # 检查代理当前的情感和态度
        population_category = self.agent_state.population_category
        # 根据不同人群类别设置情感和态度波动范围
        category_description = population_category.get_description()

        def parse_output(output_text):
            # Define keywords
            emotions_keywords = ["happiness", "sadness", "anger"]
            attitudes_keywords = ["optimism", "pessimism", "neutrality"]
            
            emotions = {}
            attitudes = {}

            # Function to extract key-value pairs from a given section
            def extract_values(section):
                values = {}
                pairs = section.split(',')
                for pair in pairs:
                    key, value = pair.split(':')
                    key = key.strip().strip("'\"")
                    value = value.strip()
                    values[key] = float(value)
                return values

            # Find and extract emotions
            emotions_section = re.search(r"emotions:\s*\{([^}]*)\}", output_text, re.IGNORECASE)
            if emotions_section:
                emotions = extract_values(emotions_section.group(1))

            # Find and extract attitudes
            attitudes_section = re.search(r"attitudes:\s*\{([^}]*)\}", output_text, re.IGNORECASE)
            if attitudes_section:
                attitudes = extract_values(attitudes_section.group(1))

            return {"emotions": emotions, "attitudes": attitudes}
                            
            # 构建输入提示
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "You are {agent_name}, {agent_description}\n"
                    "Now you need to update your emotions and attitude."
                ),
                (
                    "system",
                    "You are situated within a simulated environment characterized by the following properties {agent_world_state}",
                ),
                (
                    "system",
                    "Considering your population category: {population_category}, individuals exhibit the following characteristics: {category_description}"
                ),
                (
                    "system", 
                    "The news content you have received is: {news_content}."
                ),
                (
                    "system",
                    "Your current emotion is: {emotions}. \nYour current attitude is: {attitudes}."
                ),
                ("human", "{footer}"),
            ]
        ).partial(schema=EmotionAttitudeResult.model_json_schema())

        input_context = {
            "agent_name": self.agent_state.name,
            "agent_description": self.agent_state.description,
            "agent_world_state": self.agent_state.host_world_prompt,
            "population_category": self.agent_state.population_category,
            "category_description": category_description,
            "news_content": news_content,
            "emotions": self.agent_state.emotion,
            "attitudes": self.agent_state.attitude,
            "footer": """"
            1. Based on the news content, your current emotions and attitudes, attribute category, and category description, update your new emotions and attitudes to complete the template;
            2. Your responses must follow this template:

                emotions: {'happiness': (), 'sadness': (), 'anger': ()}
                attitudes: {'optimism': (), 'pessimism': (), 'neutrality': ()}
                reason: {reason}
            3. Ensure all responses adhere to this template, filling in the () fields based on the contextual input.
            """
        }
        #          3. Simulate human reactions to news and reflect changes in various emotions and attitudes. Emotions must include happiness, sadness, and anger, and attitudes must include optimism, pessimism, and neutrality;

        # chain = create_structured_output_runnable(
        #     output_schema=trigger_event_class.schema(),
        #     llm=self.llm,
        #     prompt=prompt,
        #     verbose=True,
        # )
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        response = chain.invoke(input_context)
        print("emotion: ", response)
        response = parse_output(response)
        response = EmotionAttitudeResult.model_validate(response)
        print("emotion: ", response)
        self.logger.info(f"Emotion: {response}")
        return response.emotions, response.attitudes