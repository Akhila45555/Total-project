PROMPT_TEMPLATE = """
 You are a professional enterprise customer service assistant.
 Only answer using the context provided.

 Context:
 {context}

 User Question:
 {user_query}

 Answer:
 """

def compile_prompt(context, query):
 return PROMPT_TEMPLATE.format(
         context=context,
       user_query=query
    )
# context = "python is a programming language."
# query = "what is python"
# result = compile_prompt(context, query)
# print(result)



context = "sql is a database."
query = "what is sql"
result = compile_prompt(context, query)
print(result)
  