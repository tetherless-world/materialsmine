import json
import requests
import tempfile
import xml.etree.ElementTree as ET
import pandas as pd
import rdflib
import slugify
import os

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import autonomic

disabled = []

files = {
    "template": '''<{}> a <http://nanomine.org/ns/NanomineXMLFile>,
        <http://schema.org/DataDownload>,
        <https://www.iana.org/assignments/media-types/text/xml> ;
    <http://vocab.rpi.edu/whyis/hasContent> "data:text/xml;charset=UTF-8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPFBvbHltZXJOYW5vY29tcG9zaXRlPjxJRD5MMTAyX1MzX0h1XzIwMDc8L0lEPjxDb250cm9sX0lEPkwxMDJfUzFfSHVfMjAwNzwvQ29udHJvbF9JRD48REFUQV9TT1VSQ0U+PENpdGF0aW9uPjxDb21tb25GaWVsZHM+PENpdGF0aW9uVHlwZT5yZXNlYXJjaCBhcnRpY2xlPC9DaXRhdGlvblR5cGU+PFB1YmxpY2F0aW9uPkpvdXJuYWwgb2YgdGhlIEV1cm9wZWFuIENlcmFtaWMgU29jaWV0eTwvUHVibGljYXRpb24+PFRpdGxlPkRpZWxlY3RyaWMgcHJvcGVydGllcyBvZiBCU1QvcG9seW1lciBjb21wb3NpdGU8L1RpdGxlPjxBdXRob3I+SHUsIFRhbzwvQXV0aG9yPjxBdXRob3I+SnV1dGksIEphcmk8L0F1dGhvcj48QXV0aG9yPkphbnR1bmVuLCBIZWxpPC9BdXRob3I+PEF1dGhvcj5WaWxrbWFuLCBUYWlzdG88L0F1dGhvcj48S2V5d29yZD5Db21wb3NpdGVzPC9LZXl3b3JkPjxLZXl3b3JkPkRpZWxlY3RyaWMgcHJvcGVydGllczwvS2V5d29yZD48S2V5d29yZD5NaWNyb3N0cnVjdHVyZS1maW5hbDwvS2V5d29yZD48S2V5d29yZD5CU1QtQ09DPC9LZXl3b3JkPjxQdWJsaXNoZXI+RWxzZXZpZXI8L1B1Ymxpc2hlcj48UHVibGljYXRpb25ZZWFyPjIwMDc8L1B1YmxpY2F0aW9uWWVhcj48RE9JPjEwLjEwMTYvai5qZXVyY2VyYW1zb2MuMjAwNy4wMi4wODI8L0RPST48Vm9sdW1lPjI3PC9Wb2x1bWU+PFVSTD5odHRwczovL3d3dy5zY2llbmNlZGlyZWN0LmNvbS9zY2llbmNlL2FydGljbGUvcGlpL1MwOTU1MjIxOTA3MDAxMjUyP3ZpYSUzRGlodWI8L1VSTD48TGFuZ3VhZ2U+RW5nbGlzaDwvTGFuZ3VhZ2U+PExvY2F0aW9uPk1pY3JvZWxlY3Ryb25pY3MgYW5kIE1hdGVyaWFscyBQaHlzaWNzIExhYm9yYXRvcmllcywgRU1QQVJUIFJlc2VhcmNoIEdyb3VwIG9mIEluZm90ZWNoIE91bHUsIFAuTy4gQm94IDQ1MDAsIEZJTi05MDAxNCBVbml2ZXJzaXR5IG9mIE91bHUsIEZpbmxhbmQ8L0xvY2F0aW9uPjxEYXRlT2ZDaXRhdGlvbj4yMDE1LTA3LTI0PC9EYXRlT2ZDaXRhdGlvbj48L0NvbW1vbkZpZWxkcz48Q2l0YXRpb25UeXBlPjxKb3VybmFsPjxJU1NOPjA5NTUtMjIxOTwvSVNTTj48SXNzdWU+MTMtMTU8L0lzc3VlPjwvSm91cm5hbD48L0NpdGF0aW9uVHlwZT48L0NpdGF0aW9uPjwvREFUQV9TT1VSQ0U+PE1BVEVSSUFMUz48TWF0cml4PjxNYXRyaXhDb21wb25lbnQ+PENoZW1pY2FsTmFtZT5jeWNsbyBvbGVmaW4gY29wb2x5bWVyPC9DaGVtaWNhbE5hbWU+PEFiYnJldmlhdGlvbj5DT0M8L0FiYnJldmlhdGlvbj48UG9seW1lclR5cGU+Y29wb2x5bWVyPC9Qb2x5bWVyVHlwZT48TWFudWZhY3R1cmVyT3JTb3VyY2VOYW1lPlRpY29uYSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PFRyYWRlTmFtZT5Ub3BhcyA4MDA3Uy0wNDwvVHJhZGVOYW1lPjxEZW5zaXR5Pjx2YWx1ZT4xLjAyPC92YWx1ZT48dW5pdD5nL2NtXjM8L3VuaXQ+PC9EZW5zaXR5PjwvTWF0cml4Q29tcG9uZW50PjwvTWF0cml4PjxGaWxsZXI+PEZpbGxlckNvbXBvbmVudD48Q2hlbWljYWxOYW1lPmJhcml1bSBzdHJvbnRpdW0gdGl0YW5hdGU8L0NoZW1pY2FsTmFtZT48QWJicmV2aWF0aW9uPkJTVDwvQWJicmV2aWF0aW9uPjxNYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+U2lnbWHigJNBbGRyaWNoIENoZW1pZSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PERlbnNpdHk+PHZhbHVlPjQuOTwvdmFsdWU+PHVuaXQ+Zy9jbV4zPC91bml0PjwvRGVuc2l0eT48U3BoZXJpY2FsUGFydGljbGVEaWFtZXRlcj48ZGVzY3JpcHRpb24+bGVzcyB0aGFuIDIwMCBubTwvZGVzY3JpcHRpb24+PHZhbHVlPjIwMDwvdmFsdWU+PHVuaXQ+bm08L3VuaXQ+PC9TcGhlcmljYWxQYXJ0aWNsZURpYW1ldGVyPjwvRmlsbGVyQ29tcG9uZW50PjxGaWxsZXJDb21wb3NpdGlvbj48RnJhY3Rpb24+PHZvbHVtZT4wLjA1PC92b2x1bWU+PC9GcmFjdGlvbj48L0ZpbGxlckNvbXBvc2l0aW9uPjxEZXNjcmlwdGlvbj5CYTAuNVNyMC41VGlPMzwvRGVzY3JpcHRpb24+PC9GaWxsZXI+PC9NQVRFUklBTFM+PFBST0NFU1NJTkc+PE1lbHRNaXhpbmc+PENob29zZVBhcmFtZXRlcj48TWl4aW5nPjxNaXhlcj5Ub3JxdWUgUmhlb21ldGVyPC9NaXhlcj48UlBNPjxkZXNjcmlwdGlvbj4zMi02NCBycG08L2Rlc2NyaXB0aW9uPjx2YWx1ZT40ODwvdmFsdWU+PHVuaXQ+cnBtPC91bml0PjwvUlBNPjxUaW1lPjx2YWx1ZT4xNTwvdmFsdWU+PHVuaXQ+bWludXRlczwvdW5pdD48dW5jZXJ0YWludHk+PHR5cGU+YWJzb2x1dGU8L3R5cGU+PHZhbHVlPjU8L3ZhbHVlPjwvdW5jZXJ0YWludHk+PC9UaW1lPjxUZW1wZXJhdHVyZT48dmFsdWU+MjMwPC92YWx1ZT48dW5pdD5DZWxzaXVzPC91bml0PjwvVGVtcGVyYXR1cmU+PC9NaXhpbmc+PC9DaG9vc2VQYXJhbWV0ZXI+PENob29zZVBhcmFtZXRlcj48TW9sZGluZz48TW9sZGluZ01vZGU+aG90LXByZXNzaW5nPC9Nb2xkaW5nTW9kZT48TW9sZGluZ0luZm8+PFRlbXBlcmF0dXJlPjx2YWx1ZT4yMDA8L3ZhbHVlPjx1bml0PkNlbHNpdXM8L3VuaXQ+PC9UZW1wZXJhdHVyZT48L01vbGRpbmdJbmZvPjwvTW9sZGluZz48L0Nob29zZVBhcmFtZXRlcj48L01lbHRNaXhpbmc+PC9QUk9DRVNTSU5HPjxDSEFSQUNURVJJWkFUSU9OPjxTY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxFcXVpcG1lbnRVc2VkPkpFT0wgSlNNLTY0MDA8L0VxdWlwbWVudFVzZWQ+PC9TY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxEaWVsZWN0cmljX2FuZF9JbXBlZGFuY2VfU3BlY3Ryb3Njb3B5X0FuYWx5c2lzPjxFcXVpcG1lbnQ+QWdpbGVudCBFNDk5MUE8L0VxdWlwbWVudD48L0RpZWxlY3RyaWNfYW5kX0ltcGVkYW5jZV9TcGVjdHJvc2NvcHlfQW5hbHlzaXM+PFhSYXlfRGlmZnJhY3Rpb25fYW5kX1NjYXR0ZXJpbmc+PEVxdWlwbWVudD5TaWVtZW5zIEQ1MDAwPC9FcXVpcG1lbnQ+PC9YUmF5X0RpZmZyYWN0aW9uX2FuZF9TY2F0dGVyaW5nPjwvQ0hBUkFDVEVSSVpBVElPTj48UFJPUEVSVElFUz48RWxlY3RyaWNhbD48QUNfRGllbGVjdHJpY0Rpc3BlcnNpb24+PERpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PGRlc2NyaXB0aW9uPlJlbGF0aXZlIHBlcm1pdHRpdml0eSBhdCAxR0h6PC9kZXNjcmlwdGlvbj48dmFsdWU+Mi45PC92YWx1ZT48L0RpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PERpZWxlY3RyaWNfTG9zc19UYW5nZW50PjxkZXNjcmlwdGlvbj5Mb3NzIFRhbmdlbnQgYXQgMSBHSHo8L2Rlc2NyaXB0aW9uPjx2YWx1ZT41ZS0wNTwvdmFsdWU+PC9EaWVsZWN0cmljX0xvc3NfVGFuZ2VudD48L0FDX0RpZWxlY3RyaWNEaXNwZXJzaW9uPjwvRWxlY3RyaWNhbD48L1BST1BFUlRJRVM+PC9Qb2x5bWVyTmFub2NvbXBvc2l0ZT4=" .'''
}


def get_remote_xml(file_under_test):
    """ Given an nanomine file returns the xml string """
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504], raise_on_redirect=True, raise_on_status=True)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    response = s.get('https://materialsmine.org/nmr/xml/' + file_under_test + '.xml', timeout=5)
    j = json.loads(response.text)
    xml_str = j["data"][0]["xml_str"]
    return xml_str


def get_local_xml(file_under_test):
    """ Attempts to load a given file from the local /tests/xml/ folder """
    file_under_test += ".xml"
    test_folder_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(test_folder_path, "xml", file_under_test)
    with open(file_path) as f:
        return f.read()   

def get_xml(file_under_test):
    try:
        return get_local_xml(file_under_test)
    except FileNotFoundError:
        print("File not found locally, loading from server...")
        return get_remote_xml(file_under_test)

def disable_test(func):
    disabled.append(func.__name__)
    print(func.__name__, "is disabled and will not run")
    def disable(*args, **kwargs):
        print(func.__name__, "has been disabled")
    return disable


def setUp(runner, file_under_test):
    # Skip setting up disabled tests
    if os.getenv("CI") is not None:
        if runner._testMethodName in disabled:
            print("Skipping test", str(runner._testMethodName), "in CI since it is disabled")
            return
    # Initialization
    runner.login(*runner.create_user("user@example.com", "password"))

    with tempfile.NamedTemporaryFile() as temp:
        xml_str = get_xml(file_under_test)
        temp.write(xml_str.encode("utf-8"))
        temp.seek(0)


        files[file_under_test] = files["template"].format(temp.name)
        upload = files[file_under_test]

        response = runner.client.post(
            "/pub", data=upload, content_type="text/turtle", follow_redirects=True)
        runner.assertEquals(response.status, '201 CREATED')

        response = runner.client.post("/pub", data=open('/apps/nanomine-graph/setl/xml_ingest.setl.ttl', 'rb').read(),
                                    content_type="text/turtle", follow_redirects=True)
        runner.assertEquals(response.status, '201 CREATED')

        setlmaker = autonomic.SETLMaker()
        results = runner.run_agent(setlmaker)

        # confirm this is creating a SETL script for the XML file.
        runner.assertTrue(len(results) > 0)

        setlr = autonomic.SETLr()

        print(len(runner.app.db))
        for setlr_np in results:
            setlr_results = runner.run_agent(setlr, nanopublication=setlr_np)


def query_table(runner, dependentVar, independentVar,
                measurement_description=None, x_description=None, y_description=None):
    
    if measurement_description is not None:
        measurement_description = '?sample <http://purl.org/dc/elements/1.1/Description> "{}" .'.format(measurement_description)
    else:
        measurement_description = ""

    if x_description is not None:
        x_description = '?independentVarNode <http://purl.org/dc/elements/1.1/Description> "{}" .'.format(x_description)
    else:
        x_description = ""

    if y_description is not None:
        y_description = '?dependentVarNode <http://purl.org/dc/elements/1.1/Description> "{}" .'.format(y_description)
    else:
        y_description = ""
    


    query = """
        SELECT ?dependentVar ?independentVar
        WHERE {{
            ?sample <http://semanticscience.org/resource/hasAttribute> ?dependentVarNode .
            ?dependentVarNode a {} .
            ?dependentVarNode <http://semanticscience.org/resource/hasValue> ?dependentVar .
            ?dependentVarNode <http://semanticscience.org/resource/inRelationTo> ?independentVarNode .
            ?independentVarNode a {} .
            ?independentVarNode <http://semanticscience.org/resource/hasValue> ?independentVar .
            {}
            {}
            {}
        }}
    """.format(dependentVar, independentVar, measurement_description, x_description, y_description)
    # print(query)
    values = runner.app.db.query(query)
    return values


def autoparse(file_under_test):
    # Parses out information from the specified file for verification the the correct data
    # ends up in the graph
    with tempfile.TemporaryFile() as temp:
        xml_str = get_remote_xml(file_under_test)
        temp.write(xml_str.encode('utf-8'))
        temp.seek(0)
        tree = ET.parse(temp)
    
        root = tree.getroot()
        expected_data = dict()
        # CommonFields Data
        # common_fields = next(root.iter("CommonFields"))
        expected_data["authors"] = [
            elem.text for elem in root.findall(".//CommonFields//Author")]
        expected_data["keywords"] = [elem.text.title()
                                    for elem in root.findall(".//CommonFields//Keyword")]
        expected_data["DOI"] = [elem.text.title()
                                for elem in root.findall(".//CommonFields//DOI")]
        expected_data["language"] = ["http://nanomine.org/language/" + elem.text.lower()
                                    for elem in root.findall(".//CommonFields//Language")]
        expected_data["journ_vol"] = [
            rdflib.Literal(int(val.text)) for val in root.findall(".//CommonFields//Volume")]

        # Matrix Data
        # matrix_data = next(root.iter("Matrix"))
        expected_data["m_name"] = [rdflib.Literal(elem.text)
                                for elem in root.findall(".//Matrix//ChemicalName")]
        expected_data["m_trd_name"] = [
            rdflib.Literal(elem.text) for elem in root.findall(".//Matrix//TradeName")]
        expected_data["abbrev"] = [rdflib.Literal(elem.text)
                                for elem in root.findall(".//Matrix//Abbreviation")]
        expected_data["manufac"] = [
            rdflib.Literal(elem.text) for elem in root.findall(".//Matrix//ManufacturerOrSourceName")]
        expected_data["specific_surface_area"] = [
            rdflib.Literal(elem.text, datatype=rdflib.XSD.double) for elem in root.findall(".//Matrix//SurfaceArea/specific/value")]
        expected_data["specific_surface_area_units"] = [
            rdflib.Literal(elem.text) for elem in root.findall(".//Matrix//SurfaceArea/specific/unit")]

        # Filler data
        # filler_data = next(root.iter("Filler"))
        expected_data["f_name"] = [rdflib.Literal(elem.text)
                                for elem in root.findall(".//Filler//ChemicalName")]
        expected_data["f_trd_name"] = [
            rdflib.Literal(elem.text) for elem in root.findall(".//Filler//TradeName")]
        expected_data["abbrev"] += [rdflib.Literal(elem.text)
                                    for elem in root.findall(".//Filler//Abbreviation")]
        expected_data["manufac"] += [rdflib.Literal(elem.text)
                                    for elem in root.findall(".//Filler//ManufacturerOrSourceName")]
        expected_data["specific_surface_area"] += [
            rdflib.Literal(elem.text, datatype=rdflib.XSD.double) for elem in root.findall(".//Filler//SurfaceArea/specific/value")]
        expected_data["specific_surface_area_units"] += [
            rdflib.Literal(elem.text) for elem in root.findall(".//Filler//SurfaceArea/specific/unit")]

        #Viscoleastic Properties,hardness, hardnessteststandard - Neha
        expected_data["viscoelastic_measurement_mode"] = [rdflib.Literal(elem.text)
                                        for elem in root.iter(".//Viscoelastic//MeasurementMode")]   
        
        expected_data["hardness"] = [rdflib.Literal(elem.text)
                                    for elem in root.iter("Hardness")]
        
        expected_data["hardnessteststandard"] = [rdflib.Literal(elem.text)
                                                for elem in root.iter(".//HardnessTestStandard")]

        expected_data["melt_viscosity_values"] = [rdflib.Literal(elem.text)
                                                for elem in root.iter("Author")]


        # Check that matrix and filler components are properly constructed
        def build_component_dict(component):
            material = dict()
            material["name"] = component.find(".//ChemicalName")
            material["abbrev"] = component.find(".//Abbreviation")
            material["manufac"] = component.find(".//ManufacturerOrSourceName")
            material["trade"] = component.find(".//TradeName")
            for key, value in material.items():
                if value is not None:
                    material[key] = rdflib.Literal(material[key].text)
            return material

        expected_data["compiled_material"] = [build_component_dict(
            component) for component in root.findall(".//MatrixComponent")]
        expected_data["compiled_material"] += [build_component_dict(
            component) for component in root.findall(".//FillerComponent")]

        def extract_choose_parameter(section):
            if section is None:
                return None
            order = list()
            for param in section.findall(".//ChooseParameter"):
                for component in param:
                    order.append(component.tag)
            return order

        expected_data["filler_processing"] = extract_choose_parameter(root.find(".//FillerProcessing"))
        expected_data["solution_processing"] = extract_choose_parameter(root.find(".//SolutionProcessing"))

        # Table data

        def extract_table_data(data_tag):
            if data_tag is None:
                return None
            if data_tag.find("data") is None:
                return None
            table = dict()  # Holds the description, headers, and dataframe
            table["description"] = data_tag.find(".//description").text
            table["headers"] = [elem.text for elem in data_tag.find(
                ".//headers").iter("column")]
            data = dict()
            for i, category in enumerate(table["headers"]):
                data[category] = data_tag.find(
                    ".//rows").findall("row/column[@id='" + str(i) + "']")
                data[category] = [float(elem.text) for elem in data[category]]

            table["data"] = pd.DataFrame(data)
            return table

        expected_data["Dielectric_Real_Permittivity"] = [extract_table_data(
            data) for data in root.iter("Dielectric_Real_Permittivity")]
        expected_data["Dielectric_Loss_Permittivity"] = [extract_table_data(
            data) for data in root.iter("Dielectric_Loss_Permittivity")]
        expected_data["Dielectric_Loss_Tangent"] = [extract_table_data(
            data) for data in root.iter("Dielectric_Loss_Tangent")]
        expected_data["ElectricConductivity"] = [extract_table_data(
            data) for data in root.iter("ElectricConductivity")]

        # Other Data
        expected_data["equipment"] = [elem.text.lower()
                                    for elem in root.iter("EquipmentUsed")]
        expected_data["equipment"] += [elem.text.lower()
                                    for elem in root.iter("Equipment")]
        expected_data["equipment"] = ["http://nanomine.org/ns/" + slugify.slugify(elem)
                                    for elem in expected_data["equipment"]]
        expected_data["values"] = [
            rdflib.Literal(val.text, datatype=rdflib.XSD.double) for val in root.iter("value")]

        expected_data["temps"] = []
        for node in root.iter("Temperature"):
            expected_data["temps"] += [rdflib.Literal(val.text, datatype=rdflib.XSD.double)
                                    for val in node.iter("value")]
        return expected_data


def test_nanocomposites(runner):
    # Ensure there is a nanocomposite in the graph
    nanocomposites = list(runner.app.db.subjects(
        rdflib.RDF.type, rdflib.URIRef("http://nanomine.org/ns/PolymerNanocomposite")))
    print(nanocomposites, len(runner.app.db))
    runner.assertEquals(len(nanocomposites), 1)
    print("Correct Number of Nanocomposites")


def test_authors(runner, expected_authors=None):
    # Ensure that the proper number of authors are in the graph
    print("\n\nauthors")
    authors = runner.app.db.query(
        """SELECT ?name 
    WHERE {
        ?paper <http://purl.org/dc/terms/creator> ?author .
        ?author <http://xmlns.com/foaf/0.1/name> ?name .
    }
    """
    )
    # for author in authors:
    # print(author)
    authors = [str(author[0]) for author in authors]
    if expected_authors is None:
        expected_authors = runner.expected_data["authors"]
    runner.assertCountEqual(expected_authors, authors)
    print("Expected Authors Found")


def test_language(runner, expected_language=None):
    # Ensure the paper is marked as being in English
    languages = list(runner.app.db.objects(
        None, rdflib.URIRef("http://purl.org/dc/terms/language")))
    print("\n\nLanguage")
    processed_langs = [str(language) for language in languages]
    # print(processed_langs)
    if expected_language is None:
        expected_language = runner.expected_data["language"]
    runner.assertCountEqual(expected_language, processed_langs)
    print("Correct Language")


def test_keywords(runner, expected_keywords=None):
    # Check how many keywords exist
    print("\n\nKeywords")
    keywords_lst = list(runner.app.db.objects(
        None, rdflib.URIRef("http://www.w3.org/ns/dcat#keyword")))
    keywords = [str(keyword) for keyword in keywords_lst]
    # print(keywords)
    if expected_keywords is None:
        expected_keywords = runner.expected_data["keywords"]
    runner.assertCountEqual(expected_keywords, keywords)
    print("Expected Keywords Found")


def test_devices(runner, expected_devices=None):
    # Check if all used devices are showing up
    print("\n\nDevices")
    devices_lst = list(runner.app.db.subjects(rdflib.URIRef(
        "http://www.w3.org/2000/01/rdf-schema#subClassOf"), rdflib.URIRef("http://semanticscience.org/resource/Device")))
    devices_lst = [str(device) for device in devices_lst]
    if expected_devices is None:
        expected_devices = runner.expected_data["equipment"]
    runner.assertCountEqual(expected_devices, devices_lst)
    print("Expected Devices Found")


def test_volume(runner, expected_volume=None):
    # Checks the volume of the journal
    print("Journal Volume")
    volume = runner.app.db.query(
        """
    SELECT ?volume
    WHERE {
        ?publication a <http://nanomine.org/ns/ResearchArticle> .
        ?publication <http://purl.org/ontology/bibo/volume> ?volume .
    }
    """
    )
    volume = [vol[0] for vol in volume]
    if expected_volume is None:
        expected_volume = runner.expected_data["journ_vol"]
    runner.assertCountEqual(expected_volume, volume)
    print("Expected Journal Volume Found")


def test_matrix_chemical_names(runner, expected_names=None):
    # Check if the names of the chemicals are present
    print("\n\nMatrix Chemical Names")
    names = runner.app.db.query(
        """
    SELECT ?chemName WHERE {
        ?matrix <http://semanticscience.org/resource/hasRole> ?bnode .
        ?matrix a ?chemURI .
        ?bnode a <http://nanomine.org/ns/Matrix> .
        ?chemURI <http://www.w3.org/2000/01/rdf-schema#label> ?chemName .
    }
    """
    )
    names = [name[0] for name in names]
    if expected_names is None:
        expected_names = runner.expected_data["m_name"]
    runner.assertCountEqual(expected_names, names)
    print("Expected Matrix Chemical Names found")


# TODO Reimplement
@disable_test
def test_matrix_trade_names(runner, expected_names=None):
    # Check if the names of the chemicals are present
    print("\n\nMatrix Trade Names")
    names = runner.app.db.query(
    """
    SELECT ?trade
    WHERE {
        ?mat <http://semanticscience.org/resource/hasRole> ?bnode_mat .
        ?bnode_mat a <http://nanomine.org/ns/Matrix> .
        ?mat <http://semanticscience.org/resource/hasAttribute> ?prop .
        ?prop a <http://nanomine.org/ns/TradeName> .
        ?prop <http://semanticscience.org/resource/hasValue> ?trade .
    }
    """
    )
    names = [name[0] for name in names]
    if expected_names is None:
        expected_names = runner.expected_data["m_trd_name"]
    runner.assertCountEqual(expected_names, names)
    print("Expected Matrix Chemical Trade Names found")


def test_filler_chemical_names(runner, expected_names=None):
    # Check if the names of the chemicals are present
    print("\n\nFiller Chemical Names")
    names = runner.app.db.query(
        """
    SELECT ?chemName WHERE {
        ?Filler <http://semanticscience.org/resource/hasRole> ?bnode .
        ?Filler a ?chemURI .
        ?bnode a <http://nanomine.org/ns/Filler> .
        ?chemURI <http://www.w3.org/2000/01/rdf-schema#label> ?chemName .
    }
    """
    )
    names = [name[0] for name in names]
    if expected_names is None:
        expected_names = runner.expected_data["f_name"]
    runner.assertCountEqual(expected_names, names)
    print("Expected Filler Chemical Names found")


# TODO Reimplement
@disable_test
def test_filler_trade_names(runner, expected_names=None):
    # Check if the names of the chemicals are present
    print("\n\nFiller Trade Names")
    names = list(runner.app.db.query(
    """
    SELECT ?trade
    WHERE {
        ?mat <http://semanticscience.org/resource/hasRole> ?bnode_mat .
        ?bnode_mat a <http://nanomine.org/ns/Filler> .
        ?mat <http://semanticscience.org/resource/hasAttribute> ?prop .
        ?prop a <http://nanomine.org/ns/TradeName> .
        ?prop <http://semanticscience.org/resource/hasValue> ?trade .
    }
    """
    ))
    names = [name[0] for name in names]
    if expected_names is None:
        expected_names = runner.expected_data["f_trd_name"]
    runner.assertCountEqual(expected_names, names)
    print("Expected Filler Chemical Trade Names found")


# TODO Fix or remove
@disable_test
def test_temperatures(runner, expected_temperatures=None):
    print("Checking if the expected temperatures are present")
    temperatures = list(runner.app.db.objects(
        None, rdflib.URIRef("http://purl.obolibrary.org/obo/PATO_0000146")))
    if expected_temperatures is None:
        expected_temperatures = runner.expected_data["temps"]
    runner.assertCountEqual(expected_temperatures, temperatures)
    print("Expected Temperatures Found")


# TODO Reimplement
@disable_test
def test_abbreviations(runner, expected_abbreviations=None):
    print("Checking if the expected abbreviations are present")
    abbreviations = list(runner.app.db.query(
    """
    SELECT ?abbrev
    WHERE {
        ?prop a <http://nanomine.org/ns/Abbreviation> .
        ?prop <http://semanticscience.org/resource/hasValue> ?abbrev .
    }
    """
    ))
    abbreviations = [a[0] for a in abbreviations]
    if expected_abbreviations is None:
        expected_abbreviations = runner.expected_data["abbrev"]
    runner.assertCountEqual(expected_abbreviations, abbreviations)
    print("Expected Abbreviations Found")


# TODO Reimplement
@disable_test
def test_manufacturers(runner, expected_manufacturers=None):
    print("Checking if the expected manufactures are present")
    manufacturers = list(runner.app.db.query(
        """
        SELECT ?manufac
        WHERE {
            ?prop a <http://nanomine.org/ns/Manufacturer> .
            ?prop <http://semanticscience.org/resource/hasValue> ?manufac .
        }
        """
        ))
    manufacturers = [m[0] for m in manufacturers]
    if expected_manufacturers is None:
        expected_manufacturers = runner.expected_data["manufac"]
    runner.assertCountEqual(expected_manufacturers, manufacturers)
    print("Expected Manufactures Found")


# TODO Reimplement
@disable_test
def test_complete_material(runner, expected_materials=None):
    materials = runner.app.db.query(
        """
    SELECT ?abbrev ?manufac ?name ?trade
    WHERE {
        ?mat <http://semanticscience.org/resource/hasRole> ?bnode_mat .
        ?mat a ?compound .
        { ?bnode_mat a <http://nanomine.org/ns/Matrix> } UNION { ?bnode_mat a <http://nanomine.org/ns/Filler> } .
        OPTIONAL {?mat <http://semanticscience.org/resource/hasAttribute> ?bnode_abbrev .
                  ?bnode_abbrev a <http://nanomine.org/ns/Abbreviation> .
                  ?bnode_abbrev <http://semanticscience.org/resource/hasValue> ?abbrev} .

        OPTIONAL {?mat <http://semanticscience.org/resource/hasAttribute> ?bnode_manufac .
                  ?bnode_manufac a <http://nanomine.org/ns/Manufacturer> .
                  ?bnode_manufac <http://semanticscience.org/resource/hasValue> ?manufac} .

        OPTIONAL {?compound <http://www.w3.org/2000/01/rdf-schema#label> ?name} .


        OPTIONAL {?mat <http://semanticscience.org/resource/hasAttribute> ?bnode_trade .
                  ?bnode_trade a <http://nanomine.org/ns/TradeName> .
                  ?bnode_trade <http://semanticscience.org/resource/hasValue> ?trade} .
    }
    """
    )
    material_properties = list()
    for material in materials:
        material_dict = dict()
        for key in material.labels.keys():
            material_dict[key] = material[key]
        material_properties.append(material_dict)

    if expected_materials is None:
        expected_materials = runner.expected_data["compiled_material"]

    runner.assertCountEqual(expected_materials, material_properties)


def test_dielectric_real_permittivity(runner, expected_frequency, expected_real_permittivity, descriptions):
    print("Checking if the Dielectric Real Permittivity Table is as expected")
    values = query_table(runner, "<http://nanomine.org/ns/RealPartOfDielectricPermittivity>", "<http://nanomine.org/ns/FrequencyHz>", **descriptions)
    frequency = [v["independentVar"] for v in values]
    real_permittivity = [v["dependentVar"] for v in values]
    runner.assertCountEqual(expected_frequency, frequency)
    runner.assertCountEqual(expected_real_permittivity, real_permittivity)


def test_dielectric_loss_tangent(runner, expected_frequency, expected_tan_delta, descriptions):
    print("Checking if Dielectric Loss Tangent Table is as expected")
    values = query_table(runner, "<http://nanomine.org/ns/TanDelta>", "<http://nanomine.org/ns/FrequencyHz>", **descriptions)
    frequency = [v["independentVar"] for v in values]
    tan_delta = [v["dependentVar"] for v in values]
    runner.assertCountEqual(expected_frequency, frequency)
    runner.assertCountEqual(expected_tan_delta, tan_delta)

# TODO Fix or remove
@disable_test
def test_filler_processing(runner, expected_process=None):
    print("Testing Filler Processing")
    process = runner.app.db.query(
    """
    SELECT ?method
    WHERE {
        ?sequence a <http://nanomine.org/ns/ExperimentalProcedure> .
        ?sequence <http://semanticscience.org/resource/hasPart> ?method .
    }
    """
    )
    if expected_process is None:
        expected_process = runner.expected_data["filler_processing"]
    runner.assertTrue(expected_process is not None)
    runner.assertTrue(process is not None)
    runner.assertCountEqual(expected_process, process)  # TODO figure out how to query ordering in process order


# TODO Reimplement
@disable_test
def test_viscoelastic_measurement_mode(runner, expected_mode=None):
    print("Testing viscoelastic measurement mode")
    mode = list(runner.app.db.objects(
        None, rdflib.URIRef("http://nanomine.org/ns/tensile")))
    if expected_mode is None:
        expected_mode = runner.expected_data["viscoelastic_measurement_mode"]
    runner.assertCountEqual(expected_mode, mode)
    print("Expected mode Found")

# TODO Add autoparsing
def test_tensile_loading_profile(runner, expected_strain=None, expected_stress=None):
    print("Stress value")
    values = query_table(runner, "<http://nanomine.org/ns/Stress>", "<http://nanomine.org/ns/Strain>")

    if expected_strain is None:
        raise NotImplementedError
    if expected_stress is None:
        raise NotImplementedError
    
    stress = [value["dependentVar"] for value in values]
    strain = [value["independentVar"] for value in values]
    runner.assertCountEqual(expected_strain, strain) 
    runner.assertCountEqual(expected_stress, stress) 
    print("Expected Stress  value Found") 

# TODO Add autoparsing
# TODO Verify node type, currently doesn't
def test_flexural_loading_profile(runner, expected_strain=None, expected_stress=None):
    print("Testing Flexural Loading Profile")
    values = query_table(runner, "<http://nanomine.org/ns/Stress>", "<http://nanomine.org/ns/Strain>")
    print("Finished Query", flush=True)
    if expected_strain is None:
        raise NotImplementedError
    if expected_stress is None:
        raise NotImplementedError
    
    stress = [value["dependentVar"] for value in values]
    strain = [value["independentVar"] for value in values]

    runner.assertCountEqual(expected_strain, strain) 
    runner.assertCountEqual(expected_stress, stress) 
    print("Expected Flexural Loading Profile Found") 


# TODO Refactor to remove usage of specific bnodes
# TODO Reimplement 
@disable_test
def test_melt_viscosity(runner, expected_value=None):
    print("\n\nMelt Viscosity")
    values = runner.app.db.query(
    """
    SELECT ?value
    WHERE {
        <bnode:cfff5d04317445c49f22102e124ab68e> <http://semanticscience.org/resource/hasValue> ?value .
        <bnode:cfff5d04317445c49f22102e124ab68e> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://nanomine.org/ns/MeltVisocsity> .
        <http://nanomine.org/sample/l256-s3-potschke-2004_nanomine-meltviscosity_9> <http://semanticscience.org/resource/hasAttribute> <bnode:cfff5d04317445c49f22102e124ab68e> .
    }
    """
    )
    values = [value[0] for value in values]
    if expected_value is None:
        expected_authors = runner.expected_data["melt_viscosity_data"]
    runner.assertCountEqual(expected_value, values)
    print("Expected Melt Viscosity values found")


# TODO Add autoparsing
def test_rheometer_mode(runner, expected_modes=None):
    print("\n\nTesting for Rheometer Mode")
    modes = runner.app.db.objects(None, rdflib.URIRef("http://nanomine.org/ns/RheometerMode"))
    modes = list(modes)
    if expected_modes is None:
        raise NotImplementedError
    runner.assertCountEqual(expected_modes, modes)
    print("Expected Rheometer Modes Found")


def test_specific_surface_area(runner, expected_area=None, expected_units=None):
    print("\n\nTesting for specific surface area")
    query_results = runner.app.db.query(
        '''
        SELECT ?area ?unit_label
        WHERE
        {
            ?aNode a <http://nanomine.org/ns/SpecificSurfaceArea> .
            ?aNode <http://semanticscience.org/resource/hasValue> ?area .
            ?aNode <http://semanticscience.org/resource/hasUnit> ?unit .
            ?unit <http://www.w3.org/2000/01/rdf-schema#label> ?unit_label .
        }
        '''
        )
    surface_area =[result["area"] for result in query_results]
    units = [result["unit_label"] for result in query_results]
    if expected_area is None:
        expected_area = runner.expected_data["specific_surface_area"]
    if expected_units is None:
        expected_units = runner.expected_data["specific_surface_area_units"]
    runner.assertCountEqual(expected_area, surface_area)
    runner.assertCountEqual(expected_units, units)


def test_shear_loading_profile(runner, expected_aspect_ratio, expected_number, descriptions, types):
    print("Testing shear loading profile")
    values = query_table(runner, types["y_type"], types["x_type"], **descriptions)

    number = [value["dependentVar"] for value in values]
    aspect_ratio = [value["independentVar"] for value in values]

    runner.assertCountEqual(expected_aspect_ratio, aspect_ratio)
    runner.assertCountEqual(expected_number, number)


def test_weibull_plot(runner, expected_breakdown, expected_failure, descriptions):
    print("Testing Weibull Plot")
    values = query_table(runner, "<http://nanomine.org/ns/ProbabilityOfFailure>", "<http://nanomine.org/ns/BreakdownStrength>", **descriptions)

    breakdown = [value["independentVar"] for value in values]
    failure = [value["dependentVar"] for value in values]

    runner.assertCountEqual(expected_breakdown, breakdown)
    runner.assertCountEqual(expected_failure, failure)



disabled.append("test_triples")     # Prevent triples from being printed in CI
def print_triples(runner):
    if os.getenv("CI") is None:
        print("Printing SPO Triples")
        for s, p, o in runner.app.db.triples((None, None, None)):
            print(str(s.n3()) + " " + str(p.n3()) + " " + str(o.n3()) + " .")
