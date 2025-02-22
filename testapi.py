from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_body={},
  model="qwen/qwen2.5-vl-72b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Write a faceless Instagram Reel script about motivation under 30 seconds, formatted in JSON for Text-to-Speech (TTS) with timestamps. The script should include a motivational message with different frames (each with a text line, duration, and scene description in keywords). The structure of the JSON should have a list of frames, each with a 'frame' number, 'text' to be read, 'duration' for the TTS, and 'scene' describing the visuals of the scene in keywords."
        }
      ]
    }
  ]
)
print(completion.choices[0].message.content)
