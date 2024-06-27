import asyncio
from enum import Enum
import json
import re

import sys
import websockets
from typing import List, Optional
from genworlds.agents.abstracts.thought import AbstractThought
from newsagents.agents.custom_agent_state import CustomAgentState
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field, ConfigDict
#from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.structured_output import (
    create_structured_output_runnable
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from genworlds.utils.logging_factory import LoggingFile
from newsagents.world.world_map import NewsCategory
  
    
class NewsClassifierThought(AbstractThought):
    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "llama3",
    ):
        self.model_name = model_name
        self.llm = ChatOpenAI(
            model=self.model_name, openai_api_key=openai_api_key, temperature=0.1
        )
        self.logger = LoggingFile.get_logger(self.__class__.__name__)

    def run(self, news_content):
        class NewsClassifier(BaseModel):
            """A model for classifying news articles including their category and country of origin."""
            category: NewsCategory = Field(..., description="The category of the news article")
            country: str = Field(..., description="The country where the news article originated")
            title: Optional[str] = Field(None, description="The title of the news article")
            keywords: Optional[List[str]] = Field(None, description="A list of keywords associated with the news article")

        def extract_news_metadata(news_text):
            # Extracting the relevant parts from the given text
            category_line = [line for line in news_text.split('\n') if line.startswith('category:')][0]
            country_line = [line for line in news_text.split('\n') if line.startswith('country:')][0]
            
            # Extracting the values from the lines
            category = category_line.split(': ')[1].strip()
            country = country_line.split(': ')[1].strip()
        
            # Returning the result as a dictionary
            return {"category": category, "country": country}

        news_categories = ", ".join([category.value for category in NewsCategory])

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", "The news content you have received is: {news_content}. "
                ),
                (
                    "system", "The news categories include: {news_category}. "
                ),
                ("human", "{footer}\n"),
            ]
        ).partial(schema=NewsClassifier.model_json_schema())

        input_context = {
            "news_content": news_content,
            "news_category": news_categories,
            "footer": """
                1. Based on the news content and news categories, analyze and infer which category the news belongs to and which country it is from, the category must appear in the context;
                2. Answers should follow the following format:
                    category: {news category}
                    country: {country abbreviation}
                    title: {news title}
                    keywords: {keywords}
                """
        } 

        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        res = chain.invoke(input_context)
        print("res: ",res)
        
        metadata = extract_news_metadata(res)
        self.logger.info(f"Extracted Metadata: {metadata}")
        response = NewsClassifier.model_validate(metadata)

        print(f"News Category: {response.category}, Country: {response.country}")
        self.logger.info(f"News Category: {response.category}, Country: {response.country}")

        return response.category, response.country


