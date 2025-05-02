import math
import os
from pptx import Presentation
import copy
import shutil
import time 
import threading
import io
from pptx.dml.color import RGBColor

""" ----- Group people in 3s ----- """
def group_people(people):
    max_group_size = 3
    total_people = len(people)
    num_groups = math.ceil(total_people / max_group_size)
    groups = []
    
    for i in range(num_groups):
        start_idx = i * max_group_size
        end_idx = min((i + 1) * max_group_size, total_people)
        groups.append(people[start_idx:end_idx])
    
    return groups


""" ----- Populate each group's PPT ----- """
def populate_ppt_for_group(group, group_number, template_path,date):
    prs = Presentation(f'{template_path}')
    table = None
   
    #Find table
    for slide in prs.slides:
        reporting_date_shape = None
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text.strip()
                if "Reporting Date" in text:
                    reporting_date_shape = shape
                    break

        if reporting_date_shape:
            text_frame = reporting_date_shape.text_frame
            paragraph = text_frame.paragraphs[0]

        # Get the first run (or create one if it doesn't exist)
        if not paragraph.runs:
            run = paragraph.add_run()
            run.text = "Reporting Date: " + date
        else:
            # Append the date to the existing text
            paragraph.runs[0].text += " " + date

        # Bold all runs (to make sure full text is bold)
        for run in paragraph.runs:
            run.font.bold = True
    else:
        print("Reporting date text field not found.")
        #table
        for shape in slide.shapes:
            if hasattr(shape, 'has_table') and shape.has_table:
                table = shape.table
                break
            if table:
                break
        
    if not table:
        return None

    # Fill in data rows, first row is a header
    for row_idx, person in enumerate(group, start=1):
        # Project
        cell = table.cell(row_idx, 0)
        cell.text = person["project"]
    
        # Lead 
        cell = table.cell(row_idx, 1)
        cell.text = person["name"]
        
        # Progress 
        cell = table.cell(row_idx, 2)
        cell.text = "\n".join(f"• {task}" for task in person["tasks"])

        # Support
        if "support" in person:
            cell = table.cell(row_idx, 3)
            cell.text = "\n".join(f"• {help}" for help in person["support"])

        # Risk and dependencies 
        if "risk" in person:
            cell = table.cell(row_idx, 4)
            cell.text = "\n".join(f"• {danger}" for danger in person["risk"])

        #RAG Status
        if "status" in person :
            #Blue
            if person["status".lower()] == 'blue':
                cell = table.cell(row_idx, 5)
                fill = cell.fill
                fill.solid()
                fill.fore_color.rgb = RGBColor(61, 152, 186)
                trend_cell = table.cell(row_idx,6)
                trend_cell.text = " <+>"

            #Green
            if person["status".lower()] == 'green':
                cell = table.cell(row_idx, 5)
                fill = cell.fill
                fill.solid()
                fill.fore_color.rgb = RGBColor(146, 208, 80)
                trend_cell = table.cell(row_idx,6)
                trend_cell.text = " <+>"

            #orange
            if person["status".lower()] == 'orange':
                cell = table.cell(row_idx, 5)
                fill = cell.fill
                fill.solid()
                fill.fore_color.rgb = RGBColor(255, 192, 0)
                trend_cell = table.cell(row_idx,6)
                trend_cell.text = " <_>"

            #red
            if person["status".lower()] == 'red':
                cell = table.cell(row_idx, 5)
                fill = cell.fill
                fill.solid()
                fill.fore_color.rgb = RGBColor(255, 0, 0)
                trend_cell = table.cell(row_idx,6)
                trend_cell.text = " <->"
            
        # Save ppt for that group
        filename = f"group_{group_number}_presentation.pptx"
        prs.save(filename)
        print(f"Created presentation: {filename}")
        
    return filename


""" ----- Just appened the group slides to the main PPT  ----- """
def merge_slides(filenames, cover_path):
    prs_main = Presentation(cover_path)
    for  filename in filenames:
        insert_prs = Presentation(f'{filename}')

        source_slide = insert_prs.slides[0]
        layout = prs_main.slide_layouts[6]
        new_slide = prs_main.slides.add_slide(layout)

        # Copy non image shapes because xml can't hangle images well 
        for shape in source_slide.shapes:
            if shape.shape_type != 13:
                new_slide.shapes._spTree.insert_element_before(copy.deepcopy(shape.element), 'p:extLst')
        
        # Copying images 
        for shape in source_slide.shapes:
            if shape.shape_type == 13:  # Picture
                if hasattr(shape, 'image'):
                    # Get image data
                    image_bytes = shape.image.blob
                    
                    # Save image dimensions and position
                    left = shape.left
                    top = shape.top
                    width = shape.width
                    height = shape.height
                    
                    # Add the image to the new slide
                    new_slide.shapes.add_picture(
                        io.BytesIO(image_bytes),
                        left, top, width, height
                    )

    prs_main.save('Merged.pptx')

""" ----- An orderly arrangement of the slides ----- """
def move_second_slide_to_last():
    prs_merge = Presentation('Merged.pptx')
    slides = prs_merge.slides
    
    # Get the second slide (index 1)
    second_slide = slides[1]
    
    # Move the second slide to the end by removing and re-adding it
    slide_layout = second_slide.slide_layout
    new_slide = slides.add_slide(slide_layout)
    
    # Copy content from the second slide to the new slide, non image
    for shape in second_slide.shapes:
        new_elm = shape.element
        new_slide.shapes._spTree.append(new_elm)
    
    # Copying images 
        for shape in second_slide.shapes:
            if shape.shape_type == 13:  # Picture
                if hasattr(shape, 'image'):
                    # Get image data
                    image_bytes = shape.image.blob
                    
                    # Save image dimensions and position
                    left = shape.left
                    top = shape.top
                    width = shape.width
                    height = shape.height
                    
                    # Add the image to the new slide
                    new_slide.shapes.add_picture(
                        io.BytesIO(image_bytes),
                        left, top, width, height
                    )
    
    # Delete the original second slide
    slides._sldIdLst.remove(slides._sldIdLst[1])

    return prs_merge.save('Merged.pptx')


"""" ----- Removing the all the files created ------"""
def remove_file (group_files):
    for group_file in group_files:
        os.remove(group_file)
    return ("Group files have been deleted")

""" ----- Removing the temporary storage -----"""
def remove_directory(foldername):
    if os.path.exists(foldername):
        shutil.rmtree(foldername)

""" ----- Removing the Merged file ------ """
def remove_merged():

    def delete():
        time.sleep(600)
        if os.path.exists("Merged.pptx"):
            os.remove("Merged.pptx")

    threading.Thread(target=delete).start()

