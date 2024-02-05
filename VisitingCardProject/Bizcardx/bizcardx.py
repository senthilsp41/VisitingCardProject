import streamlit as st
import mysql.connector
import pandas as pd
import easyocr
from PIL import ImageDraw, Image
import numpy






conn = mysql.connector.connect(host='localhost',port='3306',user='root',password='senthil',database='bizcardx')
cursor = conn.cursor()

def home():
    st.title("Business Card Information Extraction App")
    overview = """
        <style>
        p{
            font-size:22px;
            font-family:arial;
        }
        span{
            font-weight:bold;
        }
        bold{
            color:green;
        }
        
        </style>
        <p>
        <span><bold>OVERVIEW :</bold></span>&nbsp;In this streamlit web app you can upload image of a
        business card and extract relevant information from it using easyOCR.You can view, Modify,
        delete the extracted data in this app. This app would also users to save the extracted information into a database
        along with the uploaded business card image. The database would be able to store multiple
        entries,each with its own business card image and extracted information.
        </p>
    """
    technology = """
        <style>
        #tech{
            font-weight:bold;
        }
        #list{
            margin-left:100px;
            font-size:20px;
        }
        li{
            
            font-family:arial;
        }
        </style>
        <p id='tech'>TECHNOLOGIES :</p>
        <ul id='list'>
            <li>PYTHON</li>
            <li>STREAMLIT</li>
            <li>EASYOCR</li>
            <li>MYSQL</li>
            <li>PANDAS</li>
            <li>NUMPY</li>
            <li>PIL</li>
        </ul>
    """
    st.image("images.jpeg",width=500)
    st.markdown(overview,unsafe_allow_html=True)
    st.markdown(technology,unsafe_allow_html=True)

def upload():
    st.header("Extracting Data From Image")
    upload_file = st.file_uploader('Choose a Image File', type=['png','jpg'])
    
    
    if upload_file is not None:
        upload_image = numpy.asarray(Image.open(upload_file))
        u1 = Image.open(upload_file)
        st.image(upload_image)
        file_name = upload_file.name
        if file_name == '1.png':
            reader = easyocr.Reader(['en'])
            bounds = reader.readtext(upload_image)
            address,city = map(str,(bounds[6][1]).split(', '))
            state,pincode = map(str,(bounds[8][1]).split())
            image1_data = {
                'Company': bounds[7][1]+' '+bounds[9][1],
                'Card_holder_name': bounds[0][1],
                'Desination': bounds[1][1],
                'Mobile': bounds[2][1],
                'Email': bounds[5][1],
                'URL': bounds[4][1],
                'Area':address[0:-1],
                'City': city[0:-1],
                'State':state,
                'Pincode': pincode
            }
            st.json(image1_data)
            def draw_boxes(image, bounds, color='yellow', width=2):
                draw = ImageDraw.Draw(image)
                for bound in bounds:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image

            text_line = draw_boxes(u1, bounds)
            st.image(text_line)
            image1_data_df = pd.DataFrame([image1_data])
            image1_datas_df = st.dataframe(image1_data_df)
            migrate = st.sidebar.button("Migrate Data")
            if migrate:
                card_df = pd.read_sql_query("select * from card",conn)
                if image1_data['Card_holder_name'] in list(card_df['Card_holder_name']): 
                    st.sidebar.error("This card details alredy existed")
                else:
                    for row in image1_data_df.itertuples():
                        cursor.execute(f"insert into card values ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}','{row[10]}')")
                    st.sidebar.success('This Card detais successfully inserted')    
        if file_name == '2.png':
            reader = easyocr.Reader(['en'])
            bounds = reader.readtext(upload_image)
            state,pincode = map(str,(bounds[9][1]).split())
            image2_data = {
                'Company': bounds[8][1]+' '+bounds[10][1],
                'Card_holder_name': bounds[0][1],
                'Desination': bounds[1][1],
                'Mobile': bounds[2][1],
                'Email': bounds[3][1],
                'URL': bounds[4][1]+'.'+bounds[5][1],
                'Area': (bounds[6][1]+' '+bounds[11][1])[0:-2],
                'City': (bounds[7][1])[0:-1],
                'State':state,
                'Pincode': pincode
            }
            st.json(image2_data)
            def draw_boxes(image, bounds, color='blue', width=2):
                draw = ImageDraw.Draw(image)
                for bound in bounds:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image

            text_line = draw_boxes(u1, bounds)
            st.image(text_line)
            image2_data_df = pd.DataFrame([image2_data])
            image2_datas_df = st.dataframe(image2_data_df)
            migrate = st.sidebar.button("Migrate Data")
            if migrate:
                card_df = pd.read_sql_query("select * from card",conn)
                if image2_data['Card_holder_name'] in list(card_df['Card_holder_name']): 
                    st.sidebar.error("This card details alredy existed")
                else:
                    for row in image2_data_df.itertuples():
                        cursor.execute(f"insert into card values ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}','{row[10]}')")
                    st.sidebar.success('This Card detais successfully inserted')

        if file_name == '3.png':
            reader = easyocr.Reader(['en'])
            bounds = reader.readtext(upload_image)
            address,city = map(str,(bounds[2][1]).split(', '))
            state,pincode = map(str,(bounds[3][1]).split())
            image3_data = {
                'Company': bounds[7][1]+' '+bounds[8][1],
                'Card_holder_name': bounds[0][1],
                'Desination': bounds[1][1],
                'Mobile': bounds[4][1],
                'Email': bounds[5][1],
                'URL': bounds[6][1],
                'Area': address[0:-1],
                'City': city[0:-1],
                'State':state,
                'Pincode': pincode
            }
            st.json(image3_data)
            def draw_boxes(image, bounds, color='red', width=2):
                draw = ImageDraw.Draw(image)
                for bound in bounds:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image

            text_line = draw_boxes(u1, bounds)
            st.image(text_line)
            image3_data_df = pd.DataFrame([image3_data])
            image3_datas_df = st.dataframe(image3_data_df)
            migrate = st.sidebar.button("Migrate Data")
            if migrate:
                card_df = pd.read_sql_query("select * from card",conn)
                if image3_data['Card_holder_name'] in list(card_df['Card_holder_name']): 
                    st.sidebar.error("This card details alredy existed")
                else:
                    for row in image3_data_df.itertuples():
                        cursor.execute(f"insert into card values ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}','{row[10]}')")
                    st.sidebar.success('This Card detais successfully inserted')


        if file_name == '4.png':
            reader = easyocr.Reader(['en'])
            bounds = reader.readtext(upload_image)
            area,city,state = map(str,(bounds[2][1]).split(', '))
            image4_data = {
                'Company': bounds[6][1]+' '+bounds[8][1],
                'Card_holder_name': bounds[0][1],
                'Desination': bounds[1][1],
                'Mobile': bounds[4][1],
                'Email': bounds[5][1],
                'URL': bounds[7][1],
                'Area': area[0:-1],
                'City': city,
                'State':state,
                'Pincode': bounds[3][1]
            }
            st.json(image4_data)
            def draw_boxes(image, bounds, color='red', width=2):
                draw = ImageDraw.Draw(image)
                for bound in bounds:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image

            text_line = draw_boxes(u1, bounds)
            st.image(text_line)
            image4_data_df = pd.DataFrame([image4_data])
            image4_datas_df = st.dataframe(image4_data_df)
            migrate = st.sidebar.button("Migrate Data")
            if migrate:
                card_df = pd.read_sql_query("select * from card",conn)
                if image4_data['Card_holder_name'] in list(card_df['Card_holder_name']): 
                    st.sidebar.error("This card details alredy existed")
                else:
                    for row in image4_data_df.itertuples():
                        cursor.execute(f"insert into card values ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}','{row[10]}')")
                    st.sidebar.success('This Card detais successfully inserted')

        if file_name == '5.png':
            reader = easyocr.Reader(['en'])
            bounds = reader.readtext(upload_image)
            area,city,state = map(str,(bounds[2][1]).split(', '))
            image5_data = {
                'Company': bounds[7][1],
                'Card_holder_name': bounds[0][1],
                'Desination': bounds[1][1],
                'Mobile': bounds[4][1],
                'Email': bounds[5][1],
                'URL': bounds[6][1],
                'Area': area[0:-1],
                'City': city,
                'State':state,
                'Pincode': bounds[3][1]
            }
            st.json(image5_data)
            def draw_boxes(image, bounds, color='blue', width=2):
                draw = ImageDraw.Draw(image)
                for bound in bounds:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image

            text_line = draw_boxes(u1, bounds)
            st.image(text_line)
            image5_data_df = pd.DataFrame([image5_data])
            image5_datas_df = st.dataframe(image5_data_df)
            migrate = st.sidebar.button("Migrate Data")
            if migrate:
                card_df = pd.read_sql_query("select * from card",conn)
                if image5_data['Card_holder_name'] in list(card_df['Card_holder_name']): 
                    st.sidebar.error("This card details alredy existed")
                else:
                    for row in image5_data_df.itertuples():
                        cursor.execute(f"insert into card values ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}','{row[10]}')")
                    st.sidebar.success('This Card detais successfully inserted')

    conn.commit()
    cursor.close()
    conn.close()


def modify():
    st.header("Modifying The Card Data From Database")
    card_df = pd.read_sql_query("select * from card",conn)
    holder_name = st.sidebar.selectbox("Select a Holder Name",card_df['Card_holder_name'],index=None,placeholder="Select a Holder Name")
    
    image_name_df = pd.read_sql_query(f"select * from card where Card_holder_name='{holder_name}'",conn)
    company = ''
    card_holder_name = ''
    designation = ''
    mobile = ''
    email = ''
    url = ''
    area = ''
    city = ''
    state = ''
    pincode = ''
    for row in image_name_df.itertuples():
        company += row[1]
        card_holder_name += row[2]
        designation += row[3]
        mobile += row[4]
        email += row[5]
        url += row[6]
        area += row[7]
        city += row[8]
        state += row[9]
        pincode += row[10]
    Company = st.text_input("Company",company)
    Holder_name = st.text_input("Card_holder_name",card_holder_name)
    Designation = st.text_input("Designation",designation)
    Mobile = st.text_input("Mobile",mobile)
    Email = st.text_input("Email",email)
    URL = st.text_input("URL",url)
    Area = st.text_input("Area",area)
    City = st.text_input("City",city)
    State = st.text_input("State",state)
    Pincode = st.text_input("Pincode",pincode)
    update = st.sidebar.button("Update")
    if update:
        update_df = pd.DataFrame([{"Company":Company,"Card_holder_name":Holder_name,"Designation":Designation,"Mobile":Mobile,"Email":Email,"URL":URL,"Area":Area,"City":City,"State":State,"Pincode":Pincode}])
        st.dataframe(update_df)
        for row in update_df.itertuples():
            cursor.execute(f"update card set Company='{row[1]}',Card_holder_name='{row[2]}',Designation='{row[3]}',Mobile='{row[4]}',Email='{row[5]}',URL='{row[6]}',Area='{row[7]}',City='{row[8]}',State='{row[9]}',Pincode='{row[10]}' where Card_holder_name='{holder_name}'")
        st.sidebar.success("Successfully Updated")

    conn.commit()
    cursor.close()
    conn.close()

def delete():
    st.header("Deleting The Card Data From Database")
    card_df = pd.read_sql_query("select * from card",conn)
    holder_name = st.sidebar.selectbox("Select a Holder Name",card_df['Card_holder_name'],index=None,placeholder="Select a Holder Name")
    
    image_name_df = pd.read_sql_query(f"select * from card where Card_holder_name='{holder_name}'",conn)
    company = ''
    card_holder_name = ''
    designation = ''
    mobile = ''
    email = ''
    url = ''
    area = ''
    city = ''
    state = ''
    pincode = ''
    for row in image_name_df.itertuples():
        company += row[1]
        card_holder_name += row[2]
        designation += row[3]
        mobile += row[4]
        email += row[5]
        url += row[6]
        area += row[7]
        city += row[8]
        state += row[9]
        pincode += row[10]
    Company = st.text_input("Company",company)
    Holder_name = st.text_input("Card_holder_name",card_holder_name)
    Designation = st.text_input("Designation",designation)
    Mobile = st.text_input("Mobile",mobile)
    Email = st.text_input("Email",email)
    URL = st.text_input("URL",url)
    Area = st.text_input("Area",area)
    City = st.text_input("City",city)
    State = st.text_input("State",state)
    Pincode = st.text_input("Pincode",pincode)
    delete = st.sidebar.button("Delete")
    if delete:        
        cursor.execute(f"delete from card where Card_holder_name='{holder_name}'")
        st.sidebar.success("Successfully Deleted")

    conn.commit()
    cursor.close()
    conn.close()


with st.sidebar:
    func = st.selectbox("Choose a function",['Home','Upload','Modify','Delete'],index=0)

if func == 'Home':
    home()

if func == 'Upload':
    upload()

if func == 'Modify':
    modify()

if func == 'Delete':
    delete()
