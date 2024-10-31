vietnamese_food_chatbot/
│
├── api/
│   ├── __init__.py
│   ├── routes.py          # API endpoints
│   └── middleware.py      # API middleware
│
├── core/
│   ├── __init__.py
│   ├── ai_model.py        # AI model code
│   ├── chatbot.py         # Chatbot logic
│   ├── crawler.py         # Web crawler
│   └── database.py        # Database schema
│
├── data/
│   └── vietnam_food_data.json
│
├── models/
│   └── food_ai_model.pkl
│
├── logs/
│   ├── api.log
│   ├── crawler.log
│   └── training.log
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_chatbot.py
│
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker compose setup
└── README.md           # Project documentation 