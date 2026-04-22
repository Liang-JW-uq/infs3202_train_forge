from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from django.http import JsonResponse
from pydantic import BaseModel, Field
from orm.models import UserTrainer, Client, Exercise, Tag
from django.forms.models import model_to_dict

from pydantic import BaseModel, Field
from typing import List, Optional


# Have to ensure result return from llm matches to workoutexercise model
# in order for easy insertion into inline formset rows
class WorkoutExercise(BaseModel):
    id: int = Field(description="the exact id from the exercises in the provided data")
    name: str = Field(description="the name of the exercise")
    def_sets: Optional[int] = Field(0, description="number of sets to perfrom")
    def_reps: Optional[int] = Field(0, description="reptitions per set")
    def_weight: Optional[float] = Field(0.0, description="suggested weight in kg")
    def_duration: Optional[int] = Field(0, description="duration in minutes for cardio")

class WorkoutPlan(BaseModel):
    exercises: List[WorkoutExercise]
    ai_explanation: Optional[str] = Field(
        # default="",
        description="a brief overall explanation of why the workout was recommended"
    )

class StructuredOutput(BaseModel):
    question: str = Field(description='The question')
    answer: str = Field(description='The answer to the question')

def ask(request, prompt):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        google_api_key='AIzaSyC0w0i5lk99Ind_jHkPT7aCXYy8xAkoTlo',
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
        google_api_key='AIzaSyC0w0i5lk99Ind_jHkPT7aCXYy8xAkoTlo',
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
        google_api_key='AIzaSyC0w0i5lk99Ind_jHkPT7aCXYy8xAkoTlo',
        temperature=0.5,
        max_tokens=150
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', """
            You are a university lecturer with certification in meteorology studies.
        """),
        ('human', """
            question: {question}
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


def generate_workout(request, client_id, no_of_exercises):
    trainer = UserTrainer.objects.get(id=request.user.id)

    # Primary model is for Google Gemini
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        google_api_key='AIzaSyC0w0i5lk99Ind_jHkPT7aCXYy8xAkoTlo',
    )
    # # Backup model
    # llm2 = ChatOpenAI(
    #     model='nvidia/nemotron-3-super-120b-a12b:free',
    #     api_key='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',
    #     base_url='https://openrouter.ai/api/v1'
    # )

    trainer_prompt = get_prompt()
    library = get_data(trainer.id, client_id)
    print(f"Exercises 2: {list(library.get('exercises'))}")
    
    # ------------- Structured Output
    structured_llm = llm.with_structured_output(WorkoutPlan, include_raw=True)
    chain = trainer_prompt | structured_llm
    response = chain.invoke({
        'no_of_exercises': no_of_exercises,
        'client_info': library.get('client'),
        'exercise_list': library.get('exercises')
    })
    workout_data = response.get('parsed')
    # usage = response.get('raw').usage_meta
    return JsonResponse({
        'answer': workout_data.model_dump()
    })

    # ------------- Unstructured Output
    # chain = trainer_prompt | llm
    # response = chain.invoke({
    #     'no_of_exercises': no_of_exercises,
    #     'client_info': library.get('client'),
    #     'exercise_list': library.get('exercises')
    # })
    # # answer = response.get('parsed')

    # # workout_data = response.get('parsed')           # using with_structure_output only
    # usage = response.usage_metadata
    # return JsonResponse({
    #     "content": response.content,
    #     "input_tokens": usage.get("input_tokens"),
    #     "output_tokens": usage.get("output_tokens")
    # }, safe=False)


def get_data(trainer_id, client_id):
    # client = Client.objects.get(id=client_id)
    # client_data = model_to_dict(client)

    client = Client.objects.values('id', 'name', 'age', 'height', 'weight', 'goals').get(id=client_id)
    exercises = Exercise.objects.filter(trainer__id=trainer_id)
    # {
    #     'id': 1,
    #     'name': 'Push Ups',
    #     'tags': ['slimming', 'body-build']
    # }
    exercise_list = []
    for exercise in exercises:
        exercise_obj = {
            'id': exercise.id,
            'name': exercise.name,
            'def_sets': exercise.def_sets,
            'def_reps': exercise.def_reps,
            'def_weight': float(exercise.def_weight) if exercise.def_weight is not None else None,
            'def_duration': exercise.def_duration,
            'tags': [tag.name for tag in exercise.tags.all()],
        }
        exercise_list.append(exercise_obj)
    

    return {'client': client, 'exercises': exercise_list}

def get_prompt():
    chat_prompt = ChatPromptTemplate.from_messages([
        (
            "system", """
            You are a personal trainer.

            You will receive a client info
            - age, height, weight, goals

            You will receive a list of exercises. Each exercise includes:
            - name, instructions, default sets/reps/weight or duration
            - tags (representing muscle groups or workout goals, training styles but NOT equipment)
            - you may refer to the exercises tag for selection

            Task:
            - Select exactly {no_of_exercises} exercises based on the client goals, age, height, weight
            - ONLY use exercises from the list

            You may adjust sets, reps, weight, or duration

            You MUST return ALL fields defined in the schema.

            This is your data:
            Client: {client_info}
            Exercises: {exercise_list}
            """
        ),
        (
            "human", """
            """
        ),
    ])

    return chat_prompt
