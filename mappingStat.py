import os
import os.path
import argparse
import commands

def stat_extractor(filename):
	fh = open(filename,'r')
	total_input,uniqReads_num,uniqReads_pct,mm_pct = '','','',''
	misMat_base,too_mm_pct,unmapped_too_mm_pct,unmapped_too_short_pct = '','','',''
	unmapped_other_pct,chimeric_pct,avg_len = '','',''
	for line in fh.readlines():
		line = line.strip()
		w = line.split("|")
		if "Number of input reads" in line:
			total_input = w[1].strip()
		elif "Uniquely mapped reads number" in line:
			uniqReads_num = w[1].strip()
		elif "Uniquely mapped reads %" in line:
			uniqReads_pct = w[1].strip()
		elif "% of reads mapped to multiple loci" in line:
			mm_pct = w[1].strip()
		elif "Mismatch rate per base, %" in line:
			misMat_base = w[1].strip()
		elif "% of reads mapped to too many loci" in line:
			too_mm_pct = w[1].strip()
		elif "% of reads unmapped: too many mismatches" in line:
			unmapped_too_mm_pct = w[1].strip()
		elif "% of reads unmapped: too short" in line:
			unmapped_too_short_pct = w[1].strip()
		elif "% of reads unmapped: other" in line:
			unmapped_other_pct = w[1].strip()
		elif "% of chimeric reads" in line:
			chimeric_pct = w[1].strip()
		elif "Average input read length" in line:
			avg_len = w[1].strip()

	return total_input,uniqReads_num,uniqReads_pct,chimeric_pct,mm_pct,too_mm_pct,\
			unmapped_other_pct,unmapped_too_mm_pct,unmapped_too_short_pct,misMat_base,avg_len
			
	fh.close()

# Main ---------------------------------------------------
parser = argparse.ArgumentParser(description='')
parser.add_argument('--dir', required=True,help="Specify a dir which contains all STAR mapping summary infos")
parser.add_argument('--out', default="Align.summary.txt",help="Specify the output filename")

args = parser.parse_args()

path = args.dir
if path[0] == ".":
	a,b = commands.getstatusoutput('pwd')
	path = b + path[1:]


output_file = args.out
fho = open(output_file,'w')
header = ["sample_id","input_reads_number","unique_mapping","unique%","chimeric%","multi_mapping%","too_many_loci%",\
		"unmapped_other%","unmapped_too_many_mismatch%","unmapped_too_short%","mismatch_rate_per_base","average_input_length"]
print >>fho,"\t".join(header)

for filename in os.listdir(path):
	suffix_most = os.path.splitext(filename)
	if suffix_most[-1] == ".out":
		suffix_second = os.path.splitext(suffix_most[0])
		if suffix_second[-1] == ".final":
			x = stat_extractor(path + filename)
			sample = suffix_second[0].rstrip("_Log")
			x = [sample] + list(x)
			print >> fho, "\t".join(x)

fho.close()
