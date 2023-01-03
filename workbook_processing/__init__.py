from graph_setup import sg
from util import ts, ct
import argparse
import pandas as pd
from rdflib import URIRef, Namespace, RDF, RDFS, OWL, Literal, SH, XSD


def process_workbook(args: argparse.Namespace,
                     ontology_uri: URIRef,
                     ns : Namespace) -> None:
    """
    Create SHACL elements from the workbook

    :param ns: RDF namespace to use for newly created elements
    :param ontology_uri: URI of the ontology to enrich
    :param args: command line arguments
    :return: None
    """
    wb_name = args.xlsx.name
    wb_uri = URIRef(ns+ct(wb_name))
    sg.add((wb_uri, RDF.type, OWL.Class))
    sg.add((wb_uri, RDF.type, SH.NodeShape))
    sg.add((wb_uri, RDFS.subClassOf, OWL.Thing))
    sg.add((wb_uri, RDFS.label, Literal(wb_name)))
    sg.add((wb_uri, RDFS.comment, Literal('Harvested from '+str(wb_name))))
    print(ts(),'Reading', args.xlsx)
    dfl = pd.read_excel(args.xlsx, sheet_name=None, dtype=object)
    for ws_name in dfl:
        if ws_name in args.exclude:
            continue
        if args.include is not None:
            if ws_name not  in args.include:
                continue
        ws_uri = URIRef(ns+ct(ws_name))
        sg.add((ws_uri, RDF.type, OWL.Class))
        sg.add((ws_uri, RDF.type, SH.NodeShape))
        sg.add((ws_uri, RDFS.label, Literal(ws_name)))
        sg.add((ws_uri, RDFS.comment,
                Literal('Harvested from {b}:{s}'.format(b=wb_name, s=ws_name))))
        sg.add((ws_uri, RDFS.subClassOf, wb_uri))
        pg_name = ws_name+' Property Group'
        pg_uri = URIRef(ns+ct(pg_name))
        sg.add((pg_uri, RDF.type, SH.PropertyGroup))
        sg.add((pg_uri, RDFS.label, Literal(pg_name)))
        sg.add((pg_uri, RDFS.label, Literal('Harvested from {b}:{s}'.format(b=wb_name, s=ws_name))))
        for col_name in dfl[ws_name].columns:
            col_uri = URIRef(ns+ct(ws_name)+'-'+ct(col_name))
            path_uri = URIRef(ns+ct(col_name))
            sg.add((col_uri, RDF.type, SH.PropertyShape))
            sg.add((col_uri, SH.datatype, XSD.string))
            sg.add((col_uri, SH.description,
                    Literal('Harvested from {b}:{s}:{c}'.format(b=wb_name,
                                                                 s=ws_name,
                                                                 c=col_name))))
            sg.add((col_uri, SH.name, Literal(col_name)))
            sg.add((col_uri, SH.path, path_uri))
            sg.add((ws_uri, SH.property, col_uri))
            sg.add((col_uri, SH.group, pg_uri))

