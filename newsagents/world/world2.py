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

# 创建本、硕、博学生代理的初始状态
# http://www.moe.gov.cn/jyb_sjzl/moe_560/2022/quanguo/202401/t20240110_1099539.html
undergrad_initial_state = CustomAgentState(
    id="undergrad",
    name="Undergraduate Group",
    description="Representing 53.3 million Chinese undergraduate students, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
master_initial_state = CustomAgentState(
    id="master",
    name="Master's Group",
    description="Representing 3.1 million Chinese master's students, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
    population_category = PopulationCategory.AVERAGE,
    #is_planning=False
    news_content=[]
)
PhD_initial_state = CustomAgentState(
    id="PhD",
    name="Doctoral Group",
    description="Representing 550,000 Chinese doctoral students, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
    population_category = PopulationCategory.CALM,
    #is_planning=False
    news_content=[]
)

# 创建专任教师、行政人员、教辅人员、工勤人员、专职科研人员代理的初始状态
# http://www.moe.gov.cn/jyb_sjzl/moe_560/2022/quanguo/202401/t20240110_1099483.html
fulltime_teachers_initial_state = CustomAgentState(
    id="fulltime_teachers",
    name="Full-time Teachers",
    description="Representing 2.4 million Chinese full-time teachers, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
fulltime_researchers_initial_state = CustomAgentState(
    id="fulltime_researchers",
    name="Full-time Researchers",
    description="Representing 60000 Chinese full-time researchers, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
adm_initial_state = CustomAgentState(
    id="Adm",
    name="Adm Personnel",
    description="Representing 500000 Chinese administration personnel, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
supporting_initial_state = CustomAgentState(
    id="supporting",
    name="Supporting Staff",
    description="Representing 300000 Chinese Supporting Staff, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
    population_category = PopulationCategory.AVERAGE,
    # is_planning=False
    news_content=[]
)
workers_initial_state = CustomAgentState(
    id="workers",
    name="Workers",
    description="Representing 150000 Chinese workers, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
    population_category = PopulationCategory.AVERAGE,
    # is_planning=False
    news_content=[]
)
others_initial_state = CustomAgentState(
    id="others",
    name="others Staff",
    description="Representing 50000 Chinese other affiliated agency staff, reflecting their emotions, attitudes and possible actions in response to the news",
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
        # "Agent_Likes_News_Action_schemas": "AgentLikesNewsAction",
        # "Agent_Shares_News_Action_schemas": "AgentSharesNewsAction",
        # "Agent_Comments_On_News_Action_schemas": "AgentCommentsOnNewsAction",
        # "Agent_Follows_NewsAction_schemas": "AgentFollowsNewsAction",
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
    population_category = PopulationCategory.AVERAGE,
    # is_planning=False
    news_content=[]
)

# 创建学生代理并运行他们的 think_n_do 函数
undergraduate_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    name="Undergraduate Group",
    id="undergrad",
    description="Reflecting undergraduate groups' reaction to the news",
    initial_agent_state=undergrad_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
master_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="master",
    name="Master's Group",
    description="Reflecting master groups' reaction to the news",
    initial_agent_state=master_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
PhD_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="PhD",
    name="Doctoral Group",
    description="Reflecting PhD groups' reaction to the news",
    initial_agent_state=PhD_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)


# 创建老师代理并运行他们的 think_n_do 函数
fulltime_teachers_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="fulltime_teachers",
    name="Full-time Teachers",
    description="Reflecting full-time teachers groups' reaction to the news",
    initial_agent_state=fulltime_teachers_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
fulltime_researchers_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="fulltime_researchers",
    name="Full-time Researchers",
    description="Reflecting full-time researchers groups' reaction to the news",
    initial_agent_state=fulltime_researchers_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
adm_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="Adm",
    name="Adm Personnel",
    description="Reflecting administration personnel groups' reaction to the news",
    initial_agent_state=adm_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
supporting_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="supporting",
    name="Supporting Staff",
    description="Reflecting supporting staff groups' reaction to the news",
    initial_agent_state=supporting_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
workers_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="workers",
    name="Workers",
    description="Reflecting workers groups' reaction to the news",
    initial_agent_state=workers_initial_state,
    action_classes=action_classes,
    other_thoughts=[],
    host_world_prompt="Academic Social Network",
)
others_group_agent = NewsNetworkAgent(
    openai_api_key="llama3",
    id="others",
    name="others Staff",
    description="Reflecting other affiliated agency staff groups' reaction to the news",
    initial_agent_state=others_initial_state,
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
    agents=[undergraduate_group_agent, master_group_agent, PhD_group_agent, fulltime_teachers_group_agent, fulltime_researchers_group_agent, adm_group_agent, supporting_group_agent, workers_group_agent, others_group_agent]
)

# 启动世界
NewsAgentsWorld.launch()

