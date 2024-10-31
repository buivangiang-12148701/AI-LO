from fastapi import FastAPI

app = FastAPI(
    title="Vietnamese Food Chatbot API",
    description="API for Vietnamese Food Chatbot with AI capabilities",
    version="1.0.0",
    contact={
        "name": "VG-PA",
        "email": "giangbv92@gmail.com",
        "url": "https://github.com/buivangiang-12148701"
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/buivangiang-12148701/vietnamese-food-chatbot/blob/main/LICENSE"
    }
) 