import json
import re

import sys
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
            keywords = ["Happiness", "Sadness", "Anger", "Optimism", "Pessimism", "Neutrality"]
            emotions = {}
            attitudes = {}

            # Iterate through keywords
            for keyword in keywords:
                # Find keyword's position
                start_index = output_text.find(keyword)
                if start_index != -1:
                    # Extract four characters after the keyword
                    value_str = output_text[start_index + len(keyword) + 2:start_index + len(keyword) + 6]
                    # Remove non-numeric and non-decimal characters
                    value = ''.join(char for char in value_str if char.isdigit() or char == '.')
                    # Convert to float
                    value = float(value)
                    # Determine if emotion or attitude
                    if keyword in ["Happiness", "Sadness", "Anger"]:
                        emotions[keyword.lower()] = value
                    else:
                        attitudes[keyword.lower()] = value

            return {"emotions": emotions, "attitudes": attitudes}
                            
            # 构建输入提示
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are {agent_name}, {agent_description}."),
                (
                    "system",
                    "You are situated within a simulated environment characterized by the following properties {agent_world_state}",
                ),
                (
                    "system",
                    "Considering your population category ({population_category}), individuals exhibit the following characteristics: {category_description}."
                ),
                (
                    "system",
                    "Your current emotion is: {emotions}. \nYour current attitude is: {attitudes}."
                ),
                ("system", "The news content you have received is: {news_content}."),
                ("human", "{footer}"),
            ]
        )
        # 构建输入上下文
        input_context = {
            "agent_name": self.agent_state.name,
            "agent_description": self.agent_state.description,
            "agent_world_state": self.agent_state.host_world_prompt,
            "category_description": category_description,
            "population_category": self.agent_state.population_category,
            "emotions": self.agent_state.emotion,
            "attitudes": self.agent_state.attitude,
            "news_content": news_content,
            "footer": """"
                1. Generate new emotions and attitudes based on the news content and the your current emotions and attitudes state and attribute category;
                2. Ensure consistency in the format of emotions and attitudes in the generated responses;
                3. Simulate human reactions to news and reflect changes in various emotions and attitudes. Emotions must include happiness, sadness, and anger, and attitudes must include optimism, pessimism, and neutrality.
                4. Please be sure to output the answer
            
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
        print("emotion: ", response)
        response = parse_output(response)
        response = EmotionAttitudeResult.model_validate(response)
        self.logger.info(f"Emotion: {response}")
        return response.emotions, response.attitudes