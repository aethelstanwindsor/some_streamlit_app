
import requests
import streamlit
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title('My super awesome diner website thing')
my_fruit_list = my_fruit_list.set_index('Fruit')


streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)



streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

fruits_selected = streamlit.multiselect(f'pick some fruit', list(my_fruit_list.index), [my_fruit_list.index[4], my_fruit_list.index[8]])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.header('🥣🐔Build your own fruit smoothie🥑🥗')
streamlit.dataframe(fruits_to_show)
