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

Once your environnement is correctly set up. You'll need to dowload a stopwords list from nltk. To do this, you need to do the following commands in your python environnement. 

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
