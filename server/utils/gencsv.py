import csv, sys

PREFIX = "CY"
CSV_OUTPUT_FILE = "list.csv"
# maximum product id possible = 36^6 = 2176782336; i.e. [0, 2176782336)
MAX_PRODUCT_ID = 2176782336
BASE = 36

def validate(start, count):
    end = start + count
    # ensure count and start is +ve
    assert (start >= 0 and count > 0)
    assert (start < MAX_PRODUCT_ID)
    assert (end <= MAX_PRODUCT_ID)

# Function to convert a number to the extended base-36 string
def convert_number_to_base36(number):
    if 0 <= number < BASE**6:
        base36_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        base36_str = ''
        for _ in range(6):
            number, remainder = divmod(number, BASE)
            base36_str = base36_chars[remainder] + base36_str
        return PREFIX + base36_str
    else:
        raise ValueError("Number must be between 0 and 36^6-1 for this conversion.")


if __name__ == "__main__":
    # called from terminal

    # numbers in the range -2147483648 through 2147483647
    start = int(sys.argv[1])
    count = int(sys.argv[2])
    end = start + count
    PREFIX = sys.argv[3]

    validate(start, count)

    # generate the list [start, end)
    # write for the tracker sheet entry
    validate(start, count)
    with open('tracker.csv', 'w') as new_file:
        write=csv.writer(new_file, delimiter='\n')
        [write.writerow([convert_number_to_base36(id)]) for id in range(start, end)]



# >>> import execution_methods
# This is my file to test Python's execution methods.
# The variable __name__ tells me which context this file is running in.
# The value of __name__ is: 'execution_methods'