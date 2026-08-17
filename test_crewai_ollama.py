import os
from crewai import Agent, Crew, Process, Task
from langchain_community.llms import Ollama

os.environ["OPENAI_API_KEY"] = "NA"

ollama_llm = Ollama(model="llama3")

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and kinetic systems',
    backstory='An expert analyst with a keen eye for technical truth and high-speed data flow.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_llm
)

task1 = Task(
    description='Analyze the current state of local LLMs and agent swarms.',
    expected_output='A concise 3-bullet summary of local swarm resilience.',
    agent=researcher
)

crew = Crew(
    agents=[researcher],
    tasks=[task1],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n[+] CrewAI + Ollama Execution Result:")
    print(result)
