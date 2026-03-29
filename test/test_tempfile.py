import tempfile


with tempfile.TemporaryDirectory() as temp_dir:
    print(temp_dir)