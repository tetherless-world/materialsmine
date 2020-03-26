import rdflib

from whyis.test.agent_unit_test_case import AgentUnitTestCase
from base64 import b64encode
import autonomic

class IngestTest(AgentUnitTestCase):

    upload_template = '''<https://materialsmine.org/nmr/xml/example> a <http://nanomine.org/ns/NanomineXMLFile>,
        <http://schema.org/DataDownload>,
        <https://www.iana.org/assignments/media-types/text/xml> ;
    <http://vocab.rpi.edu/whyis/hasContent> "data:text/xml;charset=UTF-8;base64,%s" .'''

    def setUp(self):
        # Initialization
        self.login(*self.create_user("user@example.com", "password"))

        encoded_file = b64encode(self.data.encode('utf8')).decode('ascii')

        print ("XML length:", len(encoded_file))
        upload = self.upload_template % (encoded_file)
        response = self.client.post("/pub", data=upload, content_type="text/turtle", follow_redirects=True)
        self.assertEquals(response.status, '201 CREATED')

        response = self.client.post("/pub", data=open('/apps/nanomine-graph/setl/xml_ingest.setl.ttl', 'rb').read(),
                                      content_type="text/turtle", follow_redirects=True)
        self.assertEquals(response.status, '201 CREATED')

        setlmaker = autonomic.SETLMaker()
        setlmaker.dry_run = False
        results = self.run_agent(setlmaker)

        # confirm this is creating a SETL script for the XML file.
        self.assertTrue(len(results) > 0)

        setlr = autonomic.SETLr()
        setlr.dry_run = False

        print(len(self.app.db))
        for setlr_np in results:
            setlr_results = self.run_agent(setlr, nanopublication=setlr_np)

class TestChemicalNames(IngestTest):

    data = '''<?xml version="1.0" encoding="UTF-8"?>
    <PolymerNanocomposite>
      <ID>L101_S3_Dang_2007</ID>
      <MATERIALS>
        <Matrix>
          <MatrixComponent>
            <ChemicalName>bisphenol A epoxy resin</ChemicalName>
            <StdChemicalName>DGEBA Epoxy Resin</StdChemicalName>
            <uSMILES>CC(C)(C1=CC=C(OCC2CO2)C=C1)C3=CC=C(OCC4CO4)C=C3</uSMILES>
            <Abbreviation>EPR</Abbreviation>
            <ManufacturerOrSourceName>Dow chemical</ManufacturerOrSourceName>
            <TradeName>DER661</TradeName>
          </MatrixComponent>
        </Matrix>
        <Filler>
          <FillerComponent>
            <ChemicalName>barium titanate</ChemicalName>
            <StdChemicalName>Barium titanate</StdChemicalName>
            <Abbreviation>BaTiO3</Abbreviation>
            <ManufacturerOrSourceName>Guoteng electronic ceramic company</ManufacturerOrSourceName>
            <ParticleSurfaceTreatment>
              <ChemicalName>silane coupling agent</ChemicalName>
              <Abbreviation>KH550</Abbreviation>
            </ParticleSurfaceTreatment>
            <ParticleSurfaceTreatment>
              <ChemicalName>phosphated ester</ChemicalName>
              <Abbreviation>BYK-9010</Abbreviation>
            </ParticleSurfaceTreatment>
          </FillerComponent>
        </Filler>
      </MATERIALS>
    </PolymerNanocomposite>'''

    def test_chemprops_id(self):
        print (len(self.app.db))
        component_types = set(self.app.db.query('''
            SELECT ?parttype ?role WHERE {
                ?sample a <http://nanomine.org/ns/PolymerNanocomposite>.
                ?sample <http://semanticscience.org/resource/hasComponentPart>/<http://semanticscience.org/resource/isSurroundedBy>? ?part.
                ?part a ?parttype;
                    <http://semanticscience.org/resource/hasRole> [
                        a ?role;
                        <http://semanticscience.org/resource/inRelationTo> ?sample
                    ].
            }'''))
        print ('\n'.join(['\t'.join(x) for x in component_types]))
        self.assertTrue((rdflib.URIRef('http://nanomine.org/compound/BariumTitanate'),
                  rdflib.URIRef('http://nanomine.org/ns/Filler')), component_types)

        self.assertIn((rdflib.URIRef('http://nanomine.org/compound/DgebaEpoxyResin'),
                  rdflib.URIRef('http://nanomine.org/ns/Matrix')), component_types)
