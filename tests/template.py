from . import ingest_tester
from whyis.test.agent_unit_test_case import AgentUnitTestCase


class IngestTestSetup(AgentUnitTestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting Up Class")
        cls.maxDiff = None
        cls.expected_data = ingest_tester.autoparse(cls.file_under_test)

    def setUp(self):
        ingest_tester.setUp(self, self.file_under_test)

    def run_agent(self, agent, nanopublication=None):
        app = self.app
        agent.dry_run = True
        agent.app = app
        results = []
        if nanopublication is not None:
            results.extend(agent.process_graph(nanopublication))
        elif agent.query_predicate == app.NS.whyis.globalChangeQuery:
            results.extend(agent.process_graph(app.db))
        else:
            print("Running as update agent")
            for resource in agent.getInstances(app.db):
                print(resource.identifier)
                for np_uri, in app.db.query('''select ?np where {
    graph ?assertion { ?e ?p ?o.}
    ?np a np:Nanopublication;
        np:hasAssertion ?assertion.
}''', initBindings={'e': resource.identifier}, initNs=app.NS.prefixes):
                    print(np_uri)
                    np = app.nanopub_manager.get(np_uri)
                    results.extend(agent.process_graph(np))
        return results

class IngestTestTests(IngestTestSetup):  
    def test_nanocomposites(self):
        ingest_tester.test_nanocomposites(self)

    def test_authors(self):
        ingest_tester.test_authors(self, self.expected_data["authors"])

    def test_language(self):
        ingest_tester.test_language(self, self.expected_data["language"])

    def test_keywords(self):
        ingest_tester.test_keywords(self, self.expected_data["keywords"])

    def test_devices(self):
        ingest_tester.test_devices(self, self.expected_data["equipment"])

    def test_volume(self):
        ingest_tester.test_volume(self, self.expected_data["journ_vol"])

    def test_matrix_chemical_names(self):
        ingest_tester.test_matrix_chemical_names(self)

    def test_matrix_trade_names(self):
        ingest_tester.test_matrix_trade_names(self)

    def test_filler_chemical_names(self):
        ingest_tester.test_filler_chemical_names(self)

    def test_filler_trade_names(self):
        ingest_tester.test_filler_trade_names(self)

    # TODO Fix or remove
    def test_temperatures(self):
        ingest_tester.test_temperatures(self)

    def test_abbreviations(self):
        ingest_tester.test_abbreviations(self)

    def test_manufacturers(self):
        ingest_tester.test_manufacturers(self)

    def test_complete_material(self):
        ingest_tester.test_complete_material(self)

    # TODO Fix or remove
    def test_filler_processing(self):
        ingest_tester.test_filler_processing(self)

    def test_viscoelastic_measurement_mode(self):
        ingest_tester.test_viscoelastic_measurement_mode(self)

    # TODO add the following tests once completed
        # test_stress
        # test_melt_viscosity
        # test_rheometer_mode
        # test_specific_surface_area
        # test_dielectric_real_permittivity
