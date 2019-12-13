# VI_project
Visualisation project where we show correlation between armed conflicts and the articles in the press.

Using this dataset [ucdp ged global](https://ucdp.uu.se/downloads/index.html#ged_global)

Using this js library [jvectormap](http://jvectormap.com) to display the world map.

Using this js library [wordcloud2](https://github.com/timdream/wordcloud2.js) to display word cloud.

# Installation 

To use our project, you need to install all the requirements by using the command :

` pip install -r requirements.txt`

Or you can use the Pipfile to deploy your virtual environnement by using the command :

` pipenv install `

You will need to put some data on the data folder to make the application work. You can then download the needed data with the following [link](https://drive.switch.ch/index.php/s/runMxGL0vUF7jZ4).

If the data is correctly downloaded put it in the data folder and go to the stopword list instruction.

Otherwise, if the above link isn't working, you can go download the dataset [ucdp ged global](https://ucdp.uu.se/downloads/index.html#ged_global) as an excel file and put it in a folder named `armed_conflict` in the data folder. You also need to create an empty folder `armed_conflict_pickle` next to the folder `armed_conflict`.

After your data folder is correctly set up with your the excel file. Run the init script : 
`python init_armed_conflict.py`. This script create the pickle file the backend need to use to making the application work.

Once your environnement is correctly set up and the data is correctly placed. You'll need to dowload a stopwords list from nltk. To do this, you need to do the following commands in your python environnement. 

```python
import nltk
nltk.downloads(‘stopwords’)
```

When the stopwords list is downloaded, you can run the flask server by running the script `run_server.py`. You can do this by running the following command :

`python run_server.py`

You should now could access our application on your browser at the following address : 

`http://127.0.0.1:5000/`

### Citations of the dataset

`Sundberg, Ralph, and Erik Melander, 2013, “Introducing the UCDP Georeferenced Event Dataset”, Journal of Peace Research, vol.50, no.4, 523-532`

`Högbladh Stina, 2019, “UCDP GED Codebook version 19.1”, Department of Peace and Conflict Research, Uppsala University`
