#!/usr/bin/env python3

"""
Battery Joltage Calculator 
Select exactly two batteries (in their original order) to form largest two-digit number.
"""

def find_max_joltage(bank_str):
    """
    Find maximum joltage by selecting two batteries.
    When batteries at positions i and j are selected (i < j),
    the joltage is digit_i followed by digit_j.
    """
    bank = [int(digit) for digit in bank_str]
    n = len(bank)
    max_joltage = 0
    
    # Check all pairs where i < j (maintain original order)
    for i in range(n):
        for j in range(i + 1, n):  # j must be after i
            # Form number: digit at i followed by digit at j
            joltage = bank[i] * 10 + bank[j]
            if joltage > max_joltage:
                max_joltage = joltage
    
    return max_joltage


def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: {} <input_file>".format(sys.argv[0]))
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            banks = [line.strip() for line in f if line.strip()]
        
        total_joltage = 0
        results = []
        
        print("Battery Bank Analysis:")
        print("-" * 60)
        
        for idx, bank_str in enumerate(banks, 1):
            max_jolt = find_max_joltage(bank_str)
            total_joltage += max_jolt
            results.append((idx, bank_str, max_jolt))
            
            # Display
            display_bank = bank_str if len(bank_str) <= 30 else bank_str[:27] + "..."
            print("Bank {}: {}".format(idx, display_bank))
            print("  Maximum joltage: {}".format(max_jolt))
            
            # Show explanation for example cases
            if bank_str == "987654321111111":
                print("  Explanation: First two batteries (9 and 8) -> 98")
            elif bank_str == "811111111111119":
                print("  Explanation: First battery (8) and last battery (9) -> 89")
            elif bank_str == "234234234234278":
                print("  Explanation: Last two batteries (7 and 8) -> 78")
            elif bank_str == "818181911112111":
                print("  Explanation: 9 at position 7 and 2 at position 12 -> 92")
        
        print("-" * 60)
        print("Summary:")
        print("-" * 60)
        
        # Build sum string
        sum_parts = []
        for idx, bank_str, max_jolt in results:
            print("Bank {}: {}".format(idx, max_jolt))
            sum_parts.append(str(max_jolt))
        
        print("-" * 60)
        sum_str = " + ".join(sum_parts)
        print("Total: {} = {}".format(sum_str, total_joltage))
        print("-" * 60)
        
        # Save result
        with open("output3.txt", 'w') as f:
            f.write(str(total_joltage))
        
        print("Result saved to 'output3.txt'")
        
        return total_joltage
        
    except FileNotFoundError:
        print("Error: File '{}' not found.".format(input_file))
        sys.exit(1)


if __name__ == "__main__":
    main()
