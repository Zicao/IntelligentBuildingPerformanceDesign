'''
Copyright 2018 Zhichao Tian, E-mail:tzchao123@qq.com

'''
from pyautocad import Autocad, APoint
acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print(acad.doc.Name)