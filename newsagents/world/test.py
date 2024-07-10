import os
import chromadb.utils.embedding_functions as embedding_functions
from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import chromadb
import ollama
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")



load_dotenv(dotenv_path="../.env")
openai_base = os.getenv("OPENAI_API_BASE")
hf_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")


country = "CN"
category = "Academic News"

# 检索匹配的Markdown文件
docs_path = "/home/newsworld/newsagents/docs"
country_code = country.split(' ')[0]  # 去掉括号和附加信息，仅保留国家代码
category_name = category.split(' ')[0].lower()  # 仅保留类别的前面部分，并转换为小写
markdown_filename = f"{country_code}_{category_name}.md"
# markdown_filename = f"{country_code}_{category_name}.md"
markdown_path = os.path.join(docs_path, markdown_filename)

if not os.path.isfile(markdown_path):
    markdown_path = None

# Indexing: Load
loader = UnstructuredFileLoader(markdown_path, mode="elements")
# loader = TextLoader(markdown_path, encoding = "utf8")
data = loader.load()
print(f"Number of documents: {len(data)}\n")
# # Text Splitters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True, separators=["\n\n"]
)
all_splits = text_splitter.split_documents(data)

# ollama_ef = embedding_functions.OllamaEmbeddingFunction(
#     url="http://localhost:11434/api/embeddings",
#     model_name="llama3",
# )

# embeddings = ollama_ef(text_contents)
documents = [
    text.page_content for text in all_splits
]
print(documents)

# client = chromadb.Client()
# collection = client.create_collection(name="docs")


# # store each document in a vector embedding database
# for i, d in enumerate(documents):
#   response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
#   embedding = response["embedding"]
#   collection.add(
#     ids=[str(i)],
#     embeddings=[embedding],
#     documents=[d]
#   )


# # an example prompt
# prompt = "How many teachers and students?"

# # generate an embedding for the prompt and retrieve the most relevant doc
# response = ollama.embeddings(
#   prompt=prompt,
#   model="mxbai-embed-large"
# )
# results = collection.query(
#   query_embeddings=[response["embedding"]],
# )
# data = results['documents']
# print("data: ", data)
# # generate a response combining the prompt and data we retrieved in step 2
# output = ollama.generate(
#   model="llama3",
#   prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
# )

# print(output['response'])


