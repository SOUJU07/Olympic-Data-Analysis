import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://www.urbanriver.com/wp-content/uploads/2012/04/olympic-rings.gif')


user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.years_country_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Medal Tally')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally of ' + str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + selected_country + ' On ' + str(selected_year))
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    city = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    nation = df['region'].unique().shape[0]
    athletes = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event',
                                             'Medal'])['Name'].shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(city)
    with col3:
        st.header('Sports')
        st.title(sport)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(event)

    with col2:
        st.header('Nations')
        st.title(nation)

    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time=helper.data_over_time(df,"region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title('Participating Nations over Time')
    st.plotly_chart(fig)


    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title('Events over Time')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title('Athletes over Time')
    st.plotly_chart(fig)

    st.title('No. of Events every year (Every Sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successfull Athletes')
    sprt = df['Sport'].unique().tolist()
    sprt.sort()
    sprt.insert(0,'Overall')
    selected_sport=st.selectbox('Select a sport',sprt)
    most_success=helper.most_successfull(df,selected_sport)
    st.table(most_success)


if user_menu=='Country Wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()


    selected_region = st.sidebar.selectbox('Select a Country', country_list)
    selected_country=helper.country_wise_medal(df,selected_region)
    st.title(selected_region + " Medal Tally over the Year")
    fig = px.line(selected_country, x="Year", y="Medal")
    st.plotly_chart(fig)

    selected_country_medal=helper.country_wise_sport_medal(df,selected_region)
    st.title(selected_region + " excels in the following Sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(selected_country_medal,annot=True)
    st.pyplot(fig)

    selected_region_for_player=helper.most_successfull_player(df,selected_region)
    st.title("Top 10 Athletes of "+ selected_region)
    st.table(selected_region_for_player)

if user_menu=='Athlete Wise Analysis':
    temp_df = df.drop_duplicates(subset=['Name', 'Sex', 'Age', 'region', 'Height', 'Weight'])
    x1 = temp_df['Age'].dropna()
    x2 = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=900,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = df[df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
