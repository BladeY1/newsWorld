import os
from time import sleep

from newsagents.agents.thoughts.agent_bulider_large import AgentsBuilderThought
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

agents_builder = AgentsBuilderThought(
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

news3 = NewsObject(
    id="news_3",
    title="Biden and Trump to Run for the 60th U.S. Presidential Election in 2024",
    content="""June 27, 2024: At 9 p.m., Biden and Trump participated in the first major televised debate hosted by CNN in Atlanta, Georgia. Many domestic and foreign media criticized Biden's performance, noting concerns about his health and judgment. This sparked discussions within the Democratic Party about whether Biden should step aside for another candidate.

Following the debate: Biden's team launched a series of campaign activities to reassure supporters, stating their commitment to his candidacy. Former President Obama and former Secretary of State Hillary Clinton reiterated their support for Biden. ABC News reported that Biden failed to demonstrate his capability to serve another term. New York Times columnist Thomas Friedman suggested Biden should withdraw in favor of Vice President Kamala Harris or other potential candidates.

July 13, 2024: At 6:11 p.m., former President Donald Trump was shot by an American man during a rally at the Butler Farm Show Grounds in Butler, Pennsylvania. Although not seriously injured, Trump's right ear was grazed by an unknown object. Bloodied, he stood up under the protection of Secret Service bodyguards, raised his fist, and shouted “Fight! Fight! Fight!” three times, eliciting cheers and chants of “U-S-A!” from the crowd. This iconic moment was featured on the cover of Time magazine on July 14. Trump was taken to the hospital in stable condition and flew to New Jersey that evening.

July 14, 2024: Elon Musk expressed his full support for Trump and wished him a speedy recovery.

July 15, 2024: U.S. House Speaker Mike Johnson, a Republican, officially announced at the Republican National Convention the nomination of Donald Trumpas the Republican candidates for President.
    """,
    publisher_id="publisher_3",
    category=NewsCategory.POLITICAL,
    publish_time="2024-06-28"

)

new4 = NewsObject(
    id="news_4",
    title="Japan dumps nuclear waste into Pacific Ocean",
    content="""August 24, 2023: The Japanese government decided to begin discharging treated radioactive wastewater from the Fukushima Daiichi Nuclear Power Plant into the Pacific Ocean. This wastewater, exceeding one million tons, had been contaminated with radioactive nuclides. Under the approval of the Japanese government and the supervision of the International Atomic Energy Agency (IAEA), the radioactive water is being filtered and diluted before gradually being released into the ocean. The entire discharge plan is expected to span at least 30 years.

Background: The issue began with the Fukushima Daiichi Nuclear Power Plant disaster caused by the Great East Japan Earthquake on March 11, 2011. A massive tsunami damaged the plant's cooling systems, leading to the meltdown of three reactors and leaving behind molten nuclear fuel debris. Continuous pumping of seawater into the reactors was required to cool the melted fuel, resulting in a large amount of nuclide-contaminated cooling water. Chemical explosions during the disaster also led to the release of radioactive materials into the atmosphere and the Pacific Ocean. As of March 2023, the plant had accumulated 1.25 million tons of radioactive wastewater, with the volume still increasing.

Storage and Treatment: Since the accident, the plant has stored the contaminated cooling water in tanks and used the Advanced Liquid Processing System (ALPS) to remove radioactive substances, except tritium and carbon-14. With the increasing volume of stored water, the plant faced storage capacity issues. The Japanese authorities discussed wastewater disposal options for years to advance the plant's decommissioning.

Government Approval: In April 2021, the Japanese Cabinet approved the plan to discharge ALPS-treated wastewater into the Pacific Ocean. The authorities stated that tritium and carbon-14, which ALPS cannot remove, would be diluted to safe levels. In July 2023, the IAEA released a comprehensive safety review, concluding that the discharge met international safety standards and posed negligible risks to humans and the environment.

Post-Discharge Monitoring: After the discharge began on August 24, 2023, the IAEA conducted independent sampling and measurement of seawater near the plant, confirming that tritium levels were within safe limits.

International Reactions: The discharge of radioactive wastewater has sparked a range of international responses.
    """,
    publisher_id="publisher_4",
    category=NewsCategory.SOCIAL,
    publish_time="2023-08-24"

)

category, country = news_classifier.run(news3.content, news3.category)
sleep(0.5)
agents = agents_builder.run(category, country)

agent_states = create_agent_states(agents)

# 创建代理并运行他们的 think_n_do 函数
agents = create_agents_from_states(agent_states)

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
    objects=[news3],
    agents=agents
)

# 启动世界
NewsAgentsWorld.launch()

