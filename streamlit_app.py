
import requests
import streamlit
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title('My super awesome diner website thing')
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header("Fruityvice Fruit Advice!")



streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

fruits_selected = streamlit.multiselect(f'pick some fruit', list(my_fruit_list.index), [my_fruit_list.index[4], my_fruit_list.index[8]])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.header('🥣🐔Build your own fruit smoothie🥑🥗')
streamlit.dataframe(fruits_to_show)

results = None
for target_fruit in fruits_to_show:
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{target_fruit.lower()}")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  if results is None:
    results = [fruityvice_normalized]
  else:
    results.append(fruityvice_normalized)

streamlit.header('More detailed informatoin about the selected foods')
df_results = pandas.concat(results)
streamlit.dataframe(df_results)
