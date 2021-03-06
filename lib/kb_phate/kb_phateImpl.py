# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport

from .utils.PhanotateUtil import PhanotateUtil
from kb_phate.utils.PhanotateUtil import PhanotateUtil

#END_HEADER


class kb_phate:
    '''
    Module Name:
    kb_phate

    Module Description:
    A KBase module: kb_phate
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.2.3"
    GIT_URL = "https://github.com/jeffkimbrel/kb_phate.git"
    GIT_COMMIT_HASH = "fa4fcdaf4fc9b0ef4533ffbf3e7f13db3363a91e"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.config = config
        self.config['SDK_CALLBACK_URL'] = self.callback_url
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_phanotate(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_phanotate
        import_runner = PhanotateUtil(self.config)
        output = import_runner.run(ctx, params)
        #END run_phanotate

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_phanotate return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def run_phate(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_phate
        #END run_phate

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_phate return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
