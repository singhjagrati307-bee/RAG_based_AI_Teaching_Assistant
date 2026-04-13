# 1)

import whisper
model = whisper.load_model("base")
print("Model loaded successfully!")
print("welcome whisper")


# convert the videos to mp3

#2)
import os
files = os.listdir(r"C:\Users\BIT\Desktop\Project 2\rag based ai\videos")
print(files)

#3)
import os
import re  ## here I used regex (regular expressions) is because your file names are not consistent and contain different patterns .
# like# Lecture 11 - Joyjeet Ghose_ Slotter and Planer.mp4"
# "Lecture 12 - Joyjeet Ghose_ Drilling (1).mp4"
# "Lecture 14 - Joyjeet Ghose_ Milling Part 2.mp4"
# "by Joyjeet Ghose (1).mp4"
# If you try to split by " " or "_", the position of "Lecture" or "(1)" changes in each filename, so normal string split won’t always give correct results.

files = os.listdir(r"C:\Users\BIT\Desktop\Project 2\rag based ai\videos")

for file in files:
    match = re.search(r"Lecture\s+(\d+)", file)
    if match:
        tutorial_number = match.group(1)
    else:
        tutorial_number = "N/A"
    print(file, " → Tutorial Number:", tutorial_number)
    

## 4)
import re
import os
import subprocess

files = os.listdir(r"C:\Users\BIT\Desktop\Project 2\rag based ai\videos")
for file in files:
    tutorial_number = file.split("Lecture\s+(\d+)")
    file_name = file.split(" | ")[0]
    print(tutorial_number, file_name)
    subprocess.run["ffmpeg", "i" , f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3"]
    
    
import os
import re
import subprocess

# folders
input_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\videos"
output_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\audios"

# list all files
files = os.listdir(input_folder)

for file in files:
    # find lecture number using regex
    match = re.search(r"Lecture\s+(\d+)", file)
    tutorial_number = match.group(1) if match else "NA"
    
    # remove extension from filename
    file_name = os.path.splitext(file)[0]
    
    print(tutorial_number, file_name)
    
    # create full paths
    input_path = os.path.join(input_folder, file)
    output_path = os.path.join(output_folder, f"{tutorial_number}_{file_name}.mp3")
    
    # run ffmpeg conversion command
    subprocess.run(["ffmpeg", "-i", input_path, output_path])
    
    
    
    