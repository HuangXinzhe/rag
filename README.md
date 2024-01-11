# rag
## 项目背景
基于LangChain的RAG 
1. 将作为知识的文本预处理并embedding存入chroma向量数据库中（create_db.py）
2. 将待问句进行embedding在chroma向量数据库中进行相似度匹配
3. 将匹配到的文本通过大模型进行问答(web_demo.py)  

LLM.py为加载大模型的文件，可选用所有支持LangChain的大模型
## 安装
项目所需环境：
```
pip install -r requirements.txt
```
## 使用
1. 在create_db.py中修改作为知识文件的目标文件夹及所需的embedding模型，根据需要修改向量数据库地址
2. 修改LLM.py中所需的大模型
3. 修改embedding模型，问答大模型和向量数据库地址，根据需要需要修改提示词及可视化web相关的页面显示信息


