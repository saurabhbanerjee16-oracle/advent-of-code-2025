import sys

def calculate_password_from_file(filename):
    """Calculate password from rotations in a file"""
    try:
        with open(filename, 'r') as file:
            rotations = [line.strip() for line in file if line.strip()]
        
        if not rotations:
            print(f"File '{filename}' is empty")
            return None
        
        dial_range = 100
        current_position = 50
        zero_count = 0
        
        print(f"Processing rotations from '{filename}':")
        print("-" * 50)
        
        for i, rotation in enumerate(rotations, 1):
            # Validate input format
            if len(rotation) < 2 or (rotation[0] not in ['L', 'R']):
                print(f"Warning: Invalid format '{rotation}' on line {i}, skipping")
                continue
                
            try:
                direction = rotation[0]
                distance = int(rotation[1:])
            except ValueError:
                print(f"Warning: Invalid number in '{rotation}' on line {i}, skipping")
                continue
            
            previous_position = current_position
            
            if direction == 'L':
                current_position = (current_position - distance) % dial_range
            else:  # 'R'
                current_position = (current_position + distance) % dial_range
            
            is_zero = current_position == 0
            if is_zero:
                zero_count += 1
            
            print(f"Step {i:3d}: {rotation:8s} | {previous_position:3d} → {current_position:3d} {'(ZERO!)' if is_zero else ''}")
        
        print("-" * 50)
        print(f"\nResults:")
        print(f"Total rotations processed: {len(rotations)}")
        print(f"Times dial pointed to 0: {zero_count}")
        print(f"Password: {zero_count}")
        
        return zero_count
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    print("=" * 60)
    print("SAFE DIAL PASSWORD CALCULATOR (File Input)")
    print("=" * 60)
    
    # Check if filename provided as command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"Using file: {filename}")
        calculate_password_from_file(filename)
    else:
        # Ask user for filename
        filename = input("\nEnter the filename containing rotations: ").strip()
        
        if not filename:
            print("No filename provided. Exiting.")
            return
        
        calculate_password_from_file(filename)

# Alternative: Simple file reading without verbose output
def simple_file_calculation(filename):
    """Simple version that just calculates and returns the password"""
    try:
        with open(filename, 'r') as file:
            rotations = [line.strip() for line in file if line.strip()]
        
        if not rotations:
            print("File is empty")
            return None
        
        position = 50
        count = 0
        
        for rotation in rotations:
            if len(rotation) >= 2 and rotation[0] in "LR":
                try:
                    steps = int(rotation[1:])
                    if rotation[0] == 'L':
                        position = (position - steps) % 100
                    else:
                        position = (position + steps) % 100
                    
                    if position == 0:
                        count += 1
                except ValueError:
                    continue
        
        print(f"Password from file '{filename}': {count}")
        return count
        
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None

if __name__ == "__main__":
    main()
