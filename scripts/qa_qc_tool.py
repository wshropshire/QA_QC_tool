import logging
import argparse
import subprocess
import os

def create_directory(outdir):
    """Function to create the output directory"""
    if os.path.isdir(outdir):
        raise Exception("Directory already exists")
    if not os.path.isdir(outdir):
        os.system("mkdir -p %s" % outdir)
    return


def make_prokka_command(prokka_path, contigs, sample_name, outdir, threads):
    prokka_command = ['{0}'.format(prokka_path), '--cpus', threads, '--compliant', '--outdir',
                      '{0}/{1}_prokka_results'.format(outdir, sample_name), '--prefix',
                      '{0}_prokka'.format(sample_name), contigs]
    subprocess.run(prokka_command)
    return

def make_getFasta_stats_command(getFasta_stats_path, contigs, outdir, sample_name):
        getFasta_stats_command = ['{0}'.format(getFasta_stats_path), '-T', contigs]
        result = subprocess.run(getFasta_stats_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        fasta_stats = result.stdout.decode('utf-8')
        fastaStat_file_name = "{0}/{1}_fasta_stats.tsv".format(outdir, sample_name)
        fastaStats_file = open(fastaStat_file_name, 'w')
        fastaStats_file.write(fasta_stats)
        fastaStats_file.close()


def make_minimap2_command(minimap2_path, contigs, long_reads, threads, outdir):
    minimap2_cmd = ['{0}'.format(minimap2_path), '-t', threads, '-ax', 'map-ont', contigs, long_reads]
    result = subprocess.run(minimap2_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    minimap2 = result.stdout.decode('utf-8')
    minimap2_align = "{0}/align.sam".format(outdir)
    minimap2_align_file = open(minimap2_align, 'w')
    minimap2_align_file.write(minimap2)
    minimap2_align_file.close()
    return


def make_bwa_command(bwa_path, assembly_reference, pe_reads, outdir, threads):
    print("Indexing assembly reference for bwa alignment")
    bwa_index_cmd = ['{0}'.format(bwa_path), 'index', assembly_reference]
    subprocess.run(bwa_index_cmd)
    print("bwa-mem alignment with assembly reference and paired-end short-reads")
    bwa_align_cmd = ['{0}'.format(bwa_path), 'mem', '-t', threads, '-o',
                     '{0}/align_2.sam'.format(outdir), assembly_reference, pe_reads]
    subprocess.run(bwa_align_cmd)
    return


def make_pileup_command(pileup_path, sam_file, sample_name, outdir):
    pileup_command = ['{0}'.format(pileup_path), 'in={0}'.format(sam_file),
                      'out={0}/{1}_covstats.tsv'.format(outdir, sample_name),
                      'basecov={0}/{1}_basecov.tsv'.format(outdir, sample_name),
                      'delcoverage=f']
    subprocess.run(pileup_command)
    return


def make_snippy_command(snippy_path, contigs, pe_reads, sample_name, outdir, threads):
    snippy_command = ['{0}'.format(snippy_path), '--cpus', threads, '--outdir', '{0}/snippy_results'.format(outdir),
                      '--prefix', sample_name, '--ref', contigs, '--peil', pe_reads]
    subprocess.run(snippy_command)
    return


def make_mlst_command(mlst_path, contigs, sample_name, outdir):
    mlst_command = ['{0}'.format(mlst_path), contigs]
    result = subprocess.run(mlst_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    mlst = result.stdout.decode('utf-8')
    mlst_file_name = "{0}/{1}_mlst.tsv".format(outdir, sample_name)
    mlst_file = open(mlst_file_name, 'w')
    mlst_file.write(mlst)
    mlst_file.close()
    return


def make_abricate_command(abricate_path, contigs, db, sample_name, outdir):
    abricate_command = ['{0}'.format(abricate_path), '--nopath', '--mincov', '90', '--minid', '90', '--db', db, contigs]
    result = subprocess.run(abricate_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    abricate = result.stdout.decode('utf-8')
    abricate_file_name = "{0}/{1}_{2}_abricate.tsv".format(outdir, sample_name, db)
    abricate_file = open(abricate_file_name, 'w')
    abricate_file.write(abricate)
    abricate_file.close()
    return


def get_arguments():
    """Parse assembler arguments"""
    parser = argparse.ArgumentParser(description="ONT plus Illumina consensus assembler QC and preliminary results", add_help=False)

    # Help arguments
    help_group = parser.add_argument_group("Help")
    help_group.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    help_group.add_argument('-V', '--version', action='version', version='%(prog)s version 0.1',
                            help="Show QC and preliminary result version number")

    # input_arguments
    input_group = parser.add_argument_group("Inputs")
    input_group.add_argument('-s', '--sample_name', required=True, help="Name of the sample to use in the "
                            "outdir/outfiles as prefix", type=str, default=None)
    input_group.add_argument('-c', '--contigs', required=True, help="existing contigs fasta file", type=str,
                             default=None)
    input_group.add_argument('-l', '--long_reads', required=True, help="Path to the ONT long reads", type=str,
                             default=None)
    input_group.add_argument('-pe', '--pe_reads', required=True, help='interleave paired-end reads', type=str,
                             default=None)

    # Pipeline arguments
    pipeline_group = parser.add_argument_group("Pipeline Arguments")
    pipeline_group.add_argument('--bwa_path', required=False, help="Path to bwa executable. Please use \'bwa\' in "
                                                                   "the pathway if provided", type=str, default='bwa')
    pipeline_group.add_argument('--prokka_path', required=False, help='Path to prokka executable. Need to include'
                                '\'prokka\' in pathway', type=str, default='prokka')
    pipeline_group.add_argument('--getFasta_stats_path', required=False, help='Path to abricate executable. Need to include'
                                '\'get_fasta_stats.pl\' in pathway', type=str, default='get_fasta_stats.pl')
    pipeline_group.add_argument('--minimap2_path', required=False, help='Path to minimap2 executable. Need to include'
                                '\'minimap2\' in pathway', type=str, default='minimap2')
    pipeline_group.add_argument('--pileup_path', required=False, help='Path to pileup.sh bbmap executable. Need to include'
                                '\'pileup.sh\' in pathway', type=str, default='pileup.sh')
    pipeline_group.add_argument('--snippy_path', required=False, help='Path to snippy executable. Need to include'
                                '\'snippy\' in pathway', type=str, default='snippy')
    pipeline_group.add_argument('--mlst_path', required=False, help='Path to mlst executable. Need to include'
                                '\'mlst\' in pathway', type=str, default='mlst')
    pipeline_group.add_argument('--abricate_path', required=False, help='Path to abricate executable. Need to include'
                                '\'abricate\' in pathway', type=str, default='abricate')

    # Output arguments
    optional_group = parser.add_argument_group("Output and Options")
    optional_group.add_argument('-o', '--outdir', required=True, help="Name of the output directory", type=str,
                                default=None)
    optional_group.add_argument('-t', '--threads', required=False, help="Number of threads to run program", type=str,
                                default=1)
    args = parser.parse_args()
    return args


def run_conditions():
    logging.basicConfig(filename='torsten_tool.log', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Start pipeline')
    args = get_arguments()
    contigs = args.contigs
    outdir = args.outdir
    sample_name = args.sample_name
    threads = args.threads
    create_directory(args.outdir)
    print("\nCreating annotation files from input fasta file\n")
    make_prokka_command(args.prokka_path, contigs, sample_name, outdir, threads)
    fna_file = '{0}/{1}_prokka_results/{1}_prokka.fna'.format(outdir, sample_name)
    print("\nGenerating initial fasta stats\n")
    make_getFasta_stats_command(args.getFasta_stats_path, fna_file, outdir, sample_name)
    print("\nCreating a long-read pileup to get coverage stats per contig\n")
    make_minimap2_command(args.minimap2_path, fna_file, args.long_reads, threads, outdir)
    sam_file = '{0}/align.sam'.format(outdir)
    make_pileup_command(args.pileup_path, sam_file, sample_name, outdir)
    os.system('rm -r %s' % sam_file)
    print("\nCreating a short-read pileup to get coverage stats per contig\n")
    make_bwa_command(args.bwa_path, fna_file, args.pe_reads, outdir, threads)
    sample_name_short = '{0}_shortRead'.format(sample_name)
    sam_file2 = '{0}/align_2.sam'.format(outdir)
    make_pileup_command(args.pileup_path, sam_file2, sample_name_short, outdir)
    os.system('rm -r %s' % sam_file2)
    print("\nShort read consensus check using Snippy\n")
    gbk_file = '{0}/{1}_prokka_results/{1}_prokka.gbk'.format(outdir, sample_name)
    make_snippy_command(args.snippy_path, gbk_file, args.pe_reads, sample_name, outdir, threads)
    print("\nMLST check\n")
    make_mlst_command(args.mlst_path, gbk_file, sample_name, outdir)
    print("\nAbricate results using CARD and PlasmidFinder databases\n")
    make_abricate_command(args.abricate_path, gbk_file, 'card', sample_name, outdir)
    make_abricate_command(args.abricate_path, gbk_file, 'plasmidfinder', sample_name, outdir)
    logging.info('End of pipeline')
    print("\nFin! Enjoy your day!\n")


if __name__ == '__main__': run_conditions()
