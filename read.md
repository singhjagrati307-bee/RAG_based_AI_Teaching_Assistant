# how to use this RAG AI Teaching assistant on your own data.
## step1 - collect your videos
move all your video files to the videos folder 

## step2 - covert to mp3
convert all the video files to mp3 by running video_to_mp3

## step3 - convert mp3 to json
convert all the mp3 files to json by running mp3_to_json

## step4- convert the json files to vectors
use the file preprocess-json to convert the json file to a dataframe with embeddings and save as a joblib pickle 

## step5- Prompt generation and feeding to LLM

read the joblib file and load it into the memory. Then create a relevent prompt as per the user query and feed it to the LLM.




