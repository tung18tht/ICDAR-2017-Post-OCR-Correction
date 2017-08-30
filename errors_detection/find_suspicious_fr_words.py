import os, linecache, re, json

work_directory_path = os.path.dirname(os.path.realpath(__file__))

fr_words_file = open(work_directory_path + "/fr_words.txt", "rU", encoding="ISO-8859-1")
fr_words = set()
for word in fr_words_file:
  fr_words |= {word.rstrip()}

data_directory_path = work_directory_path + "/ICDAR2017_datasetPostOCR_Evaluation_2M_v1.2"
fr_data_directory_paths = [data_directory_path + "/fr_monograph", data_directory_path + "/fr_periodical"]

output_file = open(work_directory_path + "/Results/result_fr_words.json", "w")
output_file.write("{")

for fr_data_directory_path in fr_data_directory_paths:
  for root_path, directories, files in os.walk(fr_data_directory_path):
    for file in files:
      if os.path.splitext(file)[1] == ".txt":
        output_file.write("\n    \""+os.path.basename(root_path)+"/"+file+"\": ")
        errors = {}
        file_path = root_path + "/" + file
        ocr_output = linecache.getline(file_path, 1)[14:].strip()

        word_begin_index = 0

        for i, character in enumerate(ocr_output):
          if character == ' ':
            word_end_index = i

            token = ocr_output[word_begin_index:word_end_index]

            apostrophe_pos = token.find("'")
            if apostrophe_pos != -1:
              # article = token[:apostrophe_pos]
              word = token[apostrophe_pos+1:]
            else:
              word = token

            clean_word = re.sub("\W+", '', word.lower()) ## TODO: handle "-" sign
            if clean_word not in fr_words:
              errors[str(word_begin_index)+":1"] = {}

            word_begin_index = word_end_index + 1
            
        token = ocr_output[word_begin_index:]

        apostrophe_pos = token.find("'")
        if apostrophe_pos != -1:
          word = token[apostrophe_pos+1:]
        else:
          word = token

        clean_word = re.sub("\W+", '', word.lower())
        if clean_word not in fr_words:
          errors[str(word_begin_index)+":1"] = {}

        output_file.write(json.dumps(errors, indent=8)+",")

output_file.seek(0, 2)
output_file.truncate(output_file.tell() - 1)

output_file = open(work_directory_path + "/Results/result_fr_words.json", "a")
output_file.write("\n}")