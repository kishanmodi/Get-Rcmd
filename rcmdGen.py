from utils import create_sim


# recommendation function for movies
def getRecommedations(m):
    m = m.lower()
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    # searching movie name in datasets
    if m not in data['movie_title'].unique():
        return ('error')
    else:
        # getting index of movie in datasets
        i = data.loc[data['movie_title'] == m].index[0]
        lst = list(enumerate(sim[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        # getting top 10 most similar movies
        lst = lst[1:11]
        recommendList = []
        # getting movie names of top 10 most similar movies
        for i in range(len(lst)):
            a = lst[i][0]
            recommendList.append(data['movie_title'][a])
        # returning movie names of top 10 most similar movies
        return recommendList
