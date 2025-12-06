"""
DNA Pattern Finder is a console program that:

Reads one DNA sequence from a text file
Treats the sequence as a single continuous string of characters A, C, G, T
Provides a menu for performing common analyses, including:
Viewing summary statistics
Searching for motifs (e.g., ATG, TATA)
Calculating GC content (overall + sliding windows)
Finding simple ORFs in the forward strand
Allows the user to export a short text report summarising the analysis
"""

VALID_BASES = "ACGT"

MENU = """Menu:
S - Sequence summary
M - Find motif
G - GC content
O - Find ORFs
R - Export report
Q - Quit"""

def main():
    """Run the DNA Pattern Finder program."""
    print("Welcome to DNA Pattern Finder 1.0.")
    sequence, filename = get_valid_sequence()

    print(MENU)
    choice = input(">>> ").upper()

    while choice != "Q":
        if choice == "S":
            handle_summary(sequence)

        elif choice == "M":
            pass
        elif choice == "G":
            pass
        elif choice == "O":
            pass
        elif choice == "R":
            pass
        else:
            print("Invalid menu option.")

        print(MENU)
        choice = input(">>> ").upper()

    print("Happy hunting!")

def get_valid_sequence():
    """Prompt for a filename until a valid DNA sequence is loaded."""

    while True:
        filename = input("DNA file: ").strip()
        if filename == "":
            print("Filename cannot be blank.")

        try:
            sequence = load_sequence(filename)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except ValueError as error:
            print(f"Error in file '{filename}': {error}")
        else:
            print(f"Sequence loaded from {filename} (length: {len(sequence)} bases)")
            return sequence, filename

def load_sequence(filename):
    """Load and validate a DNA sequence from the given filename."""
    with open(filename, 'r') as in_file:
        raw_text = in_file.read()

    sequence = "".join(raw_text.split()).upper()

    if not sequence:
        raise ValueError("File is empty or contains no sequence data.")

    for base in sequence:
        if base not in VALID_BASES:
            raise ValueError(f"Invalid base '{base}' found in file.")

    return sequence

def get_base_count(sequence):
    """Return a dictionary mapping each base (A/C/G/T) to its count in the sequence."""

    base_count = {}

    for base in VALID_BASES:
        base_count[base] = 0

    for base in sequence:
        base_count[base] += 1

    return base_count

def handle_summary(sequence):
    """Display sequence data and statistics upon user input."""
    dna_length = len(sequence)
    base_counts = get_base_count(sequence)

    print(f"Sequence length: {dna_length} bases.")
    print(
        f"A: {base_counts['A']}\t"
        f"C: {base_counts['C']}\t"
        f"G: {base_counts['G']}\t"
        f"T: {base_counts['T']}\t"
    )

def calculate_gc_content(sequence):
    pass

def find_motif_positions(sequence, motif):
    pass

def calculate_window_gc(sequence, window_size):
    pass

def find_orfs(sequence):
    pass

def export_report():
    pass

if __name__ == "__main__":
    main()