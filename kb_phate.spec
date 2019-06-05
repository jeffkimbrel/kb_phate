/*
A KBase module: kb_phate
*/

module kb_phate {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */

    funcdef run_phanotate(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

    funcdef run_phate(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
