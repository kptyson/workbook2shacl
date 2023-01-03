from util import ts, cli
from graph_setup import load_graph, serialize
from workbook_processing import process_workbook

if __name__ == '__main__':
    args = cli()
    ontology_uri, default_namespace = load_graph(args.input_ontology)
    process_workbook(args, ontology_uri, default_namespace)
    serialize(args.output_ontology)
    print(ts(), 'Done')
