''' doc string for company name '''

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

DOTEBV_PATH = "../.env"  # Path to the .env file in the parent directory
load_dotenv(DOTEBV_PATH)


def llm_company_name(topic: str = "icecream", howmany: int = 1):

    ''' JOkes '''

    llm = OpenAI(temperature=0.9)

    prompt = PromptTemplate(
        input_variables = ["howmany", "topic"],
        template = "Give me {howmany} cool and innovative name for a/an {topic} company",
    )

    # prompt = prompt.format(topic = topic, howmany = howmany)

    chain = (
        prompt | llm
    )

    # output = chain.invoke({"topic": topic, "howmany": howmany})

    # return output

    for chunk in chain.stream({"topic": topic, "howmany": howmany}):
        yield chunk
        # print(chunk, end="", flush=True)


if __name__ == "__main__":
    TOPIC = str(input("What kind of company: "))
    HOW_MANY = int(input("How many names: "))
    
    # Generating company names
    generated_names = llm_company_name(TOPIC, HOW_MANY)
    
    # Printing the generated names
    for name in generated_names:
        print(name, end="", flush=True)
