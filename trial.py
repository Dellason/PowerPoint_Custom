#sample data 

[
  {
    "project": "AgentX",
    "name": "Nathan",
    "tasks": [
      "Compilation of tools in AgentX",
      "Building of new tools in AgentX",
      "Deployment of AgentX",
      "Adding of new tools in AgentX",
      "Connecting AgentX tools to Quest",
      "Update of tools in AgentX",
      "Fetching of flow URLs in Power Automate to AgentX",
      "Setting up single-user flow in AgentX"
    ],
    "support": ["John", "Matthew"],
    "risk": [
      "Quest API may be deprecated soon.",
      "Integration with new tools could take longer than expected."
    ],
    "status": "blue"
  },
  {
    "project": "Web Scrapper",
    "name": "Nathan",
    "tasks": [
      "Enhancing dynamic scraper for single-page scraping use"
    ],
    "support": ["Mike"],
    "risk": [
      "Limited test cases; could break on new websites.",
      "Scraper might not scale with large data sets."
    ],
    "status": "orange"
  },
  {
    "project": "AgentX",
    "name": "Richmond",
    "tasks": [
      "Developed entity extractor for AgentX",
      "Created analysis agent for AgentX",
      "Built email query flow for AgentX"
    ],
    "support": ["Jane", "Luke"],
    "risk": [
      "Dependencies on external APIs; may go down.",
      "Lack of documentation for some APIs could cause delays."
    ],
    "status": "green"
  },
  {
    "project": "Non AI services",
    "name": "Mike",
    "tasks": [
      "Developed an entity extractor flow",
      "Created an analysis agent for AgentX",
      "Built email query flow"
    ],
    "support": ["Richmond"],
    "risk": [
      "Lack of clarity on future updates.",
      "Uncertainty around resource allocation for new features."
    ],
    "status": "blue"
  },
  {
    "project": "Python Scripts",
    "name": "Luke",
    "tasks": [
      "Developed Python scripts for data extraction",
      "Created data pipeline automation"
    ],
    "support": ["Matthew", "Jane"],
    "risk": [
      "Server instability could disrupt automation.",
      "Dependencies on specific Python packages that may be deprecated."
    ],
    "status": "red"
  }
]










""""This is what I am thinking
1. we populate the table group by group so to do for multiple groups 
2. we have to loop through with the function call 
3. so waht is we create an empty list that will keep appending the file name yeah 
4. something like 
5. filenames[]
6. filenames.append(function call)
7. ideally i believe when we print the list it should give us all the filenames 

so then idk but I think there should be a way that i can paste those 
8. function that will take the main template file, the group's filename and a number of the group number plus two, 
hopefully for the slide position to put it idk 
9. this function too will have to be looped when it is called to work for all the presention slides one by one 

this is not working how I envisioned it so I made a few changes and it works perfectly 
now what i have t do it make sure the slides are before the last slide 

so ideally if that will work 
10. after save the file under a different name so our template is still not tampered with 


11. then we will delete all the group presentation files that were created 
so we don't have any problem when we are running a new session
after all this i will have to go though the code make the neccessary edits for a fastapi app 
12. input should be a list 
13. the rest will follow 
"""


""""
Per the new approach with streamlit I would have to make some changes to the functions 
In my main now the table template will be dynanic 

then the merge will now have to take an addition argument of the file path to the cover page

now i have to do some error handling
the cover page template but be exactly 2 pages 
and the table template must be one page and must have a table 
"""

""""
Have to add the other columns 

1. do the bullets for the tasks first 

2. input should have support as a list 
- risk and depencensies also a list 
- the RAG staus can red yellow green or blue 

3. depending on that i will automatically do the trend 

4. reporting time could be a different input on its own 

"""



# """ ----- The actual program ----- """
# def main(): # i will just make this function take a list for the fast api stuff
#     # Sample data
    # sample_people = [
    #     {"name": "Nathan", "project": "AgentX", "tasks": ["Task 1", "Task 2"]},
    #     {"name": "Richmond", "project": "AgentX", "tasks": ["Task 3"]},
    #     {"name": "John", "project": "AgentX", "tasks": ["Task 4", "Task 5"]},
    #     {"name": "Jane", "project": "AgentX", "tasks": ["Task 6"]},
    #     {"name": "Mike", "project": "Non AI services", "tasks": ["Task 7"]},
    #     {"name": "Matthew", "project": "Set up tools", "tasks": ["Task 8"]},
    #     {"name": "Luke", "project": "Python Scripts", "tasks": ["Task 9", "Task 10"]},
    #     {"name": "Nathan", "project": "Web Scrapper", "tasks": ["Task 11"]}
    # ]
    
#     # Path to the ppt template and variables
#     template_path = "TableTemp.pptx"  #this will now be dynamic so i will save the file name they give 
#                                         #and before that the folder path will be contant because it will be fixed 
#     filenames = []

#     # Check if template exists
#     if not os.path.exists(template_path):
#         print(f"""Error: Template file not found at {template_path}
#             Please create a PowerPoint template with a table and save it as 'TableTemp.pptx'
#             or update the template_path variable with the correct path to your template. """)
#         return
    
#     # Group people (max 3 per group)
#     groups = group_people(sample_people)
    
#     # Populate ppt for each group
#     for i, group in enumerate(groups, start=1):
#         filenames.append(populate_ppt_for_group(group, i, template_path))
    
#     print(filenames)
#     merge_slides(filenames)
#     move_second_slide_to_last()
