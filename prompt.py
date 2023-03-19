import openai
from os import environ

key = ''

openai.api_key = ''


class CompanyDetails:
    def __init__(self, company_name: str, company_bio: str, contact_info: str, negative_response_threshold: float) -> None:
        """
        company_name: name of company
        company_bio: description of company
        contact_info: email address of company
        negative_response_threshold: reviews with sentiment under this threshold will receive sympathetic responses.
        """
        self.company_name = company_name
        self.company_bio = company_bio
        self.contact_info = contact_info
        self.negative_response_threshold = negative_response_threshold  # If the review's sentiment score is below this score


# def generate_prompt(review: str, company_details: CompanyDetails) -> str:
#     company_bio = company_details.company_bio
#     contact_info = company_details.contact_info
#     prompt = f"Pretend you are the owner of the following company:\n{company_bio}\nCraft a response to the following review. Be sure to mention that they should reach out to {contact_info} to make things right:\n{review}"
#     return prompt


def get_manager_response(topics: str, email: str) -> str:

    prompt = f"Pretend you are an apologetic business owner tasked with responding to negative reviews. After this prompt, you will told the topics the customers had issues with. Create a response to a negative review that was about these topics. Do not offer a discount. Mention that the customer can reach out to management at {email}. Do not exceed 5 sentences. This is the topic: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[
            {"role": "user", "content": f"{prompt}{topics}"}
        ]
    )

    response = str(response['choices'][0]['message']['content'])

    return response