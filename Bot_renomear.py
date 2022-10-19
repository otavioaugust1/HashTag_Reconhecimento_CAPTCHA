import os

# Renaming all the files in the folder.
folder = (r"../HashTag_Reconhecimento_CAPTCHA/img/origem/")
i=0
for file_name in os.listdir(folder):
    i += 1
    old_name = folder + file_name
    new_name = folder + f'CAPTCHA_{i}_.png'
    os.rename(old_name, new_name)
print(os.listdir(folder))