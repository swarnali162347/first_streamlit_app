import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('  🥗  Kale, Spinach & Rocket Smoothie')
streamlit.text('  🐔  Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv ("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.

streamlit.dataframe (fruits_to_show)

#New section to display fruityvice api response

#streamlit.header("Fruityvice Fruit Advice!")
#try:
#  fruit_choice = streamlit.text_input('What fruit would you like information about?')
#  if not fruit_choice:
 #   streamlit.error("Please select a fruit to get information.")
 # else:
 #   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 #   streamlit.dataframe(fruityvice_normalized)
#streamlit.write('The user entered ', fruit_choice)

 #except URLError as e:
  #streamlit.error()

#create function
#below section from ln 45 to 59 re-written to replace ln 29-41
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#new section to display fruityvice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
     back_from_function = get_fruityvice_data(fruit_choice)
     streamlit.dataframe(back_from_function)
except URLError as e:
 streamlit.error()
#streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)


#re-written ln 64-69 in ln 73-85
streamlit.header("View Our Fruit List - Add your Favorites:")
#snowflake related functions
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
  return my_cur.fetchall()

#Add a button to load the fruits

if streamlit.button('Get Fruit List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 my_cnx.close()
 streamlit.dataframe(my_data_rows)

#streamlit.stop()
#fruit_choice = streamlit.text_input('What fruit would you like to add?','Kiwi')
#streamlit.write('Thanks for adding', fruit_choice)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")

#re-write ln 88-90

#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit + "')")
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 my_cnx.close()
 streamlit.text(back_from_function)
  




