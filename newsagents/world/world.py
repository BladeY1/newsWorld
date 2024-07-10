import os
from newsagents.world.custom_world import CustomWorld
from newsagents.agents.agents import NewsNetworkAgent
from newsagents.objects.news import NewsObject
from newsagents.agents.custom_agent_state import (
    CustomAgentState,
    PopulationCategory
)
from newsagents.events.events import AgentReceivesNewsEvent
from newsagents.agents.custom_state_manager import CustomStateManager
from newsagents.agents.custom_action_planner import CustomActionPlanner
from newsagents.agents.thoughts.action_schema_selector import ActionSchemaSelectorThought
from newsagents.agents.thoughts.event_filler import EventFillerThought
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")
openai_api_key = os.getenv("OPENAI_API_KEY")

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
    category="Education",
    publish_time="2024-04-17"
)

# 定义动作列表
action_classes = [
    # AgentCommentsOnNewsAction,
    # AgentFollowsNewsAction,
    # AgentLikesNewsAction,
    # AgentSharesNewsAction
]

# 创建学生代理的初始状态
student_initial_state = CustomAgentState(
    id="student_root",
    name="Student Group",
    description="Representing 57 million Chinese students, reflecting their emotions, attitudes and possible actions in response to the news",
    host_world_prompt="Academic Social Network",
    simulation_memory_persistent_path = "newsworld/newsagents/agents/memories",
    memory_ignored_event_types=set(),
    wakeup_event_types=[],
    action_schema_chains=[],
    goals=[
        # "Create new agents representing undergraduate, graduate, and doctoral students from various disciplines.",
        "According to the group you belong to and the characteristics of the group, capture the different views and reactions of students from different backgrounds, titles, and majors to news events.",
        "Participate in discussions and debates on current affairs and express your attitudes and emotions towards news reports.",
        "According to the group's emotions and attitudes, take interactive actions such as sharing, commenting, liking, and following related news content."
    ],
    plan=[],
    last_retrieved_memory="",
    other_thoughts_filled_parameters={},
    available_action_schemas = {
        "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
        #"News_Propagation_Action_schemas": "NewsPropagationAction"
    },
    available_entities=[],
    is_asleep=False,
    current_action_chain=[],
    emotion={
        "happiness": 0.0, "sadness": 0.0, "anger": 0.0
    },  
    attitude={
        "optimism": 0.0, "pessimism": 0.0, "neutrality": 0.0
    },  
    population_category = PopulationCategory.SUSCEPTIBLE,
    #is_planning=False
    news_content=[]
)

# 创建老师代理的初始状态
teacher_initial_state = CustomAgentState(
    id="teacher_root",
    name="Teacher Group",
    description="Representing 3.5 million Chinese teachers, reflecting their emotions, attitudes and possible actions in response to the news",
    host_world_prompt="Academic Social Network",
    simulation_memory_persistent_path = "newsworld/newsagents/agents/memories",
    memory_ignored_event_types=set(),
    wakeup_event_types=[],
    action_schema_chains=[],
    goals=[
        # "Generate new agents representing educators from different disciplines and educational levels.",
        "According to the group you belong to and its characteristics, capture the different views and reactions of teachers with different backgrounds, titles, and majors to news events.",
        "Participate in discussions and debates on current affairs and express your attitudes and emotions towards news reports.",
        "According to the group's emotions and attitudes, take interactive actions such as sharing, commenting, liking, and following relevant news content."
    ],
    plan=[],
    last_retrieved_memory="",
    other_thoughts_filled_parameters={},
    available_action_schemas = {
        "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
       # "News_Propagation_Action_schemas": "NewsPropagationAction"
    },
    available_entities=[],
    is_asleep=False,
    current_action_chain=[],
    emotion={
        "happiness": 0.0, "sadness": 0.0, "anger": 0.0
    },  
    attitude={
        "optimism": 0.0, "pessimism": 0.0, "neutrality": 0.0
    },  
    population_category = PopulationCategory.CALM,
    # is_planning=False
    news_content=[]
)

# 创建学生和老师代理并运行他们的 think_n_do 函数
student_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    name="Student Group",
    id="student_root",
    description="Representing 57 million Chinese students, reflecting their emotions, attitudes and possible actions in response to the news",
    initial_agent_state=student_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
teacher_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    name="Teacher Group",
    id="teacher_root",
    description="Representing 3.5 million Chinese teachers, reflecting their emotions, attitudes and possible actions in response to the news",
    initial_agent_state=teacher_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)

# student_group_agent.add_wakeup_event(event_class=AgentReceivesNewsEvent)
# teacher_group_agent.add_wakeup_event(event_class=AgentReceivesNewsEvent)

# 创建一个名为NewsAgentsWorld的世界实例
NewsAgentsWorld = CustomWorld(
    name="NewsAgents",
    description="""A social network focused on news dissemination within the academic community. It is a platform where users from the academic circle can share, comment, follow, and engage with news articles and other media content. The network is designed to facilitate conversations around current events, research, and other topics of interest within the academic community.""",
    id="newsagents-world",
    actions=action_classes,
    objects=[news],
    agents=[student_group_agent, teacher_group_agent]
)

# 启动世界
NewsAgentsWorld.launch()

