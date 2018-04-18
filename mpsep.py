#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# MIME multi-pert text separator utility.
#

import os
import sys
import email
import errno
import mimetypes
import email.message
import email.charset

from argparse import ArgumentParser

# command help
cmd_description = """\
Separate MIME multi-part text into its body text and the attached files.
The decoded body-text is written to STDOUT. the attached files are restored to file. 
"""

# option help
directory_option_usage = """\
destination directory path of the attached files. if the directory is not exist, make it.
"""

# file usage.
file_parameter_usage = """\
input file path. if this is not fed, read text data from STDIN.
"""


# ----------------------------------------------------------------------
# write payload to file
def write_to_file(payload, dir_path, filename):

    # attachment file. write to file.
    attached_file_path = os.path.join(dir_path, filename)
    fp = open(attached_file_path, 'wb')
    with fp:
        fp.write(payload)
        # notify file has restored, using STDERR.
        sys.stderr.write("Decoded attachment file --> '{0}'\n".format(attached_file_path))
        sys.stderr.flush()


# ----------------------------------------------------------------------
# write payload to stdout
def write_to_stdout(payload, charset):

    raw_str = payload.decode(charset)
    sys.stdout.write(raw_str)
    sys.stdout.flush()


# ----------------------------------------------------------------------
# Parsing message
def parse_message(msg, dest_dir_path):

    # OS default charset
    # default_encoding = sys.getdefaultencoding()

    # count for the parts that is not having the filename or name.
    nameless_part_cnt = 0

    # enumerate multipart data
    for part in msg.walk():
        # multipart/* <-- just a container. skip.
        main_content_type = part.get_content_maintype()
        if main_content_type == 'multipart':
            continue

        # get filename.
        filename = part.get_filename()
        payload = part.get_payload(decode=True)
        if not filename:
            # nameless part.
            if nameless_part_cnt == 0:
                # first nameless part.
                # assume it as message-body.

                charset = part.get_content_charset()
                if not charset:
                    # RFC1341(MIME)
                    # treat it as 'ascii' by default charset.
                    charset = 'ascii'

                # write to STDOUT.
                write_to_stdout(payload, charset)
                # insert newline to stderr.
                # display main-body which does not end with a linebreak.
                sys.stderr.write('\n')

            else:
                # second or later.
                # write to file.
                guessed_extension = mimetypes.guess_extension(part.get_content_type())
                filename = 'nameless-part_{0:02d}{1}'.format(nameless_part_cnt, guessed_extension)
                write_to_file(payload, dest_dir_path, filename)

            # increment nameless part count.
            nameless_part_cnt += 1

        else:
            # attachment file. write to file.
            write_to_file(payload, dest_dir_path, filename)


# ----------------------------------------------------------------------
# script main
def script_main():
    parser = ArgumentParser(description=cmd_description)

    # set up arguments.
    parser.add_argument('-d',
                        '--directory',
                        type=str,
                        action='store',
                        help=directory_option_usage)
    parser.add_argument('file',
                        type=str,
                        action='store',
                        nargs='?',
                        help=file_parameter_usage)

    # parse arguments
    args = parser.parse_args()

    # directory path for attached file.
    # if not fed, use $CWD.
    if not args.directory:
        cwd = os.path.curdir
        dir_path = os.path.abspath(cwd)
    else:
        dir_path = args.directory

    # create dir if not exist yet.
    try:
        os.mkdir(dir_path)
    except OSError as e:
        # Ignore directory exists error
        # TODO : <TBD> Consider behavior.
        if e.errno != errno.EEXIST:
            raise

    # Create 'Message' from file descriptor.
    # Read it as binary data.
    if not args.file:
        msg = email.message_from_binary_file(sys.stdin.buffer)
    else:
        msg_file_path = args.file  # message file.
        fp = open(msg_file_path, 'rb')
        with fp:
            msg = email.message_from_binary_file(fp)

    parse_message(msg, dir_path)


# ----------------------------------------------------------------------
# main
if __name__ == '__main__':
    script_main()

