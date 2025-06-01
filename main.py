import getVideoIdea
import getLLMScript
import getAudiobyLLM
import createVideo
import getHashtag
import updateJson

videoIdea = getVideoIdea.get_object_by_index()

script = getLLMScript.getOpenRouterResponse(videoIdea)

updateJson.add_placeholder_entry(getHashtag.getOpenRouterResponse(script))

getAudiobyLLM.sendForAudioGeneration(script)