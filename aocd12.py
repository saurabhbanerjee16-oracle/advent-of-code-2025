#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

def count_zeros_in_rotation(start, direction, degrees):
 """
 Count ALL times the dial points at 0 during a rotation.
 This includes both during the movement AND at the final position.
 
 For k from 1 to degrees:
 - If direction == 'R': position = (start + k) % 100
 - If direction == 'L': position = (start - k) % 100
 Count how many times position == 0.
 """
    count = 0
    
    if direction == 'L':
        k0 = start if start > 0 else 100
        while k0 <= degrees:
            count += 1
            k0 += 100
        new_pos = (start - degrees) % 100
    else:
        k0 = (100 - start) % 100
        if k0 == 0:
            k0 = 100
        while k0 <= degrees:
            count += 1
            k0 += 100
        new_pos = (start + degrees) % 100
    
    return new_pos, count

def main():
    if len(sys.argv) != 2:
        print("Usage: python solve.py inputfile")
        return
    
    with open(sys.argv[1], 'rb') as f:
        content = f.read().decode('latin-1')
    
    rotations = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        i = 0
        while i < len(line):
            if line[i].upper() in ('L', 'R'):
                j = i + 1
                while j < len(line) and line[j].isdigit():
                    j += 1
                if j > i + 1:
                    rotations.append(f"{line[i].upper()}{line[i+1:j]}")
                i = j
            else:
                i += 1
    
    pos = 50
    total = 0
    step = 1
    
    print("\n" + "-" * 50)
    
    for rot in rotations:
        d = rot[0]
        n = int(rot[1:])
        new_pos, zeros = count_zeros_in_rotation(pos, d, n)
        total += zeros
        marker = " (ZERO!)" if new_pos == 0 else ""
        print(f"Step {step:3}: {d}{n:<4}    | {pos:3} -> {new_pos:3}{marker}")
        pos = new_pos
        step += 1
    
    print("-" * 50)
    print(f"\nPassword: {total}")

if __name__ == "__main__":
    main()
