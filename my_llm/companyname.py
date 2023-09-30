from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field, validator
from typing import List

import json

from dotenv import load_dotenv

load_dotenv()


class CompanyName(BaseModel):
    company_names: List[str] = Field(description="list of names of companies")


def llm_company_name(product: str, howmany: int = 1):

    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["product", "howmany"],
        template="Give me {howmany} cool company names that makes {product}?",
    )

    chain = LLMChain(llm=llm, prompt=prompt, output_key="company_names")

    output =  chain.run({
        'product': product,
        'howmany': howmany
    })

    parser = PydanticOutputParser(pydantic_object=CompanyName)

    fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

    return fix_parser.parse(output)


if __name__ == "__main__":
    product_name = str(input("What is the product name: "))
    howmany = int(input("How many name you want: "))
    print(llm_company_name(product_name, howmany))