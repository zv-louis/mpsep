# mpsep - A MIME multipart text spritter.
------------------------------------------------------------

## Description

mpsep is simple python script for spriting a MIME multipart-text to the e-mail body text and the attached files.   

## Requirement

mpsep needs Python3 for running script.

## Usage

```
mpsep.py [-h] [-d DIRECTORY] [file]
```

Separate MIME multi-part text into its body text and the attached files.  
The decoded body-text is written to STDOUT. The attached files are restored as files.

- positional arguments:  
  * file  
      input file path.  
      if this is not fed, read text data from STDIN.


- optional arguments:  
  * -h, --help  
      show this help message and exit  

  * -d DIRECTORY, --directory DIRECTORY  
      A destination directory path of the attached files.  
      if the directory is not exist, make it.  
      if not fed, mpsep restore the attached files to current directory.


### example of usage

Using with openssl.  
When you decrypt and verify smime enveloped message, like smime.p7m, you'll get multiparted email text.  


```
openssl smime -decrypt -in smime.p7m -inform der -inkey [your private key] | \
openssl smime -verify -inkey [your private key] -noverify | \
mpsep.py -d [output directory for the attached files]
```



## Contribution

TBD

## Licence

[MIT](https://github.com/zv-louis/mpsep/blob/master/LICENSE)

## Author

[zv-louis](https://github.com/zv-louis)
