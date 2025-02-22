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

def getOpenRouterResponse(quote):
    msg = '''
    Write a faceless Instagram Reel alpha male script under 30 seconds, formatted in JSON for Text-to-Speech (TTS) with timestamps. 
    The script should include a message with different frames (each with a text line, duration, and scene description in keywords). 
    The structure of the JSON should have a list of frames, 
    each with a 'frame' number, 'text' to be read, 'duration' for the TTS, and 'scene' describing the visuals of the scene in keywords.
    The script should be targetting to young audience.
    You can use below quote to make the script unique:
    ''' + quote
    completion = client.chat.completions.create(
    extra_body={},
    model="qwen/qwen2.5-vl-72b-instruct:free",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": msg
            }
        ]
        }
    ]
    )
    sendForAudioGeneration(convertToJson(completion.choices[0].message.content))
    return convertToJson(completion.choices[0].message.content)

def sendForAudioGeneration(response):
    finalMsg = ''
    for line in response['frames']:
        finalMsg = finalMsg + str(line['text'])
    print(finalMsg)
    getAudiobyLLM.convertToSpeech(finalMsg)
    return True
    
quote = "The first principle of success is desire."
print(json.dumps(getOpenRouterResponse(quote)))