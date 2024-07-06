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

ai_instructions_user_trainingSim = {"role": "user", "content": """You, the AI, are going to help me simulate the process of training a GPT model. Specifically, you are going
                        to be creating a single binary criterea for foods to be 'tasty', and another single binary criteria for a food to be 'not tasty'. These
                        critera are going to be based on user input, in which up to three 'tasty' and three 'not tasty' foods will be given. The output format of your 
                        response will be:
                        [tasty boolean critera]$%&#$%&#[not tasty boolean critera]
                        The output must use be in this exact format and use the parsable string $%&#$%&# for this code to function. It will break if you include
                        anything more or less than this format. YOU MUST CREATE CRITERIA. SAYING ANYTHING TO THE EFFECT OF 'none' IS NOT ALLOWED
                        
                        Let us give it a try:
                        
                        Tasty Foods: Ice Cream, Steak, Pasta
                        Not Tasty Foods: Spinich, Seaweed, Expired Milk"""}

ai_instructions_assistant_trainingSim = {"role": "assistant", "content": """Lots of butter$%&#$%&#Chunky"""}


singleTokenPrompt_trainingSim = """Very good, here is the next one:

                    """

def createCriteria(tastyAndNotTasty):
  prompt = []
  prompt.append(ai_instructions_user_trainingSim)
  prompt.append(ai_instructions_assistant_trainingSim)
  newPrompt = singleTokenPrompt_trainingSim + tastyAndNotTasty
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
  parsedAnswer = parseAnswerTrainingSim(answer)
  return parsedAnswer

def parseAnswerTrainingSim(unparsedAnswer):
    parsedResult = unparsedAnswer.split("$%&#$%&#")
    storeAnswer(parsedResult)
    return parsedResult

def storeAnswer(parsedCritera):                                                  # Overwrites data in file so demo can be run more than once
    criteriaFile = open(criteriaPath,"w+")
    criteriaFile.write(parsedCritera[0] + "%$#%$#")
    criteriaFile.write(parsedCritera[1])
    criteriaFile.close()

eel.init('components')  

@eel.expose
def generateBinaryActivationFunctions(combinedFoods):
    print("Combined Foods received:", combinedFoods)
    foods = combinedFoods.split("#$@$#@")
    tastyCriteria = "Tasty Foods: "
    notTastyCriteria = "Not Tasty Foods: "
    for food in foods[:3]:
       tastyCriteria += food
    for food in foods[3:]:
       notTastyCriteria += food
    return createCriteria(tastyCriteria + " " + notTastyCriteria)

eel.start('trainingSim.html', size=(800, 600))

