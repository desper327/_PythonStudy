import pydantic
from pydantic import BaseModel, Field
print(pydantic.__file__)

class Person(BaseModel):
    name: str = Field(..., title="Name", description="Name of the person")
    age: int = Field(..., title="Age", description="Age of the person")

p = Person(name="Alice", age=25)
print(p.name)
print(p.age)
print(p)

print("-"*100, "\n\n\n")








from pydantic import BaseModel, ValidationError, Field

def demo_basic_model():
    # 定义一个用户模型（说明每个字段的“名字 + 类型 + 是否有默认值”）
    class User(BaseModel):
        id: int                      # 必填；若传 "1" 会自动转成数字 1
        name: str                    # 必填；若传 123 会被转成 "123"
        active: bool = True          # 选填；默认 True；"true"/"1"/1 → True
        score: float | None = None   # 可为浮点或 None；"9.5" 会自动转 9.5

    # 演示：杂乱字符串输入被转换成正确类型
    u = User(id="1", name="Alice", active="true", score="9.5")
    print("基础模型实例:", u)                      # 直接打印是简洁表示
    print("字典序列化:", u.model_dump())           # 转为普通 dict
    print("JSON 序列化:", u.model_dump_json())     # 转为 JSON 字符串

    try:
        # id="not_int" 无法转成 int；name=123 是合法（会转成 "123"），但前者已失败
        User(id="not_int", name=123)
    except ValidationError as e:
        # e.errors() 返回列表，每个元素含 loc(位置)/msg(解释)/type(错误类型)
        print("校验错误 messages:", e.errors())

#demo_basic_model()



from pydantic import BaseModel, Field, ValidationError

def demo_field_constraints():
    class Product(BaseModel):
        # ... 表示“这个字段必须传”
        name: str = Field(..., min_length=2, max_length=30, description="商品名称")
        price: float = Field(..., ge=0, le=9999.99, description="价格范围 0~9999.99")
        sku: str = Field(..., pattern=r"^[A-Z0-9]{6}$", description="6位大写字母或数字")
        stock: int = Field(0, ge=0)  # 不传默认为 0；不能为负数

    try:
        # 字符串 "4999" / "10" 会被自动转成数字
        p = Product(name="电脑", price="4999", sku="AB12C3", stock="10")
        print("合法商品:", p.model_dump())
    except ValidationError as e:
        print("错误:", e.errors())

    try:
        # name 太短；price 负数；sku 不符合大写 + 长度要求
        Product(name="X", price=-1, sku="abc123")
    except ValidationError as e:
        print("约束错误:", e.errors())

#demo_field_constraints()


# class exportFile(BaseModel):
    