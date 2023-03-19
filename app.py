from fastapi import FastAPI
from prompt import get_manager_response
from fake_database import fake_database
from review import ReviewAttr


# app = FastAPI()


# @app.post("/")
# async def review_response(review: Review):
#     company_details = fake_database[review.company_name]
#     if get_review_sentiment(review.review_text) <= company_details.negative_response_threshold:
#         response = get_manager_response(review.review_text, company_details)
#         return {"response": response, "status": 200}

def app():
    email = str(input("Enter manager's email: "))

    review = str(input("Enter review: "))

    review_attrs=review.ReviewAttr()
    sentiment_ovr = review_attrs.get_review_sentiment(review)

    if sentiment_ovr == "Positive":
        print("The review is positive, no further action is needed")
    elif sentiment_ovr == "Negative":
        topics = review_attrs.get_topics(review,'GPT')
        response = get_manager_response(topics, email)

        print(sentiment_ovr)
        print(topics)
        print(response)
    else:
        print("Review sentiment could not be determined. Please try again or ask the customer to be more specific with their complaint.")


if __name__ == "__main__":
    # from os import system
    # system("uvicorn main:app --host 0.0.0.0 --port 80")
    app()


