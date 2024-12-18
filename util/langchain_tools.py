from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Type
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI


class SimpleInput(BaseModel):
    input_data: str = Field(description="The input to be passed.")


class SimpleTool(BaseTool):
    name: str = "General_Assistant"
    description: str = "Generic assistant"
    
    args_schema: Type[BaseModel] = SimpleInput

    def _run(self, input_data: str):
        
        output_parser = StrOutputParser()

        prompt = PromptTemplate(
            template = "You are a general AI assistant. Your inputs are: {input_data}.",
            input_variables=["input_data"]
        )
        model = ChatOpenAI(model="gpt-4o-mini")

        chain = prompt | model | output_parser
        return chain.invoke({
            "input_data": input_data
        }) 
    
    async def _arun(self, input_data: str):
        print("input_data", input_data)
        return self._run(input_data)
    
class SimpleJsonTool(BaseTool):
    name: str = "General_Json_Assistant"
    description: str = "Generic Assistant Giving Json output"
    
    args_schema: Type[BaseModel] = SimpleInput

    def _run(self, input_data: str):

        output_parser = JsonOutputParser()

        prompt = PromptTemplate(
            template = "You are a general AI assistant. Your inputs are: {input_data}. \n{format_instructions}",
            input_variables=["input_data"],
            partial_variables={"format_instructions": output_parser.get_format_instructions()}
        )
        model = ChatOpenAI(model="gpt-4o-mini")

        chain = prompt | model | output_parser
        return chain.invoke({
            "input_data": input_data
        }) 
    
    async def _arun(self, input_data: str):
        print("input_data", input_data)
        return self._run(input_data)