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
G - GC Content Options
O - Find ORFs
R - Export report
Q - Quit"""


def main():
    """Run the DNA Pattern Finder program."""
    print("Welcome to DNA Pattern Finder 1.0.")
    sequence, filename = get_valid_sequence()

    last_motif = None
    last_motif_positions = []

    print(MENU)
    choice = input(">>> ").upper()

    while choice != "Q":
        if choice == "S":
            handle_summary(sequence)

        elif choice == "M":
            handle_motif_search(sequence)

        elif choice == "G":
            handle_window_gc(sequence)

        elif choice == "O":
            handle_orf_search(sequence)

        elif choice == "R":
            export_report(sequence, filename, last_motif, last_motif_positions)

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


def calculate_gc_content(sequence):
    """Return GC content of the sequence as a percentage."""
    base_count = get_base_count(sequence)
    dna_length = len(sequence)
    gc_bases = base_count["G"] + base_count["C"]
    gc_fraction = gc_bases / dna_length

    return gc_fraction * 100


def handle_summary(sequence):
    """Display sequence data and statistics upon user input."""
    dna_length = len(sequence)
    base_counts = get_base_count(sequence)
    gc = calculate_gc_content(sequence)

    print(f"Sequence length: {dna_length} bases.")
    print(
        f"A: {base_counts['A']}\t"
        f"C: {base_counts['C']}\t"
        f"G: {base_counts['G']}\t"
        f"T: {base_counts['T']}\t"
    )
    print(f"GC content: {gc:.1f}%")


def find_motif_positions(sequence, motif):
    """Return a list of 0-based positions where motif occurs in sequence."""
    motif = motif.upper()
    positions = []
    motif_length = len(motif)

    for i in range(len(sequence) - motif_length + 1):
        if sequence[i:i + motif_length] == motif:
            positions.append(i)

    return positions


def get_valid_motif(sequence):
    """Prompt user for valid motif and return it."""
    while True:
        motif = input("Motif (A/C/G/T only): ").strip()
        if motif == "":
            print("Motif cannot be blank.")
            continue

        motif = motif.upper()

        invalid_char_found = False
        for character in motif:
            if character not in VALID_BASES:
                print(f"Invalid character '{character}' in motif. Use only A/C/G/T.")
                invalid_char_found = True
                break

        if invalid_char_found:
            continue

        if len(motif) > len(sequence):
            print("Motif is longer than the sequence.")
            continue

        return motif


def handle_motif_search(sequence):
    """Runs the motif search menu option."""
    motif = get_valid_motif(sequence)
    positions = find_motif_positions(sequence, motif)

    count = len(positions)
    print(f"Motif '{motif}' found {count} times.")

    if positions:
        display_positions = [position + 1 for position in positions]
        print("Motif positions:", ", ".join(str(position) for position in display_positions))

    return motif, positions


def calculate_window_gc(sequence, window_size):
    """Return a list of GC% values for non-overlapping windows of the given size."""
    gc_percentages = []
    sequence_length = len(sequence)

    # Step in jumps of window_size: 0, window_size, 2*window_size, ...
    for start in range(0, sequence_length, window_size):
        end = start + window_size
        window = sequence[start:end]  # last window may be shorter

        # Just in case, guard against empty window (shouldn't happen)
        if not window:
            continue

        gc_percent = calculate_gc_content(window)
        gc_percentages.append(gc_percent)

    return gc_percentages


def get_valid_window_size(sequence_length):
    """Prompt for a valid window size and return it as an int."""
    window_size = 0
    while window_size <= 0 or window_size > sequence_length:
        try:
            window_size = int(input("Window size: "))
            if window_size <= 0:
                print("Window size must be > 0.")
            elif window_size > sequence_length:
                print("Window size must not be larger than the sequence length.")
        except ValueError:
            print("Invalid input - please enter a valid integer.")
            window_size = 0
    return window_size


def handle_window_gc(sequence):
    """Handle the GC content (windowed) menu option."""
    sequence_length = len(sequence)
    window_size = get_valid_window_size(sequence_length)

    gc_percentages = calculate_window_gc(sequence, window_size)

    for index, gc_percent in enumerate(gc_percentages, start=1):
        # Convert to 1-based base positions
        start_base = (index - 1) * window_size + 1
        end_base = min(index * window_size, sequence_length)
        print(f"Window {index} (bases {start_base}–{end_base}): {gc_percent:.1f}% GC")


def find_orfs(sequence):
    """Return a list of (start_index, end_index) for ORFs in the sequence.

        The indexes are 0-based and inclusive.
        Start codon: ATG
        Stop codons: TAA, TAG, TGA
        """
    start_codon = "ATG"
    stop_codons = ("TAA", "TAG", "TGA")

    orfs = []
    i = 0
    sequence_length = len(sequence)

    while i <= sequence_length - 3:
        codon = sequence[i:i + 3]
        if codon == start_codon:
            # Found a start; now scan codons in-frame
            j = i + 3
            while j <= sequence_length - 3:
                stop_codon = sequence[j:j + 3]
                if stop_codon in stop_codons:
                    # end_index is inclusive: j, j+1, j+2 → so j+2
                    end_index = j + 2
                    orfs.append((i, end_index))
                    break
                j += 3
            # Move to next position after this start; we could skip ahead by 3,
            # but moving by 1 is simpler and still correct.
            i += 1
        else:
            i += 1

    return orfs


def handle_orf_search(sequence):
    """Handle the ORF-finding menu option."""
    orfs = find_orfs(sequence)

    if not orfs:
        print("No ORFs found.")
        return

    print(f"Found {len(orfs)} ORFs:")
    for index, (start, end) in enumerate(orfs, start=1):
        # Convert 0-based to 1-based positions for display
        start_pos = start + 1
        end_pos = end + 1
        length = end - start + 1
        print(f"{index}) start: {start_pos}, stop: {end_pos}, length: {length} bases")


def export_report(sequence, current_filename, last_motif, last_motif_positions):
    """Export a text report summarising the current analysis."""
    report_filename = input("Report filename: ").strip()
    if report_filename == "":
        print("Report filename cannot be blank.")
        return

    length = len(sequence)
    base_counts = get_base_count(sequence)
    gc_percent = calculate_gc_content(sequence)

    # We can recompute ORFs here (no need to store them in main)
    orfs = find_orfs(sequence)

    try:
        with open(report_filename, "w") as out_file:
            print("DNA Pattern Finder Report", file=out_file)
            print(f"Source file: {current_filename}", file=out_file)
            print(file=out_file)  # blank line

            print(f"Sequence length: {length} bases", file=out_file)
            print(
                f"A: {base_counts['A']}    "
                f"C: {base_counts['C']}    "
                f"G: {base_counts['G']}    "
                f"T: {base_counts['T']}",
                file=out_file,
            )
            print(f"GC content: {gc_percent:.1f}%", file=out_file)
            print(file=out_file)

            # Motif info
            if last_motif is None:
                print("Last motif searched: (none)", file=out_file)
                print("Motif occurrences: n/a", file=out_file)
            else:
                print(f"Last motif searched: {last_motif}", file=out_file)
                print(f"Motif occurrences: {len(last_motif_positions)}", file=out_file)
            print(file=out_file)

            # ORF info
            print(f"Number of ORFs found (forward strand): {len(orfs)}", file=out_file)
            for index, (start, end) in enumerate(orfs, start=1):
                start_pos = start + 1
                end_pos = end + 1
                length_bases = end - start + 1
                print(
                    f"{index}) start: {start_pos}, stop: {end_pos}, "
                    f"length: {length_bases} bases",
                    file=out_file,
                )

        print(f"Report saved to {report_filename}")
    except OSError as error:
        print(f"Error saving report: {error}")


if __name__ == "__main__":
    main()
