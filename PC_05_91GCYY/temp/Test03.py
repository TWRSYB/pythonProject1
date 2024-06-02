from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.temp.Test01 import category_01
import Test02

print(Test02.category_01 == category_01)

category_03 = Category('111', 'aaa', 'aaa')

print(Test02.category_01 == category_03)
print(category_01 == category_03)