from llama_cpp import Llama
llm = Llama(
      model_path="/tmp/model.gguf",
      chat_format="llama-2"
)
response =  llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are an assistant who always responds in json without any extra message. Json format includes array of scene and monlogoue only"},
          {
              "role": "user",
              "content": "Write a reel script about motivation for instagram"
          }
      ]
)

print(response["choices"][0])
