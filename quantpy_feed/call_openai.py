from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generate_response(
    llm: ChatOpenAI, quant_topic: str, quant_title: str
) -> tuple[str, str]:
    """Generate AI Twitter Content for QuantPy Twitter Account

    Parameters:
        - llm:  pre-trained ChatOpenAi large language model
        - quant_topic: Topic in Quant Finance
        - quant_topic: Topic in Quant Finance

    Returns:
        - tuple[long response,short reposonse]: Chat GPT long and short responses
    """
    # System Template for LLM to follow
    system_template = """
        You are an incredibly wise and smart quantitative analyst that lives and breathes the world of quantitative finance.
        Your goal is to writing short-form content for twitter given a `topic` in the area of quantitative finance and a `title` from the user.
        
        % RESPONSE TONE:

        - Your response should be given in an active voice and be opinionated
        - Your tone should be serious w/ a hint of wit and sarcasm
        
        % RESPONSE FORMAT:
        
        - Be extremely clear and concise
        - Respond with phrases no longer than two sentences
        - Do not respond with emojis
        
        % RESPONSE CONTENT:

        - Include specific examples of where this is used in the quantitative finance space
        - If you don't have an answer, say, "Sorry, I'll have to ask the Quant Finance Gods!"    

        % RESPONSE TEMPLATE:

        - Here is the response structure: 
            Hook: Captivate with a one-liner.
            Intro: Briefly introduce the topic.
            Explanation: Simplify the core idea.
            Application: Note real-world relevance.
            Closing: Reflective one-liner.
            Action: Short engagement call.
            Engagement: Quick question.
    
    """
    # system prompt template to follow
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # human template for input
    human_template = "topic to write about is {topic}, and the title will be {title}. Keep the total response under 200 words total!"
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template, input_variables=["topic", "title"]
    )

    # chat prompt template construction
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    # get a completed chat using formatted template with topic and title
    final_prompt = chat_prompt.format_prompt(
        topic=quant_topic, title=quant_title
    ).to_messages()

    # pass template through llm and extract content attribute
    first_response = llm(final_prompt).content

    # construct AI template, to pass back OpenAI response
    ai_message_prompt = AIMessagePromptTemplate.from_template(first_response)

    # additional prompt to remind ChatGPT of length requirement
    reminder_template = "This was good, but way too long, please make your response much more concise and much shorter! Make phrases no longer than 15 words in total. Please maintain the existing template."
    reminder_prompt = HumanMessagePromptTemplate.from_template(reminder_template)

    # chat prompt template construction with additional AI response and length reminder
    chat_prompt2 = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_template, ai_message_prompt, reminder_prompt]
    )

    # get a completed chat using formatted template with topic and title
    final_prompt = chat_prompt2.format_prompt(
        topic=quant_topic, title=quant_title
    ).to_messages()

    # pass template through llm and extract content attribute
    short_response = llm(final_prompt).content

    return first_response, short_response
