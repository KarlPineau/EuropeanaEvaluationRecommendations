from PIL import Image
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('thumbnails') if isfile(join('thumbnails', f))]
countFalse = 0
countCorrect = 0
countNotTouch = 0

for file in onlyfiles:
    try:
        print(file)
        url = "thumbnails/"+file
        foo = Image.open(url)
        print(foo.size)

        width = foo.size[0]
        height = foo.size[1]
        if width > 400 or height > 400:
            if width < height:
                foo = foo.resize((int(round((400*width)/height)), 400), Image.ANTIALIAS)
            elif height < width:
                foo = foo.resize((400, (int(round(400*height)/width))), Image.ANTIALIAS)
            elif height == width:
                foo = foo.resize((400, 400), Image.ANTIALIAS)
            foo.save(url, optimize=True, quality=95)
            countCorrect += 1
        else:
            countNotTouch += 1
    except OSError as e:
        print(e)
        countFalse += 1

print('Correct result : '+str(countCorrect))
print('Not Touch result : '+str(countNotTouch))
print('False result : '+str(countFalse))
