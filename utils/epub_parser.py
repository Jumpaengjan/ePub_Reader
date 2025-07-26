import zipfile
import os
import xml.etree.ElementTree as ET

def extract_epub(epub_path, extract_to='temp_epub'):
    with zipfile.ZipFile(epub_path, 'r') as z:
        z.extractall(extract_to)

    # Locate content.opf path via META-INF/container.xml
    container_path = os.path.join(extract_to, 'META-INF', 'container.xml')
    tree = ET.parse(container_path)
    root = tree.getroot()
    ns = {'ns': 'urn:oasis:names:tc:opendocument:xmlns:container'}
    opf_path = root.find('ns:rootfiles/ns:rootfile', ns).attrib['full-path']
    return os.path.join(extract_to, opf_path)

def get_html_paths(opf_path):
    base_path = os.path.dirname(opf_path)
    tree = ET.parse(opf_path)
    root = tree.getroot()

    ns = {'opf': 'http://www.idpf.org/2007/opf'}

    manifest = {item.attrib['id']: item.attrib['href'] for item in root.find('opf:manifest', ns)}
    spine = root.find('opf:spine', ns)
    itemrefs = [item.attrib['idref'] for item in spine]

    html_paths = [os.path.join(base_path, manifest[idref]) for idref in itemrefs if idref in manifest]
    return html_paths
