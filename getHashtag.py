from openai import OpenAI
import globalConfigs
import json
import getAudiobyLLM

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=globalConfigs.API_KEY,
)



def convertToJson(response):
    start_index = response.find('{')
    end_index = response.rfind('}') + 1
    json_string = response[start_index:end_index]
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def getOpenRouterResponse(script):
    msg = '''
    Return a json containing params: Video Title and Hashtags only for the script below:

    ''' + str(script)

    #msg = ''' Write a faceless Instagram Reel script under 30 seconds. You can use below quality to make the script more engaging :''' + quote

    completion = client.chat.completions.create(
        model="qwen/qwen2.5-vl-72b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": msg
            }
        ]
    )

    print(completion.choices[0].message.content)
    # sendForAudioGeneration(convertToJson(completion.choices[0].message.content))
    return convertToJson(completion.choices[0].message.content)
    