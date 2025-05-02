import streamlit as st
import json
import os 
from custom_functions import group_people, populate_ppt_for_group, merge_slides,move_second_slide_to_last, remove_file, remove_directory, remove_merged

st.title("PowerPoint Generator")

# Folder to save uploaded files 
Save_directory = "uploads" 

# Create the folder if it doesn't exist
os.makedirs(Save_directory, exist_ok=True)

#for the upload file text 
st.markdown("""
<style>
    .stFileUploader label {
            color: #1E90FF;}
</style>           
""", unsafe_allow_html= True)

# File uploader
cover_page = st.file_uploader("Upload the cover page template")
table_page = st.file_uploader("Upload the table page template")
user_input = st.text_area("Paste your data in JSON format here")
date = st.text_input("Enter your preferred reporting date")


if cover_page:
    # Build the full path to save the file
    save_path = os.path.join(Save_directory, cover_page.name)

    # Write the file to disk
    with open(save_path, "wb") as f:
        f.write(cover_page.getbuffer())

    st.success(f"{cover_page.name} has been saved")

if table_page:
    # Build the full path to save the file
    table_path = os.path.join(Save_directory, table_page.name)

    # Write the file to disk
    with open(table_path, "wb") as f:
        f.write(table_page.getbuffer())

    st.success(f"{table_page.name} has been saved")

#Convert User input into a list
if user_input:
    try:
        data_list = json.loads(user_input)  # Convert string to list of dicts
        # st.write("List of Dictionaries:")
        # st.json(data_list)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")

    # Path to the ppt template and variables
    template_path = Save_directory+"/"+table_page.name
    #st.write(template_path)
    filenames = [] 

    # Check if template exists
    if not os.path.exists(template_path):
        print(f"""Error: Template file not found at {template_path}
            Please create a PowerPoint template with a table and save it as 'TableTemp.pptx'
            or update the template_path variable with the correct path to your template. """)
            
    # Group people (max 3 per group)
    groups = group_people(data_list)

    # Populate ppt for each group
    for i, group in enumerate(groups, start=1):
        filename = populate_ppt_for_group(group, i, template_path, date)
        filenames.append(filename)

    # st.write("The group files created: ")
    # st.write(filenames)

    #the cover template path
    cover_path = Save_directory+"/"+cover_page.name
    merge_slides(filenames, cover_path)
    move_second_slide_to_last()


   # """ --- Making the file downloadable to the user --- """
    # Set the path to the file
    final_file_path = "Merged.pptx"

    # Open and read the file in binary mode
    with open(final_file_path, "rb") as file:
        file_data = file.read()

    # Create a download button
    st.download_button(
        label="Download Your Presentation",
        data=file_data,
        file_name="your_presentation.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

    #Remove the group files 
    remove_file(filenames)

    #Remove temporary storage 
    remove_directory(Save_directory)

    #Remove merged file
    remove_merged()