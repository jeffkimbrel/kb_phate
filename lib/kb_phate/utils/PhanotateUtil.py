import os
import datetime
import logging
import uuid

from installed_clients.GenomeAnnotationAPIClient import GenomeAnnotationAPI
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace as Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.AssemblyUtilClient import AssemblyUtil

class PhanotateUtil:

    workdir     = 'tmp/work/'
    staging_dir = "/staging/"
    datadir     = "/kb/module/data/"

    def __init__(self, config):
        os.makedirs(self.workdir, exist_ok = True)
        self.config       = config
        self.timestamp    = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch      = config['scratch']
        self.genome_api   = GenomeAnnotationAPI(self.callback_url)
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu          = GenomeFileUtil(self.callback_url)
        self.au           = AssemblyUtil(self.callback_url)
        self.kbr          = KBaseReport(self.callback_url)
        self.ws_client    = Workspace(config["workspace-url"])

    def get_assembly(self, assembly_ref):
        #logging.info(assembly_ref)
        fasta_path = self.au.get_assembly_as_fasta({"ref": assembly_ref})["path"]
        return fasta_path

    def phanotate(self, fasta_path):
        genbank_path = '/kb/module/work/tmp/' + str(uuid.uuid4()) + '.gbk'
        os.system('python /PHANOTATE/phanotate.py ' + fasta_path + ' --outfmt genbank > ' + genbank_path)
        return genbank_path

    def add_genome(self, genbank_path, params):
        genome_params = {
                     'file': {'path'  : genbank_path},
                     'workspace_name' : params['workspace_name'],
                     'genome_name'    : params['genome_name']
                 }

        return self.gfu.genbank_to_genome(genome_params)['genome_info']

    def generate_report(self, params, genome_ref):

        output_html_files = list()

        # Make report directory and copy over files
        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        os.mkdir(output_directory)
        result_file_path = os.path.join(output_directory, 'phannotate_summary.html')

        # Build HTML tables for results
        table_lines = []
        table_lines.append(f'<h2>Hello World!</h2>')

        # Write to file
        with open(result_file_path, 'w') as result_file:
            for line in table_lines:
                result_file.write(line + "\n")

        output_html_files.append(
            {'path'       : output_directory,
             'name'       : os.path.basename(result_file_path),
             'description': 'HTML report for run_phanotate app'})

        report_params = {
            'message'                   : '',
            'html_links'                : output_html_files,
            'direct_html_link_index'    : 0,
            'objects_created' : [{'ref' : genome_ref, 'description' : 'Genome with PHANOTATE gene calls'}],
            'workspace_name'            : params['workspace_name'],
            'report_object_name'        : f'phanotate_{uuid.uuid4()}'}

        output = self.kbr.create_extended_report(report_params)

        return {'output_genome_ref' : genome_ref,
                'report_name'       : output['name'],
                'report_ref'        : output['ref']}

    def run(self, ctx, params):

        fasta_path   = self.get_assembly(params['assembly_ref'])
        genbank_path = self.phanotate(fasta_path)
        genome_info  = self.add_genome(genbank_path, params)

        logging.info(genome_info)

        genome_ref = str(genome_info[6]) + "/" + str(genome_info[0]) + "/" + str(genome_info[4])
        logging.info(genome_ref)

        report = self.generate_report(params, genome_ref)

        return report
