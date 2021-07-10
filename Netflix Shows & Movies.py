#!/usr/bin/env python
# coding: utf-8

# # Complete Table

# In[7]:


import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import pandas as pd

df = pd.read_csv('netflix_titles.csv')

## add new features in the dataset
df["date_added"] = pd.to_datetime(df['date_added'])
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

df['season_count'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else "", axis = 1)
df['duration'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else "", axis = 1)

df.head()


# # Content Type on Netflix

# In[8]:


## Is Netflix has increasingly focusing on TV rather than movies in recent years

col = "type"
grouped = df[col].value_counts().reset_index() ## only movie and tv-shows
grouped = grouped.rename(columns = {col: "count", "index" : col})

grouped.head()

## plot
trace = go.Pie(labels=grouped[col],
               values = grouped['count'],
               pull = [0.05,0],
               marker = dict(colors = ["#6ad49b","#a678de"]))
layout = go.Layout(title = "", height = 400, legend = dict(x=0.1, y=1.1))
fig = go.Figure(data = [trace], layout = layout)
iplot(fig)


# As we can see, Netflix increasingly focusing on TV rather than movies in recent years

# # Growth in content over the years

# In[19]:


tv_table = df[df["type"] == "TV Show"] 
movie_table = df[df["type"] == "Movie"]

col = "year_added"

vc1 = tv_table[col].value_counts().reset_index()
vc1 = vc1.rename(columns = {col: "count", "index" : col})
vc1['percent'] = vc1['count'].apply(lambda x : 100*x/sum(vc1['count']))
vc1 = vc1.sort_values(col)

vc2 = movie_table[col].value_counts().reset_index()
vc2 = vc2.rename(columns = {col: "count", "index" : col})
vc2['percent'] = vc2['count'].apply(lambda x : 100*x/sum(vc2['count']))
vc2 = vc2.sort_values(col)

trace1 = go.Scatter(x=vc1[col], y=vc1["count"], name = "TV_Shows", marker = dict(color="#a678de"))
trace2 = go.Scatter(x=vc2[col], y=vc2["count"], name = "Movies", marker = dict(color="#6ad49b"))
data = [trace1,trace2]
layout = go.Layout(title = "Content added over the years", legend = dict(x=0.1,y=1.1,orientation="h"))
fig = go.Figure(data,layout)
fig = go.Figure(data, layout = layout)
fig.show()


# The growth in number of movies on netflix was much higher than the TV shows until 2019,and dramaticlly decreased probably due the 'corona-time'. 
# About 1300 new movies were added in both 2018 and 2019. The growth in content started from 2013.

# # TV Shows with many seasons

# In[34]:


col = "season_count"

vc1 = tv_table[col].value_counts().reset_index()
vc1 = vc1.rename(columns = {col: "count", "index" : col})
vc1['percent'] = vc1['count'].apply(lambda x : 100*x/sum(vc1['count']))
vc1 = vc1.sort_values(col) ##FROM SOME REASON DOESN'T SORTING PROPERLY!!

trace = go.Bar(x=vc1[col], y=vc1["count"], name = "TV_Shows", marker = dict(color="#a678de"))
data = [trace]
layout = go.Layout(title = "Seasons", legend = dict(x=0.1,y=1.1,orientation="h"))
fig = go.Figure(data,layout = layout)
fig.show()
vc1


# That way we can see most TV shows in netflix are more likely to end with one season

# # Rating

# In[56]:


col = "rating"

vc1 = tv_table[col].value_counts().reset_index()
vc1 = vc1.rename(columns = {col : "count", "index" : col})
vc1['percent'] = vc1['count'].apply(lambda x : 100*x/sum(vc1['count']))
vc1 = vc1.sort_values(col)

vc2 = movie_table[col].value_counts().reset_index()
vc2 = vc2.rename(columns = {col : "count", "index" : col})
vc2['percent'] = vc2['count'].apply(lambda x : 100*x/sum(vc2['count']))
vc2 = vc2.sort_values(col)

trace1 = go.Bar(x=vc1[col], y=vc1["count"], name = "TV_Shows", marker = dict(color="#a678de"))
trace2 = go.Bar(x=vc2[col], y=vc2["count"], name = "Movies", marker = dict(color="#6ad49b"))
data = [trace1,trace2]
layout = go.Layout(title = "Rating Content", legend = dict(x=0.1,y=1.1,orientation="h"))
fig = go.Figure(data,layout = layout)
fig.show()

vc2


# A content rating (also known as maturity rating) rates the suitability of TV broadcasts or movies to its audience,usually in order to show which age group is suitable for that content.
# As we can see, most of the the movies(1845 movies) and TV shows(1018) at netflix are under the "TV-MA" rating, which means the content is not suitable under the age 17. In contrast, the content that is suitable for children,in both cases(movies&serials), is much fewer.
# 

# # Top Categories

# In[68]:


from collections import Counter
col = "listed_in"

categories = ", ".join(movie_table['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
labels = [_[0] for _ in counter_list][::-1]
values = [_[1] for _ in counter_list][::-1]

trace = go.Bar(y=labels,x=values,orientation="h",
               name="Top Categories for both Movies & TV Shows",
               marker=dict(color="#a678de"))
data = [trace]
layout = go.Layout(title="Top Categories for both Movies & TV Shows in Netflix",
                  legend = dict(x=0.1,y=1.1,orientation="h"))
fig = go.Figure(data,layout=layout)
fig.show()

