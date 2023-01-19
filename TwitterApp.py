#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import findspark


# In[ ]:


findspark.init('C:\spark')


# In[ ]:


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.functions import desc


# In[ ]:


sc = SparkContext()


# In[ ]:


ssc = StreamingContext(sc,10)
sqlContext =SparkSession.builder.appName('sc').getOrCreate() 


# In[ ]:


socket_stream = ssc.socketTextStream("FfarukK", 6666)


# In[ ]:


lines = socket_stream.window(20)


# In[ ]:


from collections import namedtuple
fields = ("tag", "count" )
Tweet = namedtuple( 'Tweet', fields )


# In[ ]:


( lines.flatMap( lambda text: text.split( " " ) ) 
  .filter( lambda word: word.lower().startswith("#") )
  .map( lambda word: ( word.lower(), 1 ) )
  .reduceByKey( lambda a, b: a + b ) 
  .map( lambda rec: Tweet( rec[0], rec[1] ) )
  .foreachRDD( lambda rdd: rdd.toDF().sort( desc("count") ) 
  .limit(10).createOrReplaceTempView("tweets") ) ) 


# In[ ]:


sqlContext


# In[ ]:


ssc.start()


# In[ ]:


import time
from IPython import display
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


count = 0
while count < 10:
    
    time.sleep( 3 )
    top_10_tweets = sqlContext.sql( 'Select tag, count from tweets' )
    top_10_tweets.show()
    top_10_df = top_10_tweets.toPandas()
    display.clear_output(wait=True)
    plt.figure( figsize = ( 10, 8 ) )
    sns.barplot( x="count", y="tag", data=top_10_df)
    plt.show()
    count = count + 1


# In[ ]:


scc.stop()

