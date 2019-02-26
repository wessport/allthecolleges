import base64
import hashlib
from scrapy.exporters import JsonLinesItemExporter, JsonItemExporter
from scrapy.utils.python import to_bytes


mapping = (
    ('school_id', 'school_id'),
    ('street_address', 'street_address'),
    ('city', 'city'),
    ('state', 'state'),
    ('postcode', 'postcode'),
    ('name', 'name'),
    ('website', 'website'),
)


def item_to_properties(item):
    props = {}

    # Ref is required
    props['ref'] = str(item['ref'])

    # Add in the extra bits
    extras = item.get('extras')
    if extras:
        props.update(extras)

    # Bring in the optional stuff
    for map_from, map_to in mapping:
        item_value = item.get(map_from)
        if item_value:
            props[map_to] = item_value

    return props


def compute_hash(item):
    ref = str(item.get('ref') or '').encode('utf8')
    sha1 = hashlib.sha1(ref)

    spider_name = item.get('extras', {}).get('@spider')
    if spider_name:
        sha1.update(spider_name.encode('utf8'))

    return base64.urlsafe_b64encode(sha1.digest()).decode('utf8')


class LineDelimitedGeoJsonExporter(JsonLinesItemExporter):

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        feature = []
        feature.append(('type', 'Feature'))
        feature.append(('id', compute_hash(item)))
        feature.append(('properties', item_to_properties(item)))

        if item.get('lon'):
            feature.append(('geometry', {
                'type': 'Point',
                'coordinates': [
                    float(item['lon']),
                    float(item['lat'])
                ],
            }))

        return feature


class GeoJsonExporter(JsonItemExporter):

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        feature = []
        feature.append(('type', 'Feature'))
        feature.append(('id', compute_hash(item)))
        feature.append(('properties', item_to_properties(item)))

        if item.get('lon'):
            feature.append(('geometry', {
                'type': 'Point',
                'coordinates': [
                    float(item['lon']),
                    float(item['lat'])
                ],
            }))

        return feature

    def start_exporting(self):
        self.file.write(to_bytes('{"type":"FeatureCollection","features":[', self.encoding))

    def finish_exporting(self):
        self.file.write(to_bytes(']}', self.encoding))
