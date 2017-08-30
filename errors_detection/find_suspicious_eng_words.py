import os, linecache, re, json

work_directory_path = os.path.dirname(os.path.realpath(__file__))

eng_words_file = open(work_directory_path + "/eng_words.txt", "rU")
eng_words = set()
for word in eng_words_file:
  eng_words |= {word.rstrip()}

data_directory_path = work_directory_path + "/ICDAR2017_datasetPostOCR_Evaluation_2M_v1.2"
eng_data_directory_paths = [data_directory_path + "/eng_monograph", data_directory_path + "/eng_periodical"]

output_file = open(work_directory_path + "/Results/result_eng_words.json", "w")
output_file.write("{")

for eng_data_directory_path in eng_data_directory_paths:
  for root_path, directories, files in os.walk(eng_data_directory_path):
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

            clean_word = re.sub('\W+', '', ocr_output[word_begin_index:word_end_index].lower())
            if clean_word not in eng_words:
              errors[str(word_begin_index)+":1"] = {}

            word_begin_index = word_end_index + 1

        clean_word = re.sub('\W+', '', ocr_output[word_begin_index:].lower())
        if clean_word not in eng_words:
          errors[str(word_begin_index)+":1"] = {}

        output_file.write(json.dumps(errors, indent=8)+",")

output_file.seek(0, 2)
output_file.truncate(output_file.tell() - 1)

output_file = open(work_directory_path + "/Results/result_eng_words.json", "a")
output_file.write("\n}")