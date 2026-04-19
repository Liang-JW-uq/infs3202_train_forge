from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from django.http import JsonResponse
from pydantic import BaseModel, Field

class StructuredOutput(BaseModel):
    question: str = Field(description='The question')
    answer: str = Field(description='The answer to the question')

def ask(request, prompt):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        google_api_key='AIzaSyAx5N01FrMAXF74LpMqg1wSy7FAzxtFmxg',
        temperature=0.3
    )

    response = llm.invoke(prompt)

    # return JsonResponse({'response': response.content}, safe=False)


    usage = response.usage_metadata
    return JsonResponse({
        "content": response.content,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens")
    }, safe=False)


def ask2(request, prompt):

    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        google_api_key='AIzaSyAx5N01FrMAXF74LpMqg1wSy7FAzxtFmxg',
        temperature=0.5,
        max_tokens=150
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        ('system', """
            You are a university lecturer with certification in meteorology studies.
        """),
        ('human', """
            Question: {question}
        """)
    ])

    chain = chat_prompt | llm

    response = chain.invoke({'question': prompt})

    
    
    usage = response.usage_metadata
    return JsonResponse({
        "content": response.content,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens")
    }, safe=False)


def ask3(request, prompt):

    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        google_api_key='AIzaSyAx5N01FrMAXF74LpMqg1wSy7FAzxtFmxg',
        temperature=0.5,
        max_tokens=150
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', """
            You are a university lecturer with certification in meteorology studies.
        """),
        ('human', """
            Question: {question}
        """)
    ])
    
    structured_llm = llm.with_structured_output(StructuredOutput, include_raw=True)
    chain = prompt_template | structured_llm
    response = chain.invoke({'question': prompt})
    answer = response.get('parsed')

    # workout_data = response.get('parsed')           # using with_structure_output only
    usage = response.get('raw').usage_metadata      # just curious about this !!!

    return JsonResponse({
        'content': answer.model_dump(),
        'input_tokens': usage.get('input_tokens'),
        'output_tokens': usage.get('output_tokens')
    }, safe=False)

    # response = chain.invoke({'question': prompt})
    
    # usage = response.usage_metadata
    # return JsonResponse({
    #     "content": response.content,
    #     "input_tokens": usage.get("input_tokens"),
    #     "output_tokens": usage.get("output_tokens")
    # }, safe=False)
