import json
import os
from openai import OpenAI                                                                # OpenAI API
from os.path import exists
import time                                                                     # Delay function for failed API calls
import pyttsx3                                                                  # Text to Speech
import eel                                                                      # GUI using js and html
import tkinter
import pickle                                                                   # Python persistence
import uuid

client = OpenAI(api_key="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")                                    # init openAI connection and key

eel.init('components')                                                          # Load front end from folder 'components'

ai_instructions_user_gptSim = {"role": "user", "content": """You, the AI, are going to help me simulate the process a GPT model uses when generating text.
                        To do this, you will be fed the beginning of a piece of text, the generate four options for the next 'token', which is four
                        characters (single letter, punctuation mark, or space. Example: ace.). Then write a decimal number to two points
                        of precision to represent the chance of it being chosen. All four should add up to 1. These options should be separated with the string #$%&#$%& written 
                        exactly like that so I can parse the output. These tokens should not be continuations of one another, rather they
                        should be different options for the text completion. then, write another #$%&#$%& and then repeat a random one of the tokens, written exactly
                        like it was before without any extra characters (preserving spaces, you tend to forget to keep spaces that were at the beginning of the token, DO NOT
                        FORGET it messes up the program), loosly based on the chances represented by the decimal numbers. Do not say anything besides
                        replying in this exact format, as anything else will break this program.
                        
                        Let's give this a try.
                        
                        Today is a nice day, I think I will go for a"""}

ai_instructions_assistant_gptSim = {"role": "assistant", "content": """ wal 0.41#$%&#$%& hik 0.24#$%&#$%& run 0.22#$%&#$%& n i 0.13#$%&#$%& hik"""}


singleTokenPrompt_gptSim = """Very good, nice job recognizing there needed to be a space before 'wal', 'hik' and 'run'. I am going to reiterate an example because
                        you historically mess this up. If the token is ' wal', the last token chosen should be ' wal' NOT 'wal'. That said, DO NOT add spaces before
                        the token if it is not necessary.
                        
                        Here is the next one:

                    """

def simulateNextToken(sentenceSoFar):
  prompt = []
  prompt.append(ai_instructions_user_gptSim)
  prompt.append(ai_instructions_assistant_gptSim)
  newPrompt = singleTokenPrompt_gptSim + sentenceSoFar
  prompt.append({"role": "user", "content": newPrompt})
  worked = False
  maxFailures = 3
  while not worked:
    try:
        response = client.chat.completions.create(model = "gpt-4-0613",         # Specifies version of Chat GPT
        messages           = prompt,                                            # Takes in the past user and assistant messages and current query
        temperature        = 0.7,                                               # Entropy (between 0 and 1). ie likelihood of choosing a less common completion.
        max_tokens         = 50,                                               # Length of response desired. 1 token is about 4 chars
        # top_p              = 0.0,                                             # Depth of nucleus sampling (Between 0 and 1). ie cutoff % of words eligible for selection.
        # frequency_penalty  = 0.0,                                             # Penalizes usage of words in any prior query (from -2 (repetition) to 2 (all unique))
        # presence_penalty   = 0.0
        ) 
    except:
      print("Problem reaching OpenAI servers, trying again...")
      maxFailures -= 1
      print (maxFailures)
      #Testing output
      if maxFailures <= 0:
        print("failure, exiting program.")
        quit()
      time.sleep(3)
    else:
      worked = True
  answer = (response.choices[0].message.content)                     # Get text response from JSON object
  parsedAnswer = parseAnswerGPTSim(answer)
#   newSentenceSoFar = sentenceSoFar + parsedAnswer[4]
#   print(parsedAnswer)
  return parsedAnswer

def parseAnswerGPTSim(unparsedAnswer):
    parsedResult = unparsedAnswer.split("#$%&#$%&")
    return parsedResult

@eel.expose
def doFourSteps(inputSentence):
    print("Do four steps called")
    sentence = inputSentence
    for _ in range(4):
        result = simulateNextToken(sentence)
        print("Result from simulateNextToken:", result)
        eel.updateOptions(result[0], result[1], result[2], result[3])
        sentence += result[4]
        eel.updateSentence(sentence)
        time.sleep(4)

# # Start Eel with the provided front-end HTML
# eel.init('components')
# eel.start('gptSimUI.html', size=(800, 600))

