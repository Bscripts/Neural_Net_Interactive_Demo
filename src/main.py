
import json
import os
import sys
from openai import OpenAI
from os.path import exists
import time
import pyttsx3
import eel
import tkinter
import pickle
import uuid
import dotenv
from dotenv import load_dotenv

load_dotenv()

# Initialize Eel with the folder containing the frontend
eel.init('components')

apiKey = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=apiKey)                                    # init openAI connection and key

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
        temperature        = 0.3,                                               # Entropy (between 0 and 1). ie likelihood of choosing a less common completion.
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

ai_instructions_user_trainingSim = {"role": "user", "content": """You, the AI, are going to help me simulate the process of training a GPT model. Specifically, you are going
                        to be creating a single binary criterea for foods to be 'tasty', and another single binary criteria for a food to be 'not tasty'. These
                        critera are going to be based on user input, in which up to three 'tasty' and three 'not tasty' foods will be given. The output format of your 
                        response will be:
                        [tasty boolean critera]$%&#$%&#[not tasty boolean critera]
                        The output must use be in this exact format and use the parsable string $%&#$%&# for this code to function. It will break if you include
                        anything more or less than this format. YOU MUST CREATE CRITERIA. You may not use negations like "sweet" and "not sweet", the criteria
                        should be different things to make it interesting for the user. Similarly, the criteria may not include words from the input foods.
                        
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
        temperature        = 0.3,                                               # Entropy (between 0 and 1). ie likelihood of choosing a less common completion.
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
        temperature        = 0.3,                                               # Entropy (between 0 and 1). ie likelihood of choosing a less common completion.
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

@eel.expose
def close_program():
    sys.exit(0)



# eel.start('trainingSim.html', size=(800, 600))
# eel.start('transformerSim.html', size=(800, 600))
# eel.start('gptSimUI.html', size=(800, 600))
# eel.start('thePlan.html', size=(800, 600))
# eel.start('whyCare.html', size=(800, 600))
# eel.start('takeaways.html', size=(800, 600))
eel.start('mainMenu.html', size=(800, 600))