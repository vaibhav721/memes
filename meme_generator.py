import argparse as arg
import os
import random
import json
import sys
from formats.format1 import *
from formats.format2 import *
from formats.format3 import *
from preprocess import preprocessImages
import urllib.request
import logo

def use(formatObj):
    meme_img = formatObj.generate()
    meme_with_logo = add_logo(meme_img)
    meme_with_logo.save(meme_with_logo.filename)
    meme_with_logo.show()


def add_logo(img):
    img = add_logo_img(img, 'data/OpenGenus.png')
    img = add_logo_txt(img, 'OpenGenus')
    return img


def add_logo_img(meme_img, logo_img_path):
    logo_img = Image.open(logo_img_path)
    w, h = logo_img.size
    logo_img = logo_img.resize((int(w/2), int(h/2)), Image.ANTIALIAS)
    width, height = meme_img.size
    mbox = meme_img.getbbox()
    sbox = logo_img.getbbox()
    meme_logo = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    position = (mbox[2] - sbox[2] - 5, mbox[3] - sbox[3] - 30)
    meme_logo.paste(meme_img, (0, 0))
    meme_logo.paste(logo_img, position, mask=logo_img)
    meme_logo.filename = meme_img.filename[:-4]+'.png'
    return meme_logo


def add_logo_txt(meme_logo, txt):
    meme_logo_opengenus = Image.new('RGBA', meme_logo.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype('./impact/impact.ttf', 20)
    d = ImageDraw.Draw(meme_logo_opengenus)
    y = meme_logo.size[0] - 100
    x = meme_logo.size[1] - 35
    d.text((y, x), txt, font=fnt, fill=(255, 255, 255, 200))
    out_img = Image.alpha_composite(meme_logo, meme_logo_opengenus)
    out_img.filename = meme_logo.filename
    return out_img


def download(url, img_name):
    urllib.request.urlretrieve(url, img_name+".jpg")

# Generates random meme.

def random_meme(show='True'):
    with open('index.json') as f:
        data = json.load(f)
    num_of_images = len(data['data'])

    if show == 'True':
        random_idx = random.randint(1, num_of_images)
        folder = data['data'][random_idx]['location']
        Image.open(folder).show()
    else:
        print (data['data'][random.randint(1,
                           num_of_images)]['description'])



#checking argument
def checkarg(format,image1,text1,text2):#for mode=0 and format=1
    if format=='1':
        if image1 is None:
            print("Required parameters:- Image1,Text1,Text2")
            print("Image is missing!")
            return False
        if text1 is None and text2 is None:
            print("Required parameters:- Image1,Text1,Text2")
            print("Top and Bottom text are missing!")
            return False
        else:
            return True

def checkarg(format,image1,image2,text1,text2):#for mode=0 and format=2&3
    flag=1
    if format=='2' or format=='3':
        if image1 is None:
            print("Image 1 is missing!")
            flag=0
        if image2 is None:
            print("Image 2 is missing!")
            flag=0
        if text1 is None :
            print("Top text is missing!")
            flag=0
        if text2 is None :
            print("Bottom text is missing!")
            flag=0
        if flag==0:
            return False
        else:
            return True

# Main Function

def start(args):
    formatObj = None
    if args.mode == '0':
        if checkarg(args.format) is False:
		sys.exit()
	if args.format == '0':
            if args.random == 'True' or args.random == 'False':
                random_meme(args.random)
            else:
                print ('Empty or invalid arguments')

        if args.format == '1':
	    if checkarg(args.format,args.image1,args.text1,args.text2) is False:
                sys.exit()
            if args.text1 and args.text2 and args.image1:
                preprocessImages(args.image1)
                formatObj = Format1(image_path=args.image1,
									top_text=args.text1,
									bottom_text=args.text2)
                use(formatObj)

            elif args.text1 and args.image1:
                preprocessImages(args.image1)
                formatObj = Format1(image_path=args.image1,
									top_text=args.text1,
                                    bottom_text=None)
                use(formatObj)

            elif args.text2 and args.image1:
                preprocessImages(args.image1)
                formatObj = Format1(image_path=args.image1,
									top_text=None,
									bottom_text=args.text2)
                use(formatObj)

        if args.format == '2':
		if checkarg(args.format,args.image1,args.image2,args.text1,args.text2) is False:
                sys.exit()
                preprocessImages(args.image1)
                preprocessImages(args.image2)
                formatObj = Format2(args.image1, args.image2, args.text1, args.text2)
                use(formatObj)

        if args.format == '3':
		if checkarg(args.format,args.image1,args.image2,args.text1,args.text2) is False:
                sys.exit()
                text_top = args.text1.split(',')
                text_bottom = args.text2.split(',')
                if text_top.__len__() > 2 or text_bottom.__len__() > 2:
                    print("Too many arguements")
                else:
                    preprocessImages(args.image1)
                    preprocessImages(args.image2)
                    formatObj = Format3(image1_path=args.image1,
										image2_path=args.image2,
										top_text=text_top,
										bottom_text=text_bottom)
                    use(formatObj)

    if args.mode == '1':
        logo.print_logo()
        if args.format is not None:
            format = args.format
        else:
            format = input('Enter the format type :')

        if format == '0':
            show = input('Generate random image? True/False:')
            random_meme(show)

        if format == '1':
            img = input('Enter the image path: ')
            print(format1type1, format1type2, format1type3)
            user_res = input('Select one of the formats (default : 1): ')
            if user_res == '1':
                preprocessImages(img)
                top_text = input('Input the top line here: ')
                formatObj = Format1(image_path=img,
									top_text=top_text)
            elif user_res == '2':
                preprocessImages(img)
                bottom_text = input('Input the bottom line here: ')
                formatObj = Format1(image_path=img,
									bottom_text= bottom_text)
            elif user_res == '3':
                preprocessImages(img)
                top_text = input('Input the top line here: ')
                bottom_text = input('Input the bottom line here: ')
                formatObj = Format1(image_path=img,
									top_text=top_text,
									bottom_text=bottom_text)
            use(formatObj)

        if format == '2':
            img1 = input('Enter image 1 path: ')
            img2 = input('Enter image 2 path: ')
            top_text = input('Input the top line here: ')
            bottom_text = input('Input the bottom line here: ')
            preprocessImages(img1)
            preprocessImages(img2)
            formatObj = Format2(img1, img2, top_text, bottom_text)
            use(formatObj)

        if format == '3':
            img1 = input('Enter image 1 path: ')
            img2 = input('Enter image 2 path: ')
            preprocessImages(img1)
            preprocessImages(img2)
            print(format3type1, format3type2, format3type3, format3type4)
            type = input('Select the layout of meme (default : 1): ')

            top_text = list()
            bottom_text = list()

            if type == '1' or type == '':
                text1 = input('Input the top spreading text: ')
                text2 = input('Input the bottom spreading text: ')
                top_text.append(text1)
                bottom_text.append(text2)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '2':
                text1 = input('Input the top spreading text: ')
                text2 = input('Input the line for first image: ')
                text3 = input('Input the line for second image: ')
                top_text.append(text1)
                bottom_text.append(text2)
                bottom_text.append(text3)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '3':
                text1 = input('Input the line for first image: ')
                text2 = input('Input the line for second image: ')
                text3 = input('Input the bottom spreading line: ')
                top_text.append(text1)
                top_text.append(text2)
                bottom_text.append(text3)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '4':
                text1 = input('Input the top line for first image: ')
                text2 = input('Input the top line for second image: ')
                text3 = input('Input the bottom line for first image: ')
                text4 = input('Input the bottom line for second image: ')
                top_text.append(text1)
                top_text.append(text2)
                bottom_text.append(text3)
                bottom_text.append(text4)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            use(formatObj)

    if args.mode == '2':
        if args.format is not None:
            format = args.format
        else:
            format = input('Enter the format type :')

        if format == '0':
            show = input('Generate random image? True/False:')
            random_meme(show)

        if format == '1':
            if args.url1 is not None:
                url = args.url1
            else:
                url = input('Enter image URL: ')
            download(url, 'meme_img')
            img = 'meme_img.jpg'
            print(format1type1, format1type2, format1type3)
            user_res = input('Select one of the formats (default : 1): ')
            if user_res == '1' or user_res == '':
                preprocessImages(img)
                top_text = input('Input the top line here: ')
                formatObj = Format1(image_path=img,
									top_text=top_text)
            elif user_res == '2':
                preprocessImages(img)
                bottom_text = input('Input the bottom line here: ')
                formatObj = Format1(image_path=img,
									bottom_text=top_text)
            elif user_res == '3':
                preprocessImages(img)
                top_text = input('Input the top line here: ')
                bottom_text = input('Input the bottom line here: ')
                formatObj = Format1(image_path=img,
									top_text=top_text,
									bottom_text=bottom_text)
            use(formatobj)

        if format == '2':
            if args.url1 is not None:
                url1 = args.url1
            else:
                url1 = input('Enter URL for first Image: ')
            if args.url2 is not None:
                url2 = args.url2
            else:
                url2 = input('Enter URL for second Image: ')
            download(url1, 'meme_img1')
            download(url2, 'meme_img2')
            img1 = 'meme_img1.jpg'
            img2 = 'meme_img2.jpg'
            top_text = input('Input the top line here: ')
            bottom_text = input('Input the bottom line here: ')
            preprocessImages(img1)
            preprocessImages(img2)
            formatObj = Format2(img1, img2, top_text, bottom_text)
            use(formatobj)

        if format == '3':
            if args.url1 is not None:
                url1 = args.url1
            else:
                url1 = input('Enter URL for first Image: ')
            if args.url2 is not None:
                url2 = args.url2
            else:
                url2 = input('Enter URL for second Image: ')
            download(url1, 'meme_img1')
            download(url2, 'meme_img2')
            img1 = 'meme_img1.jpg'
            img2 = 'meme_img2.jpg'

            print(format3type1, format3type2, format3type3, format3type4)
            type = input('Select the layout of meme (default : 1): ')

            top_text = list()
            bottom_text = list()

            if type == '1' or type == '':
                text1 = input('Input the top spreading text: ')
                text2 = input('Input the bottom spreading text: ')
                top_text.append(text1)
                bottom_text.append(text2)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '2':
                text1 = input('Input the top spreading text: ')
                text2 = input('Input the line for first image: ')
                text3 = input('Input the line for second image: ')
                top_text.append(text1)
                bottom_text.append(text2)
                bottom_text.append(text3)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '3':
                text1 = input('Input the line for first image: ')
                text2 = input('Input the line for second image: ')
                text3 = input('Input the bottom spreading line: ')
                top_text.append(text1)
                top_text.append(text2)
                bottom_text.append(text3)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            elif type == '4':
                text1 = input('Input the top line for first image: ')
                text2 = input('Input the top line for second image: ')
                text3 = input('Input the bottom line for first image: ')
                text4 = input('Input the bottom line for second image: ')
                top_text.append(text1)
                top_text.append(text2)
                bottom_text.append(text3)
                bottom_text.append(text4)
                formatObj = Format3(image1_path=img1,
									image2_path=img2,
									top_text=top_text,
									bottom_text=bottom_text)
            use(formatobj)
