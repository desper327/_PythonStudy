from pymxs import runtime as rt

selected=rt.selection[0]
print(selected)
mat = selected.material

print(mat.name)

if hasattr(mat, 'getSubMaterials'):
    print("has sub materials")
else:
    print("no sub materials")