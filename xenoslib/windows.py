#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import msvcrt


def pause():
    print('Press any key to continue...')
    msvcrt.getch()
    while msvcrt.kbhit():
        msvcrt.getch()


def timeout(seconds):
    for second in range(seconds, 0, -1):
        if msvcrt.kbhit():
            break
        print(f'Waiting {second}s , press any key to continue...', end='\r')
        time.sleep(1)
    print()


if __name__ == '__main__':
    timeout(3)
