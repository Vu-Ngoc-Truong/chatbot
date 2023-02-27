import langid
import time

text = "現代物理学の基礎を築いたのは誰か教えてください"
# time_now = time.
languages = ["ja", "en", "vi"]
langid.set_languages(languages)
# start_time = time.time()

# ranks = langid.rank(text)
# elapsed_time = time.time() - start_time
# print("Time1:", elapsed_time)
# print(ranks)

start_time = time.time()
language, confidence = langid.classify(text)
elapsed_time = time.time() - start_time
print("Time2:", elapsed_time)
print("Language: " + language)
print("Confidence: " + str(confidence))

# # Giới hạn số lượng ngôn ngữ sử dụng trong phân loại là 2
# language, confidence = langid.classify(text, top_n=2)

# print("Language: " + language)
# print("Confidence: " + str(confidence))