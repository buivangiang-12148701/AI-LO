vietnamese_food_chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── chat.py
│   │   │   │   │   ├── dishes.py
│   │   │   │   │   └── training.py
│   │   │   │   └── router.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── dish.py
│   │   │   ├── ingredient.py
│   │   │   └── recipe.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── dish.py
│   │   └── services/
│   │       ├���─ __init__.py
│   │       ├── chatbot.py
│   │       ├── crawler.py
│   │       └── ai_model.py
│   ├── data/
│   │   └── vietnam_food_data.json
│   ├── logs/
│   │   ├── api.log
│   │   ├── crawler.log
│   │   └── training.log
│   ├── models/
│   │   └── food_ai_model.pkl
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   │   ├── __init__.py
│   │   │   ├── test_chat.py
│   │   │   └── test_dishes.py
│   │   └── test_services/
│   │       ├── __init__.py
│   │       ├── test_chatbot.py
│   │       └── test_crawler.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── main.py 