import argparse
from sword2 import Connection
from sword2 import Entry

SD_URI = 'http://localhost:8080/sd-uri'

c = Connection(SD_URI, user_name = "foo", user_pass="bar")
import pdb;pdb.set_trace()

c.get_service_document()
# pick the first collection within the first workspace:
workspace_1_title, workspace_1_collections = c.workspaces[0]
collection = workspace_1_collections[0]

# upload "package.zip" to this collection as a new (binary) resource:
with open("package.zip", "r") as pkg:
    receipt = c.create(col_iri = collection.href,
                                payload = pkg,
                                mimetype = "application/zip",
                                filename = "package.zip",
                                packaging = 'http://purl.org/net/sword/package/Binary',
                                in_progress = True)    # As the deposit isn't yet finished


# Add a metadata record to this newly created resource (or 'container')
# Entry can be passed keyword parameters to add metadata to the entry (namespace + '_' + tagname)
e = Entry(id="atomid", 
          title="atom-title",
          dcterms_abstract = "Info about the resource....")
# to add a new namespace:
e.register_namespace('skos', 'http://www.w3.org/2004/02/skos/core#')
e.add_field("skos_Concept", "...")


# Update the metadata entry to the resource:
updated_receipt = c.update(metadata_entry = e,
                           dr = receipt,   # use the receipt to discover the right URI to use
                           in_progress = False)  # finish the deposit


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
