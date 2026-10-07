from engine import ask


question = "What is agriculture?"


result = ask(question)


print()
print("================================")
print("ANSWER")
print("================================")

print(result["answer"])


print()
print("================================")
print("SOURCES")
print("================================")

for source in result["sources"]:
    print("-", source)
