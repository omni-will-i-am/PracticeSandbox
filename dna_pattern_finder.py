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

MENU = """Menu:
S - Sequence summary
M - Find motif
G - GC content
O - Find ORFs
R - Export report
Q - Quit"""

def main():
    print(MENU)
    choice = input(">>> ").upper()

    while choice != "Q":
        if choice == "S":
            pass
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

def load_sequence(filename):
    pass

def get_base_count(sequence):
    pass

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