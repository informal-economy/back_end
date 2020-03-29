from recommender import recommender


userspecific_rec_csv="./lab4-recommender-systems/jabril-movie-ratings.csv"
NewJob=recommender(userspecific_rec_csv)  
print("This should be the answer for the best choice! You can change num_recs to get more choices!!")  
print(NewJob)