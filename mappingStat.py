import os
import argparse
import subprocess

def stat_extractor(filename):
    with open(filename, 'r') as fh:
        total_input = uniqReads_num = uniqReads_pct = mm_pct = ''
        misMat_base = too_mm_pct = unmapped_too_mm_pct = unmapped_too_short_pct = ''
        unmapped_other_pct = chimeric_pct = avg_len = ''

        for line in fh:
            line = line.strip()
            parts = line.split("|")
            if "Number of input reads" in line:
                total_input = parts[1].strip() if len(parts) > 1 else ''
            elif "Uniquely mapped reads number" in line:
                uniqReads_num = parts[1].strip() if len(parts) > 1 else ''
            elif "Uniquely mapped reads %" in line:
                uniqReads_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "% of reads mapped to multiple loci" in line:
                mm_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "Mismatch rate per base, %" in line:
                misMat_base = parts[1].strip() if len(parts) > 1 else ''
            elif "% of reads mapped to too many loci" in line:
                too_mm_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "% of reads unmapped: too many mismatches" in line:
                unmapped_too_mm_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "% of reads unmapped: too short" in line:
                unmapped_too_short_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "% of reads unmapped: other" in line:
                unmapped_other_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "% of chimeric reads" in line:
                chimeric_pct = parts[1].strip() if len(parts) > 1 else ''
            elif "Average input read length" in line:
                avg_len = parts[1].strip() if len(parts) > 1 else ''

        return (total_input, uniqReads_num, uniqReads_pct, chimeric_pct,
                mm_pct, too_mm_pct, unmapped_other_pct, unmapped_too_mm_pct,
                unmapped_too_short_pct, misMat_base, avg_len)

# Main ---------------------------------------------------
parser = argparse.ArgumentParser(description='')
parser.add_argument('--dir', required=True, help="Specify a directory which contains all STAR mapping summary infos")
parser.add_argument('--out', default="Align.summary.txt", help="Specify the output filename")
args = parser.parse_args()

path = args.dir
if not path.startswith('.'):
    # Handle relative paths if necessary
    current_dir = subprocess.run(['pwd'], capture_output=True, text=True).stdout.strip()
    path = os.path.join(current_dir, path)

output_file = args.out
with open(output_file, 'w') as fho:
    header = [
        "sample_id", "input_reads_number", "unique_mapping",
        "unique%", "chimeric%", "multi_mapping%",
        "too_many_loci%", "unmapped_other%",
        "unmapped_too_many_mismatch%", "unmapped_too_short%",
        "mismatch_rate_per_base", "average_input_length"
    ]
    print('\t'.join(header), file=fho)

    for filename in os.listdir(path):
        suffix_most = os.path.splitext(filename)
        if suffix_most[-1] == ".out":
            suffix_second = os.path.splitext(suffix_most[0])
            sample_name = suffix_second[0]
            
            # Extract statistics
            stats = stat_extractor(os.path.join(path, filename))
            
            # Prepare data row
            data_row = [
                sample_name,
                stats[0], stats[1], stats[2],
                stats[3], stats[4], stats[5],
                stats[6], stats[7], stats[8],
                stats[9], stats[10]
            ]
            
            # Print the row
            print('\t'.join(data_row), file=fho)

print(f"Output written to {output_file}")
