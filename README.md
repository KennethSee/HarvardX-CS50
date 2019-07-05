# HarvardX CS50: Introduction to Computer Science
This repository stores the code I wrote for all of CS50's problem sets.

# About CS50
This is an introductory to computer science course offered by Harvard University, primarily taught by Dr. David Malan. I took this course through EdX.

## My reasons for taking this course
I took this course to learn about computer science in a structured manner. While I had some prior experience with Python programming, I wanted to understand software and technology at a more fundamental level. This course was the first time I wrote code in C.

## Problem Sets

### 1. Hello
Basic problem to facilitate familiarity with C. Problem requires the program to prompt the user for a string, and print "hello [input]".

### 2. Mario
Program takes in an integer n from user input between 1 and 8, inclusive, and outputs the pyramid blocks found in the beginning of World 1-1 in Nintendo’s Super Mario Brothers. The pyramid blocks that are printed will be of height n.

### 3. Cash
Program asks the user for the amount of change owed and employs the greedy algorithm to determine the minimum number of coins that can be used to issue the change.

### 4. Caesar
This problem is an introduction to how programs can be used for cyptography. Program first takes in an integer x as a command-line argument from the user (i.e. ./caesar 3), and uses it as the key. It then takes in a string from the user, which would be the plaintext and outputs a ciphertext by shifting each character in the plaintext by the the number of the key.

Example:
./caesar 1
plaintext (input) - Hello, World
ciphertext (output) - Ifmmp, Xpsme

### 5. Vigenère
Similar to the Caesar problem, except that the program uses a sequence of keys. It takes in a string as a command-line argument instead of an integer. Each character in the string is then used to encrypt the plaintext sequentially and the key is reused until the plaintext has been fully encrypted.

### 6. Whodunit
The problem requires a program that modifies the color of the pixels in the picture file clue.bmp to make the message visible to the human eye. To test the program, compile the code and run ./whodunit clue.bmp verdict.bmp

### 7. Resize
Program takes in an integer n as the second command-line argument,the path of an input image file as the third command-line argument, and the name of the output image file as the third command-line argument. The ouput image file is the input image file expanded by a factor of n.

### 8. Recover
Program recovers JPEG images from raw file by scanning through each block of 512 bytes and writing the bytes to the relevant image files.

### 9. Speller
Program takes in a textfile and checks for mispelled word according to provided dictionary. If the dictionary file is not specified, *large* will be used by default.

### 10. Homepage
My first built website after being newly introduced to HTML, CSS, and JavaScript.

### 11. Bleep
Program takes in dictionary words from text file specified in command-line argument. It then prompts user for a message. Message will be printed, but any words contained the dictionary will be replaced by asterisks corresponding to the length of word.

### 12. Similarities
A web application built on HTML5, CSS, Python and Flask, that allows the user to upload two files and compare similarities by line, sentence, or substring. Similarities are highlighted in yellow.

### 13. Survey
A web application that takes in input from users, stores it in a csv file and outputs the csv contents as a table in a separate web page. Validation is performed on both the client and server side to ensure necessary fields are filled in during submission of form.
