from rdflib import ConjunctiveGraph, URIRef, Namespace
from pathlib import Path
from util import ts


cg = ConjunctiveGraph()
sg = cg.get_context(URIRef('#Schema'))


def serialize(ttl_file: Path) -> None:
    """
    Serialize enriched grapg

    :param ttl_file: File to create
    :return: None
    """
    print(ts(), 'Serializing to', ttl_file)
    sg.serialize(ttl_file, format='turtle')

def load_graph(ttl_file: Path) -> (URIRef, Namespace):
    """
    Load the input turtle file into the RDF graph
    :param ttl_file:
    :return: URIRef of the ontology and the default namespace
    """
    ontology_uri = None
    default_namespace = None
    print(ts(), 'Reading', ttl_file)
    sg.parse(ttl_file, format='turtle')
    result_set = sg.query('''
select ?ontology_uri ?default_namespace where {?ontology_uri a owl:Ontology ; 
        <http://topbraid.org/swa#defaultNamespace> ?default_namespace }
''')
    for res in result_set:
        ontology_uri = res.ontology_uri
        default_namespace = res.default_namespace
        break
    return ontology_uri, Namespace(default_namespace)


