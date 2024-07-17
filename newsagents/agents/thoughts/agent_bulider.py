import asyncio
from enum import Enum
import json
import os
import re
import sys
import bs4

from typing import List, Optional
import chromadb
import markdown
import ollama
from pydantic import BaseModel, Field
from genworlds.agents.abstracts.thought import AbstractThought
from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from genworlds.utils.logging_factory import LoggingFile
from newsagents.world.world_map import get_world_for_category, NewsCategory

class AgentBuilder(BaseModel):
    """A model for generating agent based on category and country."""
    id: str = Field(..., description="The unique identifier for the agent.")
    name: str = Field(..., description="The name of the agent.")
    description: str = Field(..., description="A detailed description of the agent.")
    host_world_prompt: str = Field(..., description="Prompt for the host world.")

class AgentBuilderThought(AbstractThought):
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

    def run(self, category: NewsCategory, country: str):
        def parse_agents(res: str, category: NewsCategory) -> List[AgentBuilder]:
            agents = []
            lines = res.strip().split('\n')
            host_world_prompt = f"{category.value.split()[0]} Social Network"
            
            agent_data = {}
            for line in lines:
                if line.startswith("agent"):
                    if agent_data:
                        agent_data['host_world_prompt'] = host_world_prompt
                        agents.append(AgentBuilder(**agent_data))
                        agent_data = {}
                if 'id:' in line:
                    agent_data['id'] = line.split('id: ')[1].strip()
                if 'name:' in line:
                    agent_data['name'] = line.split('name: ')[1].strip()
                if 'description:' in line:
                    agent_data['description'] = line.split('description: ')[1].strip()
            if agent_data:
                agent_data['host_world_prompt'] = host_world_prompt
                agents.append(AgentBuilder(**agent_data))
                
            return agents

        world = get_world_for_category(category)
        if world is None:
            raise ValueError(f"No world found for category: {category}")        

        # 检索匹配的Markdown文件
        docs_path = "/home/newsworld/newsagents/docs"
        country_code = country.split(' ')[0]  # 去掉括号和附加信息，仅保留国家代码
        category_name = category.value.split(' ')[0].lower()  # 仅保留类别的前面部分，并转换为小写
        markdown_filename = f"{country_code}_{category_name}.md"
        markdown_path = os.path.join(docs_path, markdown_filename)
        markdown_content = None  # 初始化内容变量
        if os.path.isfile(markdown_path):
            with open(markdown_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()

        parsed_result = parse_document(markdown_content)
        #level4_data = extract_level(parsed_result, 4)
        level3_data = extract_level(parsed_result, 3)
        level2_data = extract_level(parsed_result, 2)
        # level_data = level2_data + level3_data
        # all_data = result_to_string(parsed_result)


        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "You are a helpful AI assistant that utilizes the provided context to fulfill the user's request."
                ),
                (
                    "system", 
                    "The category of the news is {category}. The country of the news is {country}."
                ),
                (
                    "system", 
                    "The relevant groups of the news: {documents}."
                ),
                (
                    "human", 
                    "{footer}\n"
                ),
            ]
        ).partial(schema=AgentBuilder.model_json_schema())

        input_context = {
            "category": category,
            "country": country,
            "documents": level2_data,
            "footer": """
                1. Based on the category and country of the news and the relevant groups of the news, select all groups in a certain level of the relevant groups to fill in the agent template;
                2. Answers must follow the following format:
                    agent {n}: (nth agent)
                    id: {group}-agent
                    name: {group} Group
                    description: Representing {number} {country} {group}, reflecting their emotions, attitudes, and possible actions in response to the news.
                3. Ensure all answers adhere to this template, filling in the {group}, {name}, {number}, and {country} fields based on the contextual input:       
             """
        }


        output_parser = StrOutputParser()
        chain = prompt_template | self.llm | output_parser
        res = chain.invoke(input_context)
        print("res: ", res)

        agents = parse_agents(res, category)
        for agent in agents:
            self.logger.info(f"Generated Agent: {agent}")
            print(f"Generated Agent: {agent}")

        return agents
    

def parse_document(doc):
    lines = doc.strip().split('\n')
    result = []

    def add_to_result(level, content):
        current = result
        for _ in range(level - 1):
            current = current[-1][1]
        current.append((content, []))

    current_level = 1
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith("#"):
            level = stripped_line.count("#")
            content = stripped_line.lstrip("#").strip()
            add_to_result(level, content)
            current_level = level
        elif re.match(r'^\d+\.\s*\*\*', stripped_line):
            content = re.sub(r'^\d+\.\s*\*\*|\*\*$', '', stripped_line).strip()
            add_to_result(current_level + 1, content)
        elif re.match(r'^-\s', stripped_line):
            content = stripped_line.lstrip("-").strip()
            add_to_result(current_level + 2, content)

    return result

def result_to_string(result, level=1):
    output = []
    def traverse(result, level):
        for item, children in result:
            output.append("  " * (level - 1) + f"Level {level}: {item}")
            traverse(children, level + 1)
    traverse(result, level)
    return "\n".join(output)

def extract_level(parsed_result, target_level, current_level=1):
    extracted_data = []

    def traverse(result, level):
        nonlocal extracted_data
        for item, children in result:
            if level == target_level:
                extracted_data.append(item)
            else:
                traverse(children, level + 1)

    traverse(parsed_result, current_level)
    return extracted_data


# Example usage
if __name__ == "__main__":
    openai_api_key = "your_openai_api_key_here"
    agent_builder = AgentBuilderThought(openai_api_key=openai_api_key)
    
    category = NewsCategory.ACADEMIC
    country = "CN"
    agent = agent_builder.run(category, country)
    
    print(agent)


    # RAG
    # # Indexing: Load
    # loader = UnstructuredFileLoader(markdown_path, mode="elements")
    # data = loader.load()
    # print(f"Number of documents: {len(data)}\n")
    # # # Text Splitters
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000, chunk_overlap=200, add_start_index=True, separators=["\n\n"]
    # )
    # all_splits = text_splitter.split_documents(data)
    # documents = [
    #     text.page_content for text in all_splits
    # ]

    # client = chromadb.Client()
    # collection = client.create_collection(name="docs")
    # # store each document in a vector embedding database
    # for i, d in enumerate(documents):
    #     response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
    #     embedding = response["embedding"]
    #     collection.add(
    #         ids=[str(i)],
    #         embeddings=[embedding],
    #         documents=[d]
    #     )