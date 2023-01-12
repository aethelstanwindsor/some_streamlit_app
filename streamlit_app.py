from urllib.error import URLError
import requests
import streamlit
import pandas
import snowflake.connector
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


try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('Please make sure you enter an actual name')
  else:
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice.lower()}")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.header('More detailed information about the selected food')
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error(e)
streamlit.write('The user entered ', fruit_choice)






my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
if streamlit.button(f'Get fruit list'):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST;")
    my_data_rows = my_cur.fetchall()
  streamlit.text("Hello from Snowflake, these fruits are in the table:")
  streamlit.dataframe(my_data_rows)

streamlit.header('Add a fruit to the list?')
extra_fruit = streamlit.text_input('Your text input', '')
streamlit.write(f'Use fruit to add is: {extra_fruit}')
if streamlit.button(f'insert new fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  sql = f"insert into fruit_load_list values ('{extra_fruit}');"
  streamlit.text(f'Running sql: {sql}')
  with my_cnx.cursor() as my_cur:
    my_cur.execute(sql)
  streamlit.text(f'{extra_fruit} has been added')
