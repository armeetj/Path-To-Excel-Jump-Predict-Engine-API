# PathToExcel-AI-Project
## Author @xarmeetx 2019
## Contact
- Discord: [@xarmeetx#7768](https://discord.gg)
- Twitter: [@xarmeetx](https://twitter.com/xarmeetx)
- Email: xarmeetx@gmail.com

##### An engine that uses AI to predict the number of lessons a student must jump back. 
##### Based, on certain paramaters and the current lesson ID, the engine will return the final lesson ID

### Requests
```address/engine?lessonID=_&momentum=_&proficiency=_&difficulty=_&percent=_```
### Responses
```response will be a number, the ID of the lesson to jump to as a String```

## To Run
#### Install Libraries
```
pip install pathlib
pip install pandas
pip install numpy
pip install seaborn
pip install tensorflow
```

#### Run engine.py
```
python engine.py
```

#### Make sure...
- engine.py, IDBackMapping.csv, ConversionTable.csv, testData.csv, and trainData.csv are all in the same folder
- all above libraries are installed
- you are using pythong 3.7
