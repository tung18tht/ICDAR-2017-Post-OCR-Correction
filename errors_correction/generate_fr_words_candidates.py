import os, linecache, re, operator, json

work_directory_path = os.path.dirname(os.path.realpath(__file__))
data_directory_path = work_directory_path + "/ICDAR2017_datasetPostOCR_Evaluation_2M_v1.2"

fr_words_file = open(work_directory_path + "/fr_words.txt", "rU", encoding="ISO-8859-1")
fr_words = set()
for word in fr_words_file:
  fr_words |= {word.rstrip()}

error_patterns_file = open(work_directory_path + "/error_patterns.txt", "rU")
error_patterns = list()
for error_pattern in error_patterns_file:
  error_patterns.append(error_pattern.rstrip().split(";"))

erroneous_tokens_pos_file = open(data_directory_path + "/erroneous_tokens_pos.json")
erroneous_tokens_pos = json.load(erroneous_tokens_pos_file)

output_file = open(work_directory_path + '/Results/result_fr_words.json', "w")
output_file.write("{")

for file in erroneous_tokens_pos:
  if file.find("fr") == -1:
    continue

  file_path = data_directory_path + "/" + file
  ocr_output = linecache.getline(file_path, 1)[14:].strip()

  print("Checking file: " + file + "... ", end='', flush=True)

  output_file.write('\n    "' + file + '": ')
  errors_to_output = {}

  for error in erroneous_tokens_pos[file]:
    results = {}

    number_of_tokens = int(error[error.find(":")+1:])
    if number_of_tokens != 1:
      error_begin_index = int(error[:error.find(":")])

      error_end_index = error_begin_index
      for i in range(number_of_tokens):
        error_end_index = ocr_output.find(" ", error_end_index + 1)

      results[ocr_output[error_begin_index:error_end_index].replace(" ", "")] = 1
    else:
      error_begin_index = int(error[:error.find(":")])
      error_end_index = ocr_output.find(" ", error_begin_index)
      if error_end_index != -1:
        token = ocr_output[error_begin_index:error_end_index]
      else:
        token = ocr_output[error_begin_index:]

      for i in range(len(token)):
        for error_pattern in error_patterns:
          flag = 0
          if (token[i:i+1] == error_pattern[0]):
            flag = 1
          elif (token[i:i+2] == error_pattern[0]):
            flag = 2
          elif (token[i:i+3] == error_pattern[0]):
            flag = 3
          
          if flag != 0:
            new_word = token[:i] + error_pattern[1] + token[i+flag:]
            if new_word in fr_words:
              results[new_word] = int(error_pattern[2])
    
    errors_to_output[error] = results

  output_file.write(json.dumps(errors_to_output, indent=8)+",")

  print("Done")

output_file.seek(0, 2)
output_file.truncate(output_file.tell() - 1)

output_file = open(work_directory_path + "/Results/result_fr_words.json", "a")
output_file.write("\n}")