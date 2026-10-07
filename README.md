# elody-ui-ontology

The vocabulary of an Elody UI declaration: the `elody:` terms
(`https://elody.eu/ns/ui#`), layered on the W3C **SHACL 1.2 UI** vocabulary
(`shui:`) and **DASH** (`dash:`), and the **meta-shapes** a declaration must
conform to. Redmine epic #165964.

A declaration describes an entity's interface in RDF: what its properties are
(`sh:`), how they are edited and viewed (`shui:`), what shui does not say
(`dash:`), and what only the Elody platform knows (`elody:` — listings, view
modes, panels, filters, actions, flows, linked-data sources, and Elody's own
widgets as `shui:Editor` / `shui:Viewer` instances). A term lives in `elody:`
only when no `sh:`, `shui:` or `dash:` term carries the meaning, and its
`rdfs:comment` says why.

## Contents

| File | What it is |
|---|---|
| `ontology/elody-ui.ttl` | the vocabulary: an OWL ontology in Turtle (`<https://elody.eu/ns/ui>`, `owl:versionIRI`, imports shui and dash). Classes and properties with label, comment, domain and range; enumerations as individuals; retired terms as `owl:DeprecatedProperty` with `dcterms:isReplacedBy`; every term `rdfs:isDefinedBy` the ontology. |
| `ontology/elody-ui.shapes.ttl` | the meta-shapes: SHACL Core shapes for a valid declaration. A retired term fails with its replacement in the message. Validate a declaration with the vocabulary merged into its data graph, so `sh:class` sees the enumeration individuals. |
| `tests/fixtures/*.ui.ttl` | declarations that must conform (DiSHACLed's). |
| `scripts/check.py` | the release check (below). |

## What is not here

How Elody *implements* the vocabulary — the literal of an enumeration in the
GraphQL schema, the PWA widget an editor renders as, the schema field of an
element — changes with the platform, not with the vocabulary. Those bindings
live with the generator, in `uiDeclarationModule`
(`ontology/elody-ui.bindings.ttl`), which reads both files. A declaration never
states them, and validation does not need them.

## Check

```bash
pip install rdflib pyshacl
python scripts/check.py
```

Fails when a file does not parse; a term lacks a label, a comment or
`rdfs:isDefinedBy`; a property has two domains or is both a data/object and an
annotation property (OWL 2 DL); the meta-shapes are not valid SHACL
(SHACL-SHACL); or a fixture does not conform, read with this vocabulary alone.

## Versions

Semantic versioning, in `owl:versionInfo`, `owl:versionIRI`
(`https://elody.eu/ns/ui/<version>`) and `package.json` together. A new term is
a minor version; retiring a term (it stays, deprecated, with its replacement) is
a minor version; removing a retired term is a major version.
`owl:priorVersion` links each version to the one before.

## Publishing (to do)

The namespace `https://elody.eu/ns/ui` should answer with this file for RDF
clients (`text/turtle`) and with generated HTML documentation (pyLODE or
Widoco) for browsers, each version at its `owl:versionIRI`. Until then the
namespace IRI does not resolve.

## License

MIT, see `LICENSE`.
