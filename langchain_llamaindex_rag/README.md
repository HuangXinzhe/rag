# 使用LangChain和LlamaIndex从零构建PDF聊天机器人
具体步骤：
- 加载文档（PDF、HTML、文本、数据库等）
- 将数据分割成块，并对这些块建立embedding索引，这样方便使用向量检索工具进行语义搜索
- 对于每个问题，通过搜索索引和embedding数据来获取与问题相关的信息
- 将问题和相关数据输入到LLM模型中。在这个系列中使用OpenAI的LLM；

实现上述过程主要的两个框架，分别是：
- Langchain（https://python.langchain.com/en/latest/）
- LLamaIndex（https://gpt-index.readthedocs.io/en/latest/）