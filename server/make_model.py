import sys
if len(sys.argv) < 2:
    print("Please provide model name.")
    exit(-1)
model_name = sys.argv[1]

file_first = """from .core import Repository
from een.db.config import collection


class """+model_name+"""Repository(Repository):
    \"\"\"Provides interface for """+model_name+""" collection of database.\"\"\"

    def __init__(self, school):
        """+model_name.lower()+""" = collection(\""""+model_name.lower()+"""\", school)
        super().__init__("""+model_name.lower()+""")
"""

file_second = """

from een.db."""+model_name.lower()+""" import """+model_name+"""Repository
def """+model_name.lower()+"""(school):
    return """+model_name+"""Repository(school)"""



with open("een/db/"+model_name.lower()+".py", "w") as model_file:
    model_file.write(file_first)
with open("een/db/__init__.py", "a") as model_file:
    model_file.write(file_second)