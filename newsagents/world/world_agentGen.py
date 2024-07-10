import os
from time import sleep

from newsagents.world.custom_world import CustomWorld
from newsagents.agents.agents import NewsNetworkAgent, create_agents_from_states
from newsagents.objects.news import NewsObject
from newsagents.agents.custom_agent_state import (
    CustomAgentState,
    PopulationCategory,
    create_agent_states
)
from newsagents.agents.thoughts.agent_bulider import AgentBuilderThought
from newsagents.agents.thoughts.news_classifier import NewsClassifierThought
from newsagents.world.world_map import NewsCategory, World, get_world_for_category
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")
openai_api_key = os.getenv("OPENAI_API_KEY")


news_classifier = NewsClassifierThought(
    openai_api_key=openai_api_key,
    model_name="llama3",
)

agent_builder = AgentBuilderThought(
    openai_api_key=openai_api_key,
    model_name="llama3",
)

# 创建一个新闻对象
news = NewsObject(
    id="news_1",
    title="Investigation and Handling of Academic Misconduct by Teacher at Huazhong Agricultural University",
    content="""On January 16, 2024, netizens revealed a report letter signed and fingerprinted by multiple students from Huazhong Agricultural University, accusing their supervisor, Professor Huang Feiruo, of academic misconduct such as data tampering and fabricating experimental results.

On February 6, 2024, Huazhong Agricultural University announced the investigation and handling of academic misconduct by teacher Huang. After investigation, Huang's academic misconduct was confirmed, leading to the termination of his employment contract and the withdrawal of papers and projects related to the misconduct.

The whistleblowers, including 11 students from the School of Animal Science and Technology and the College of Veterinary Medicine, detailed various issues in Huang's supervision, including data manipulation and plagiarism.

Huang, a former undergraduate and doctoral student of Huazhong Agricultural University, became a professor in 2017. He has published over 40 SCI papers and led numerous research projects. However, his unethical practices have tarnished his reputation and led to severe consequences.

The incident has raised concerns about academic integrity and the treatment of whistleblowers in academic institutions. It highlights the importance of upholding ethical standards in research and education.

For more details on the investigation and its implications, stay tuned for further updates.""",
    publisher_id="publisher_1",
    category=NewsCategory.Education,
    publish_time="2024-04-17"
)

news2 = NewsObject(
    id="news_2",
    title="Female students from technical secondary school enter finals of global mathematics competition",
    content="""Reported on June 13, recently, Jiang Ping, a 17-year-old girl from Huai'an, Jiangsu Province, received good news. She entered the finals of the mathematics competition with a global ranking of 12, becoming the first secondary school student to enter the finals in the history of the competition. The list of finalists announced by the organizing committee shows that most of the 801 contestants who advanced this time are from famous universities such as Tsinghua University, Peking University, MIT, and Cambridge. It is understood that Jiang Ping's major is fashion design, but she is very obsessed with mathematics. She has always insisted on self-study in her spare time and has spent 2 years self-studying partial differential equations. It has triggered intense discussions and received support from many senior mathematical predecessors.
On June 14, Jiang Ping interviewed earlier that she wanted to apply for Zhejiang University. Zhejiang University responded to whether Jiang Ping could be admitted as an exception: it involves the corresponding process and cannot be answered for the time being.
After June 17, a large number of netizens questioned. Some people dug up what seemed to be Jiang Ping's test scores and questioned why Jiang Ping's previous scores were not outstanding, but she suddenly achieved amazing results in this competition; some people questioned that in some promotional photos, Jiang Ping's blackboard writing seemed to have errors; some people said that the competition was open-book and the results were the result of Jiang Ping cheating.
On June 27, it was true that Jiang Ping, a student at Lianshui Secondary Vocational School, scored 83 points in the monthly math test. A large number of netizens believed that this proved that Jiang Ping cheated in the Alibaba math competition.
    """,
    publisher_id="publisher_2",
    category=NewsCategory.Education,
    publish_time="2024-06-14"

)
   


category, country = news_classifier.run(news2.content)
sleep(0.5)
agents = agent_builder.run(category, country)

agent_states = create_agent_states(agents)

# 创建代理并运行他们的 think_n_do 函数
agents = create_agents_from_states(agent_states)

# student_group_agent.add_wakeup_event(event_class=AgentReceivesNewsEvent)
# teacher_group_agent.add_wakeup_event(event_class=AgentReceivesNewsEvent)
# 定义动作列表
action_classes = [
    # AgentCommentsOnNewsAction,
    # AgentFollowsNewsAction,
    # AgentLikesNewsAction,
    # AgentSharesNewsAction
]
world = get_world_for_category(category)
# 创建一个名为NewsAgentsWorld的世界实例
NewsAgentsWorld = CustomWorld(
    name=world.name,
    description=world.description,
    id=world.id,
    actions=action_classes,
    objects=[news2],
    agents=agents
)

# 启动世界
NewsAgentsWorld.launch()

