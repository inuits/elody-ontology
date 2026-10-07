"""Checks the vocabulary and its meta-shapes; run before every release.

    python scripts/check.py

Needs rdflib and pyshacl. Fails (exit 1) when:
  - a file does not parse;
  - a class or property has no rdfs:label or rdfs:comment, a term or individual
    no rdfs:isDefinedBy, a property more than one rdfs:domain, or a property is
    both a data/object property and an annotation property (OWL 2 DL);
  - the meta-shapes are not valid SHACL (checked against SHACL-SHACL);
  - the declarations in tests/fixtures do not conform to the meta-shapes, read
    with this vocabulary alone (no implementation bindings).
"""

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parent.parent
ELODY = Namespace("https://elody.eu/ns/ui#")
ONTOLOGY = URIRef("https://elody.eu/ns/ui")

problems = []
vocabulary = Graph().parse(ROOT / "ontology" / "elody-ui.ttl")
shapes = Graph().parse(ROOT / "ontology" / "elody-ui.shapes.ttl")

kinds = [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty, OWL.DeprecatedProperty]
terms = {s for kind in kinds for s in vocabulary.subjects(RDF.type, kind) if str(s).startswith(str(ELODY))}
for term in sorted(terms):
    name = term.removeprefix(str(ELODY))
    if not vocabulary.value(term, RDFS.label):
        problems.append(f"elody:{name} has no rdfs:label")
    if not vocabulary.value(term, RDFS.comment) and (term, RDF.type, OWL.DeprecatedProperty) not in vocabulary:
        problems.append(f"elody:{name} has no rdfs:comment")
    if len(set(vocabulary.objects(term, RDFS.domain))) > 1:
        problems.append(f"elody:{name} has more than one rdfs:domain")
    types = set(vocabulary.objects(term, RDF.type))
    if OWL.AnnotationProperty in types and types & {OWL.ObjectProperty, OWL.DatatypeProperty}:
        problems.append(f"elody:{name} is both an annotation and a data/object property")
for subject in {s for s in vocabulary.subjects() if str(s).startswith(str(ELODY))}:
    if (subject, RDFS.isDefinedBy, ONTOLOGY) not in vocabulary:
        problems.append(f"elody:{subject.removeprefix(str(ELODY))} has no rdfs:isDefinedBy <{ONTOLOGY}>")

for fixture in sorted((ROOT / "tests" / "fixtures").glob("*.ui.ttl")):
    # the vocabulary is merged into the data graph so sh:class sees the enumeration individuals
    data = Graph().parse(ROOT / "ontology" / "elody-ui.ttl").parse(fixture)
    conforms, _, report = validate(
        data,
        shacl_graph=shapes,
        inference="none",
        meta_shacl=True,
        allow_warnings=True,
    )
    if not conforms:
        problems.append(f"{fixture.name} does not conform:\n{report}")

print(f"{len(terms)} terms, {len(vocabulary)} triples, {len(shapes)} shape triples")
for problem in problems:
    print("FAIL", problem)
sys.exit(1 if problems else 0)
