import flask
import markdown
import os
from flask import Flask
from flask import request
from flask import Response
from flask import render_template


app = Flask(__name__)

@app.route("/")
def index():
    with open("C:\\Users\\singh\\Projects\\Path-To-Excel-Jump-Predict-Engine-API\\APIDocs.md", 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)

@app.route("/engine")
def engine():
    #0 = not a bad request
    #1 = bad request
    badRequest = 0;
    result = "default result";
    lessonID = 0;
    badRequest = 0;
    momentum = 0;
    proficiency = 0;
    difficulty = 0;
    percent = 0;

    if 'lessonID' in request.args:
        lessonID = request.args.get('lessonID');
    else:
        result = "please enter all the paramaters: see / for more info";
        badRequest = 1;

    if 'momentum' in request.args:
        momentum = request.args.get('momentum');
    else:
        result = "please enter all the paramaters: see / for more info";
        badRequest = 1;

    if 'proficiency' in request.args:
        proficiency = request.args.get('proficiency');
    else:
        result = "please enter all the paramaters: see / for more info";
        badRequest = 1;

    if 'difficulty' in request.args:
        difficulty = request.args.get('difficulty');
    else:
        result = "please enter all the paramaters: see / for more info";
        badRequest = 1;

    if 'percent' in request.args:
        percent = request.args.get('percent');
    else:
        result = "please enter all the paramaters: see / for more info";
        badRequest = 1;

    print("lessonID:", end = ' ');
    print(lessonID);
    print("momentum:", end = ' ');
    print(momentum);
    print("proficiency:", end = ' ');
    print(proficiency);
    print("difficulty:", end = ' ');
    print(difficulty);
    print("percent:", end = ' ');
    print(percent);

    if(badRequest == 0):
        print("passing params to tensorFlowEngine")
        result = tensorFlowEngine(lessonID, momentum, proficiency, difficulty, percent)

   


def tensorFlowEngine(lessonID, momentum, proficiency, difficulty, percent):
    inputString = lessonID + " " + momentum + " " + proficiency + " " + difficulty + " " + percent + " "
    print("inputString: " + inputString);
    parsedInput = inputString.split(" ");
    print("parsedInput: ")
    print(parsedInput)
    result = "not found"
    try:
        print("running returnNextLessonByID")
        result = returnNextLessonByID(parsedInput)[0];
        print('answer:', end = " ")
        print(result);
        print();
        return result;
    except:
        print("ERROR");
        return "ERROR";
    return result;


#================================================#
# author: xarmeetx (Armeet Singh Jatyani 2019)   #
#================================================#

'''
description: 
-------------------------------------------------------------------------------------------------------
This is a AI regression model. 

Input:
-------------------------------------------------------------------------------------------------------
Momentum, Proficiency, Difficulty, Percent

Output
-------------------------------------------------------------------------------------------------------
--> output of -x means the students jumps back x levels
--> output of 1 means the student progresses to the next level and has "mastered" 
    this concept
--> output of 0 means the student has to retry the excercise
'''



print("importing pandas")
import pandas as pd;
print("importing numpy")
import numpy as np;
print("importing tensorflow")
import tensorflow as tf;
print("importing keras from tensorflow")
from tensorflow import keras;
print("importing layers from tensorflow.keras")
from tensorflow.keras import layers;
print("importing EarlyStopping from tensorflow.keras.callbacks")
from tensorflow.keras.callbacks import EarlyStopping;

#constants
EPOCHS = 1000;

#just prints out the current version of tf
print("tf version: "+ tf.__version__);
print("Armeet Jatyani 2019\n");

#we are given the percent scored by the student and the number of levels we need to jump
input_column_names = ['Momentum','Proficiency','Difficulty', 'Percent','Jump'] ;
#define the path for the dataset

#reading using pandas
#pass the path and the names of the columns(the classification of the data)
trainData = pd.read_csv("trainData.csv", names=input_column_names, na_values = "?", comment='\t', sep=",", skipinitialspace=True);
# trainData = trainData.drop([0], axis=0);
testData = pd.read_csv("testData.csv", names=input_column_names, na_values = "?", comment='\t', sep=",", skipinitialspace=True);
# testData = testData.drop([0], axis=0);

#read the backmapping and conversiontable data
IDBackMapping = pd.read_csv("IDBackMapping.csv", names=['ID', 'Backmap ID'], na_values = "?", comment='\t', sep=",", skipinitialspace=True);
ConversionTable = pd.read_csv("ConversionTable.csv", names=['ID', 'Name'], na_values = "?", comment='\t', sep=",", skipinitialspace=True);

#read the training and testing inputs and targets from the csv files
trainInput = trainData.drop(columns = ['Jump']);
trainTarget = trainData.drop(columns = ['Momentum','Proficiency', 'Difficulty', 'Percent']);
testInput = testData.drop(columns = ['Jump']);
testTarget = testData.drop(columns = ['Momentum','Proficiency', 'Difficulty', 'Percent']);


IDNumpy = IDBackMapping.drop(columns = ['Backmap ID']).to_numpy();
BackmapIDNumpy = IDBackMapping.drop(columns = ['ID']).to_numpy();
ConversionTableNumpy = ConversionTable.drop(columns = ['ID']).to_numpy();
IDNumpy = np.delete(IDNumpy, 0);
BackmapIDNumpy = np.delete(BackmapIDNumpy, 0);
ConversionTableNumpy = np.delete(ConversionTableNumpy, 0);

#convert DataFrame to numpy arrays
trainInputNumpy = trainInput.to_numpy();
trainInputNumpy = np.delete(trainInputNumpy, 0, 0);
trainTargetNumpy = trainTarget.to_numpy();
trainTargetNumpy = np.delete(trainTargetNumpy, 0);
testInputNumpy = testInput.to_numpy();
testInputNumpy = np.delete(testInputNumpy, 0, 0);
testTargetNumpy = testTarget.to_numpy();
testTargetNumpy = np.delete(testTargetNumpy, 0);

#count the number of cols in the trainingInputData
n_cols = trainInput.shape[1];

print('training shape: ');
print(trainInput.shape);


#this function will build the model 
def build_model():
    #the keras model 
    model = keras.Sequential([
    #input layer (first layer)
    layers.Dense(100, activation=tf.nn.relu, input_shape=(n_cols, )),
    #middle/ "hidden" layers
    layers.Dense(100, activation=tf.nn.relu),
    #final layer (output layer)
    layers.Dense(1)
    ])
    
    #make the optimizer we will use
    optimizer = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False);
    #use the adam optimizer and mean squared error as the measure of model performance
    model.compile(optimizer = optimizer, loss = 'mean_squared_error');
    return model;

#make the model (call the method)
jump_predict_engine = build_model();
#print out the summary
jump_predict_engine;

#training the model
#5 parameters: training input, training targets, validation splits, # epochs, and callbacks
#set early stopping monitor so the model stops training when it won't improve anymore
early_stopping_monitor = EarlyStopping(patience=100);
#train model with fit()
jump_predict_engine.fit(trainInputNumpy, trainTargetNumpy, validation_split=0.1, epochs=EPOCHS, callbacks=[early_stopping_monitor]);

print('\nFINISHED TRAINING\n');

print("RUNNING TEST DATA");

enginePredictions = jump_predict_engine.predict(testInputNumpy);
roundedEnginePredictions = enginePredictions;

print('\nFINISHED RUNNING TEST DATA\n');

print('         input         | actual | engine | rounded');

i = 1
while i < enginePredictions.size:
    print(testInputNumpy[i], end = '     ');
    print(testTargetNumpy[i], end = '     ');
    print(enginePredictions[i][0], end = '     ');
    roundedEnginePredictions[i] = round(enginePredictions[i][0], 0);
    print(roundedEnginePredictions[i][0]);
    i = i + 1;

#================================================#
# author: xarmeetx (Armeet Singh Jatyani 2019)   #
#================================================#

'''
description: 
-------------------------------------------------------------------------------------------------------
method returnNextLessonByID: 
    -> Here we pass the ID of the excercise, the difficulty, and the score of the student.
    -> We return a tuple with format (id, name) which is the id and name of the next predicted lesson.

method returnNextLessonByName:
    -> Here we passe dhte Name of the excercise, the diffuculty, and the score of the student.
    -> We return a tuple with format (id, name) which is the id and name of the next predicted lesson.
'''

#return next lesson by the id of the excercise 
def returnNextLessonByID(parsedInput):
    #ID is the first argument
    ID = int(parsedInput[0]);
    
    #make the data to pass into the testing
    data = np.array([[parsedInput[1], parsedInput[2], parsedInput[3], parsedInput[4]]]);
    #make the prediction
    prediction = jump_predict_engine.predict(data); 
    
    #couunt is the prediction
    count = int(prediction[0][0]);
    print("Prediction: ", end = '');
    print(count);
    
    #we keep i so that we can keep track of how much we have jumped back
    i = 0;
    currentId = ID;
    currentName = '';
    print('Jumping: ')
    if count > 0: 
        currentName = (ConversionTableNumpy.item(currentId));
        return (ID + 1, currentName);
    elif count == 0: 
        currentName = (ConversionTableNumpy.item(currentId - 1));
        return (ID, currentName);
    elif count < 0:
        count = -count;
        while i < count:
            currentId = int(BackmapIDNumpy.item(currentId - 1));
            print(currentId);
            i = i + 1;
    currentName = (ConversionTableNumpy.item(currentId - 1));
    return (currentId, currentName);



#return the next lesson by the name of the excercise 
def returnNextLessonByName(parsedInput):
    #take the name of the lesson from the parsedInput and concatenate it all into one variable
    name = (parsedInput[0] + ' ' + parsedInput[1] + ' ' + parsedInput[2]);
    #find the id of this lesson
    ID = np.where(ConversionTableNumpy == name)[0][0] + 1;
    print(ID);
    #constructing input data for the keras net
    data = np.array([[parsedInput[3], parsedInput[4], parsedInput[5], parsedInput[6]]]);    
    
    #make the prediction
    prediction = jump_predict_engine.predict(data); 
    
    count = int(prediction[0][0]);
    print("Prediction: ", end = '');
    print(count);
    
    i = 0;
    currentId = ID;
    currentName = '';
    print('Jumping: ')
    if count > 0: 
        currentName = (ConversionTableNumpy.item(currentId));
        return (ID + 1, currentName);
    elif count == 0: 
        currentName = (ConversionTableNumpy.item(currentId - 1));
        return (ID, currentName);
    elif count < 0:
        count = -count;
        while i < count:
            currentId = int(BackmapIDNumpy.item(currentId - 1));
            print(currentId);
            i = i + 1;
    currentName = (ConversionTableNumpy.item(currentId - 1));
    return (currentId, currentName);

# the following lines are used to debug locally (will be commented out when hosting api)
""" while 0 == 0: 
    print("input: lesson ID, momentum, proficiency, difficulty, percent, jump")
    inputString = input();
    if inputString == '-1':
        break;
    parsedInput = inputString.split(" ");
    try:
        result = returnNextLessonByID(parsedInput);
        print('answer:', end = " ")
        print(result);
        print();
    except:
        print("ERROR"); """