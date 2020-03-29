import lenskit.datasets as ds
import pandas as pd
import csv
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser


#The function input x is the user specific input .csv file that has the columns: 
#item,title,genres,ratings
#which is equivalent to 
#jobId,jobtitle,jobcategory,ratings


#The output of the function is a list of so far 20 records of the best job options 
#[genres, title], i.e. [category, job]

def recommender(x):
    data = ds.MovieLens('lab4-recommender-systems/')

    print("Successfully installed dataset.")

    rows_to_show = 10   # <-- Try changing this number to see more rows of data
    data.ratings.head(rows_to_show)  # <-- Try changing "ratings" to "movies", "tags", or "links" to see the kinds of data that's stored in the other MovieLens files

    print(data.ratings.head(rows_to_show))

    joined_data = data.ratings.join(data.movies['genres'], on='item')
    joined_data = joined_data.join(data.movies['title'], on='item')
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))


    #STEP 2.1

    average_ratings = (data.ratings).groupby(['item']).mean()
    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
    joined_data = joined_data.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[1:]]

    print("RECOMMENDED FOR ANYBODY:")
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))



    average_ratings = (data.ratings).groupby('item') \
       .agg(count=('user', 'size'), rating=('rating', 'mean')) \
       .reset_index()

    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
    joined_data = joined_data.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[1:]]


    print("RECOMMENDED FOR ANYBODY:")
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))


    #Step 2.2
    minimum_to_include = 1 #20<-- You can try changing this minimum to include movies rated by fewer or more people

    average_ratings = (data.ratings).groupby(['item']).mean()
    rating_counts = (data.ratings).groupby(['item']).count()
    average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include]
    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
    joined_data = joined_data.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[3:]]

    print("RECOMMENDED FOR ANYBODY:")
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))


    #Step 2.3
    average_ratings = (data.ratings).groupby(['item']).mean()
    rating_counts = (data.ratings).groupby(['item']).count()
    average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include]
    average_ratings = average_ratings.join(data.movies['genres'], on='item')
    average_ratings = average_ratings.loc[average_ratings['genres'].str.contains('Education')]

    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[3:]]
    print("\n\nRECOMMENDED FOR AN EDUCATION SPECIALIST:")
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))


    #Step 2.4
    average_ratings = (data.ratings).groupby(['item']).mean()
    rating_counts = (data.ratings).groupby(['item']).count()
    average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include]
    average_ratings = average_ratings.join(data.movies['genres'], on='item')
    average_ratings = average_ratings.loc[average_ratings['genres'].str.contains('sewing')]

    sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
    joined_data = sorted_avg_ratings.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[3:]]
    print("\n\nRECOMMENDED FOR A SEWING SPECIALIST:")
    joined_data.head(rows_to_show)
    print(joined_data.head(rows_to_show))


    #Step 3 Personalized Recommendation

    jabril_rating_dict = {}
    #jgb_rating_dict = {}

    with open(x, newline='') as csvfile:
        ratings_reader = csv.DictReader(csvfile)
        for row in ratings_reader:
            if ((row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6)):
                jabril_rating_dict.update({int(row['item']): float(row['ratings'])})
      
    #print("Jabril Dictionary")      
    #print(jabril_rating_dict)      
      
#    with open("./lab4-recommender-systems/jgb-movie-ratings.csv", newline='') as csvfile:
#        ratings_reader = csv.DictReader(csvfile)
#        for row in ratings_reader:
#            if ((row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6)):
#                jgb_rating_dict.update({int(row['item']): float(row['ratings'])})
     
    print("\n\nRating dictionaries assembled!")
    print("Sanity check:")
    print("\tJabril's rating for Banker is " + str(jabril_rating_dict[2]))
    #print("\tJohn-Green-Bot's rating for 1197 (The Princess Bride) is " + str(jgb_rating_dict[1197]))

    #Step 4 Train a new collaborative filtering model to provide recommendations.
    num_recs = 20  #<---- This is the number of recommendations to generate. You can change this if you want to see more recommendations

    user_user = UserUser(30, min_nbrs=2) #These two numbers set the minimum (3) and maximum (15) Niki:Now 4 number of neighbors to consider. These are considered "reasonable defaults," but you can experiment with others too
    algo = Recommender.adapt(user_user)
    print("algo")
    print(algo)
    algo.fit(data.ratings)
    print(algo.fit(data.ratings))

    print("Set up a User-User algorithm!")
    #Step 4.1 Now that the system has defined clusters, we can give it our personal ratings to get the top 10 recommended movies for me and for John-Green-bot!
    jabril_recs = algo.recommend(-1, num_recs, ratings=pd.Series(jabril_rating_dict))  #Here, -1 tells it that it's not an existing user in the set, that we're giving new ratings, while 10 is how many recommendations it should generate
    print("jabril_recs")
    print(jabril_recs)
    joined_data = jabril_recs.join(data.movies['genres'], on='item')      
    joined_data = joined_data.join(data.movies['title'], on='item')
    joined_data = joined_data[joined_data.columns[2:]]
    print("\n\nRECOMMENDED JOB FOR JABRIL:")
    #joined_data
    print(joined_data)
    
    return(joined_data)
    



    



#jgb_recs = algo.recommend(-1, num_recs, ratings=pd.Series(jgb_rating_dict))  #Here, -1 tells it that it's not an existing user in the set, that we're giving new ratings, while 10 is how many recommendations it should generate
#
#joined_data = jgb_recs.join(data.movies['genres'], on='item')      
#joined_data = joined_data.join(data.movies['title'], on='item')
#joined_data = joined_data[joined_data.columns[2:]]
#print("\n\nRECOMMENDED JOB FOR JOHN-GREEN-BOT:")
#joined_data
#print(joined_data)

##Step 5 Making a combined movie recommendation list. (Can be ommited??)
#combined_rating_dict = {}
#for k in jabril_rating_dict:
#  if k in jgb_rating_dict:
#    combined_rating_dict.update({k: float((jabril_rating_dict[k]+jgb_rating_dict[k])/2)})
#  else:
#    combined_rating_dict.update({k:jabril_rating_dict[k]})
#for k in jgb_rating_dict:
#   if k not in combined_rating_dict:
#      combined_rating_dict.update({k:jgb_rating_dict[k]})
#      
#print("Combined ratings dictionary assembled!")
#print("Sanity check:")
#print("\tCombined rating for 1197 (The Princess Bride) is " + str(combined_rating_dict[1197]))
#
#
##Step 5.2
#combined_recs = algo.recommend(-1, num_recs, ratings=pd.Series(combined_rating_dict))  #Here, -1 tells it that it's not an existing user in the set, that we're giving new ratings, while 10 is how many recommendations it should generate
#
#joined_data = combined_recs.join(data.movies['genres'], on='item')      
#joined_data = joined_data.join(data.movies['title'], on='item')
#joined_data = joined_data[joined_data.columns[2:]]
#print("\n\nRECOMMENDED FOR JABRIL / JOHN-GREEN-BOT HYBRID:")
#joined_data