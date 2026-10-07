# elody-ontology

The ontologies of the Elody platform, in RDF: the terms in which Elody is
described declaratively, and the shapes that say what a valid description
looks like. Redmine epic #165964.

| Directory | Ontology | Namespace | Status |
|---|---|---|---|
| `ui/` | the **UI declaration vocabulary**: an entity's interface — listings, view modes, panels, forms, filters, actions, flows, linked-data sources, Elody's widgets — layered on W3C SHACL 1.2 UI (`shui:`) and DASH (`dash:`) | `https://elody.eu/ns/ui#` (`elody:`) | 0.2.0 |
| — | the **backend object configuration**: what collection-api's object configurations say in Python today (CRUD behaviour, validation, hooks, serialisation, storage) | to be chosen | next phase |

Each ontology has its own directory, namespace and version, and comes with
meta-shapes: SHACL shapes a description must conform to.

## ui/ — the UI declaration vocabulary

A UI declaration describes an entity's interface in RDF: what its properties
are (`sh:`), how they are edited and viewed (`shui:`), what shui does not say
(`dash:`), and what only Elody knows (`elody:`). A term lives in `elody:` only
when no `sh:`, `shui:` or `dash:` term carries the meaning, and its
`rdfs:comment` says why.

| File | What it is |
|---|---|
| `ui/elody-ui.ttl` | the vocabulary: an OWL ontology in Turtle (`<https://elody.eu/ns/ui>`, `owl:versionIRI`, imports shui and dash). Classes and properties with label, comment, domain and range; enumerations as individuals; retired terms as `owl:DeprecatedProperty` with `dcterms:isReplacedBy`; every term `rdfs:isDefinedBy` the ontology. |
| `ui/elody-ui.shapes.ttl` | the meta-shapes: SHACL Core shapes for a valid declaration. A retired term fails with its replacement in the message. Validate with the vocabulary merged into the data graph, so `sh:class` sees the enumeration individuals. |
| `tests/fixtures/ui/*.ui.ttl` | declarations that must conform (DiSHACLed's). |

How Elody *implements* the vocabulary — the literal of an enumeration in the
GraphQL schema, the PWA widget an editor renders as, the schema field of an
element — changes with the platform, not with the vocabulary. Those bindings
live with the generator, [`elody-generator`](https://github.com/inuits/elody-generator)
(`ontology/elody-ui.bindings.ttl`), which turns declarations into the GraphQL
documents the PWA renders. A declaration never states them, and validation
does not need them.

## Check

```bash
pip install rdflib pyshacl
python scripts/check.py
```

Fails when a file does not parse; a term lacks a label, a comment or
`rdfs:isDefinedBy`; a property has two domains or is both a data/object and an
annotation property (OWL 2 DL); the meta-shapes are not valid SHACL
(SHACL-SHACL); or a fixture does not conform, read with the vocabulary alone.

## Versions

Each ontology is versioned on its own, with semantic versioning in
`owl:versionInfo` and `owl:versionIRI` (`https://elody.eu/ns/ui/<version>`); the
package version follows the highest change. A new term is a minor version;
retiring a term (it stays, deprecated, with its replacement) is a minor version;
removing a retired term is a major version. `owl:priorVersion` links each
version to the one before.

## Publishing (to do)

Each namespace should answer with its Turtle for RDF clients (`text/turtle`)
and with generated HTML documentation (pyLODE or Widoco) for browsers, each
version at its `owl:versionIRI`. Until then the namespace IRIs do not resolve.

## Using it

Consumers read the files from the installed package (`elody-ontology/ui/…`).
`elody-generator` depends on a tagged version (`github:inuits/elody-ontology#v0.2.0`);
to try an unreleased change it reads a checkout through `ELODY_ONTOLOGY`, or this
checkout next to it at the root of elody-common.

## License

MIT, see `LICENSE`.
