import os, linecache, operator

WORK_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIRECTORY_PATH = WORK_DIRECTORY_PATH + "/ICDAR2017_datasetPostOCR_Training_10M"

exception_characters = set()

def load_exception_characters():
  exception_characters_file = open(WORK_DIRECTORY_PATH + "/exception_characters.txt", "rU")
  global exception_characters
  for character in exception_characters_file:
    exception_characters |= {character.strip()}

def find_error_patterns():
  error_patterns = {}

  for root_path, directories, files in os.walk(DATA_DIRECTORY_PATH):
    for file in files:
      if is_txt_file(file):
        file_path = root_path + "/" + file
        ocr_aligned = linecache.getline(file_path, 2)[14:]
        gs_aligned = linecache.getline(file_path, 3)[14:]

        if is_not_aligned_correctly(ocr_aligned, gs_aligned):
          print("!!! File \"" + file_path + "\" OCR_aligned and GS_aligned are not aligned properly\n")
          continue

        for i in range(len(ocr_aligned)):
          if (gs_aligned[i] == "#"): continue
          if (gs_aligned[i] != ocr_aligned[i]) and (gs_aligned[i] != "@") and (ocr_aligned[i] != "@"):
            if gs_aligned[i] not in exception_characters:
              key = gs_aligned[i] + ";" + ocr_aligned[i]
              error_patterns[key] = error_patterns.get(key, 0) + 1

          if (gs_aligned[i+1:i+2] == "#"): continue
          if (gs_aligned[i] != ocr_aligned[i]) and (gs_aligned[i+1] != ocr_aligned[i+1]) \
          and ((gs_aligned[i:i+2]) != "@@") and ((ocr_aligned[i:i+2]) != "@@"):
            if (gs_aligned[i] not in exception_characters) and (gs_aligned[i+1] not in exception_characters):
              key = (gs_aligned[i:i+2]).replace("@", "") + ";" + (ocr_aligned[i:i+2]).replace("@", "")
              error_patterns[key] = error_patterns.get(key, 0) + 1

          if (gs_aligned[i+2:i+3] == "#"): continue
          if (gs_aligned[i] != ocr_aligned[i]) and (gs_aligned[i+1] != ocr_aligned[i+1]) and (gs_aligned[i+2] != ocr_aligned[i+2]) \
          and ((gs_aligned[i:i+3]) != "@@@") and ((ocr_aligned[i:i+3]) != "@@@"):
            if (gs_aligned[i] not in exception_characters) and (gs_aligned[i+1] not in exception_characters) and (gs_aligned[i+2] not in exception_characters):
              key = (gs_aligned[i:i+3]).replace("@", "") + ";" + (ocr_aligned[i:i+3]).replace("@", "")
              error_patterns[key] = error_patterns.get(key, 0) + 1

  return error_patterns

def is_txt_file(file):
  return os.path.splitext(file)[1] == ".txt"

def is_not_aligned_correctly(ocr_aligned, gs_aligned):
  return len(ocr_aligned) != len(gs_aligned)

def write_error_patterns_to_file(error_patterns):
  output_file = open(WORK_DIRECTORY_PATH + "/error_patterns.txt", "w")

  for error_pattern in sorted(error_patterns.items(), key=operator.itemgetter(1), reverse=True):
    output_file.write(error_pattern[0] + ";" + str(error_pattern[1]) + "\n")

if __name__ == '__main__':
  load_exception_characters()
  error_patterns = find_error_patterns()
  write_error_patterns_to_file(error_patterns)