# Tofu

# Personalized Landing Page Generator

## Overview
This system analyzes target company website content and uses large language models to generate highly personalized marketing landing pages. This system includes:
- /save_palybook: Save playbook data, crawl target company websites, and filter and summary the content on the website.
- /personalized: Generates personalized content and HTML pages based on previously saved playbook data and content summaries.

## 
### 1. What went well while building this project? Is there anything you're particularly proud of?
-  **Fully Asynchronous Architecture**：Utilizes Python's async features for high-performance I/O processing, supporting concurrent processing of multiple target companies
-  **Rate Limiting**：API call control to avoid triggering LLM rate limits
-  **Resource Safety Management**：Uses context managers to ensure proper releasing of resources
-  **Key Content Extraction**： Focused scraping of p and h tags for critical content and summary generation to prevent token limit overflows
-  **Modular Design**：Clear separation of components for data parsing, content scraping, and AI generation

### 2. What didn't go well and you would like to improve?
- **Content Quality Assessment**：acks a comprehensive quality evaluation system for generated content.
- **Retry Mechanism**：Some error handling isn't robust enough, particularly for LLM content generation and web scraping.
- **Web Crawler**：Difficulty scraping certain special webpages.

### 3. Is there anything that you would do if you were given more time?
- **Gather More Target Information**： Additional scraping of pages under navigation menus.
- **Implement Chunked Content Processing**: Use Map-Reduce strategy for handling extra-long content。
- **Robust Retry Mechanism**： Improved retry logic for LLM content generation and web scraping failures


## 4. How would you design the system to make it production ready?
 - **Distributed Task Queue**：Use Kafka or RabbitMQ for processing generation requests
 - **Browser Cluster**：Implement browserless.io or Playwright cluster (for crawler optimization)
 - **Cache Management**：Configure proper expiration policies in Redis

## 5. Do you have suggestions on how this part of Tofu user experience could be better?
- Allow users to guide content generation direction or provide feedback on results
- Version management: Automatic snapshots 
- Streaming responses with real-time previews
- Add Visual Element Replacement: Support personalized replacement of images/logos


