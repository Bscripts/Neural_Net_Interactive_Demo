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

criteriaPath = "data/foodCritera.txt"                                           # Create file to store generated criteria for later use
if exists(criteriaPath) == False:
      criteria = open(criteriaPath,"w+")
      criteria.close()

ai_instructions_user_transformerSim = {"role": "user", "content": """You, the AI, are going to help me simulate the process of training a GPT model. Specifically, you are going
                        to judge if a food is "tasty" based on the criteria passed to you. You are to return '1' if it is tasty or '0' if it is not tasty, verbatim. You must answer this way 
                        and this way only or the program will break.
                        
                        Let us give it a try:
                        
                        Tasty Criteria: Salty
                        Not Tasty Criterea: Squishy
                        Food To Evaluate: Gummy Worms"""}

ai_instructions_assistant_transformerSim = {"role": "assistant", "content": """0"""}


singleTokenPrompt_transformerSim = """Very good, here is the next one:

                    """

def tastyOrNot(tastyAndNotTasty):
  prompt = []
  prompt.append(ai_instructions_user_transformerSim)
  prompt.append(ai_instructions_assistant_transformerSim)
  newPrompt = singleTokenPrompt_transformerSim + tastyAndNotTasty
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
  print(answer)
  return answer

def parseCriteriaTransformerSim(toParse):
    criteriaArray = toParse.split("%$#%$#")
    return criteriaArray

eel.init('components')  

@eel.expose
def getFoodToEvaluate(inputString):
    print("Input String received:", inputString)
    criteriaFile = open(criteriaPath,"r")
    criteriaFileText = criteriaFile.read()
    criteriaFileArray = parseCriteriaTransformerSim(criteriaFileText)
    promptString = "Tasty: " + criteriaFileArray[0] + " "
    promptString += "Not Tasty: " + criteriaFileArray[1] + " "
    promptString += "Food to Evaluate: " + inputString
    criteriaFile.close()

    return tastyOrNot(promptString)

@eel.expose
def getTastyCriteria():
    criteriaFile = open(criteriaPath,"r")
    criteriaFileText = criteriaFile.read()
    criteriaFileArray = parseCriteriaTransformerSim(criteriaFileText)
    criteriaFile.close()
    return criteriaFileArray[0]

@eel.expose
def getNotTastyCriteria():
    criteriaFile = open(criteriaPath,"r")
    criteriaFileText = criteriaFile.read()
    criteriaFileArray = parseCriteriaTransformerSim(criteriaFileText)
    criteriaFile.close()
    return criteriaFileArray[1]

# eel.start('transformerSim.html', size=(800, 600))

