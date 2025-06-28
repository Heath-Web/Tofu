LANDING_PAGE_FILE = "Tofu\\resources\\2022 CFO Recession Toolkit.html"
OUTPUT_FILE_PREFIX = "Tofu\\resources\\Personalized landing page - "

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("请先在环境变量中设置 OPENAI_API_KEY")