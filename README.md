# HarvardX CS50: Introduction to Computer Science
This repository stores the code I wrote for all of CS50's problem sets.

# About CS50
This is an introductory to computer science course offered by Harvard University, primarily taught by Dr. David Malan. I took this course through EdX.

## My reasons for taking this course
I took this course to learn about computer science in a structured manner. While I had some prior experience with Python programming, I wanted to understand software and technology at a more fundamental level. This course was the first time I wrote code in C.

## Problem Sets

### 1. [Hello](https://github.com/KennethSee/HarvardX-CS50/blob/master/1_hello.c)
Basic problem to facilitate familiarity with C. Problem requires the program to prompt the user for a string, and print "hello [input]".

### 2. [Mario](https://github.com/KennethSee/HarvardX-CS50/blob/master/2_mario.c)
Program takes in an integer n from user input between 1 and 8, inclusive, and outputs the pyramid blocks found in the beginning of World 1-1 in Nintendo’s Super Mario Brothers. The pyramid blocks that are printed will be of height n.

### 3. [Cash](https://github.com/KennethSee/HarvardX-CS50/blob/master/3_cash.c)
Program asks the user for the amount of change owed and employs the greedy algorithm to determine the minimum number of coins that can be used to issue the change.

### 4. [Caesar](https://github.com/KennethSee/HarvardX-CS50/blob/master/4_caesar.c)
This problem is an introduction to how programs can be used for cyptography. Program first takes in an integer x as a command-line argument from the user (i.e. ./caesar 3), and uses it as the key. It then takes in a string from the user, which would be the plaintext and outputs a ciphertext by shifting each character in the plaintext by the the number of the key.

Example:
./caesar 1
plaintext (input) - Hello, World
ciphertext (output) - Ifmmp, Xpsme

### 5. [Vigenère](https://github.com/KennethSee/HarvardX-CS50/blob/master/5_vigenere.c)
Similar to the Caesar problem, except that the program uses a sequence of keys. It takes in a string as a command-line argument instead of an integer. Each character in the string is then used to encrypt the plaintext sequentially and the key is reused until the plaintext has been fully encrypted.

### 6. [Whodunit](https://github.com/KennethSee/HarvardX-CS50/tree/master/6_whodunit)
The problem requires a program that modifies the color of the pixels in the picture file clue.bmp to make the message visible to the human eye. To test the program, compile the code and run ./whodunit clue.bmp verdict.bmp

### 7. [Resize](https://github.com/KennethSee/HarvardX-CS50/tree/master/7_resize)
Program takes in an integer n as the second command-line argument,the path of an input image file as the third command-line argument, and the name of the output image file as the third command-line argument. The ouput image file is the input image file expanded by a factor of n.

### 8. [Recover](https://github.com/KennethSee/HarvardX-CS50/tree/master/8_recover)
Program recovers JPEG images from raw file by scanning through each block of 512 bytes and writing the bytes to the relevant image files.

### 9. [Speller](https://github.com/KennethSee/HarvardX-CS50/tree/master/9_speller)
Program takes in a textfile and checks for mispelled word according to provided dictionary. If the dictionary file is not specified, *large* will be used by default.

### 10. [Homepage](https://github.com/KennethSee/HarvardX-CS50/tree/master/10_homepage)
My first built website after being newly introduced to HTML, CSS, and JavaScript.

### 11. [Bleep](https://github.com/KennethSee/HarvardX-CS50/blob/master/11_bleep.py)
Program takes in dictionary words from text file specified in command-line argument. It then prompts user for a message. Message will be printed, but any words contained the dictionary will be replaced by asterisks corresponding to the length of word.

### 12. [Similarities](https://github.com/KennethSee/HarvardX-CS50/tree/master/12_similarities)
A web application built on HTML5, CSS, Python and Flask, that allows the user to upload two files and compare similarities by line, sentence, or substring. Similarities are highlighted in yellow.

### 13. [Survey](https://github.com/KennethSee/HarvardX-CS50/tree/master/13_survey)
A web application that takes in input from users, stores it in a csv file and outputs the csv contents as a table in a separate web page. Validation is performed on both the client and server side to ensure necessary fields are filled in during submission of form.

### 14. [Finance](https://github.com/KennethSee/HarvardX-CS50/tree/master/14_finance)
A web application that allows a user to create a unique account to buy and sell stocks, and monitor the status of the user's portfolio. The frontend is powered by Bootstrap and JQuery which is connected to a server ran on Flask. Data is posted and pulled from a database hosted on sqlite. Stock prices are obtained via API calls from IEX Cloud.

Note: An IEX API key has to obtained through an IEX account and exported for the application to work.

export API_KEY=*api-key*
