from elasticsearch_dsl import DocType, Search, Date, Integer, Keyword, Text, Ip
from elasticsearch_dsl import connections, InnerDoc, Nested, Object


class IoTDetailsDoc(DocType):
    '''
    Document storage for IoT IP cache
    '''
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    tags = Keyword()
    doc_created = Date()
    doc_updated = Date()
    processed = Integer()

    class Index:
        name = 'sfn-iot-details'

    @classmethod
    def get_indexable(cls):
        return cls.get_model().get_objects()

    @classmethod
    def from_obj(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            tags=obj.tags,
            doc_created=obj.doc_created,
            doc_updated=obj.doc_updated,
            processed=obj.processed,
        )

    def save(self, **kwargs):
        return super(IoTDetailsDoc, self).save(**kwargs)


class SFNIOT(InnerDoc):
    event_type = Text()
    domain_name = Text(analyzer='snowball', fields={'raw': Keyword()})
    device_name = Text(analyzer='snowball', fields={'raw': Keyword()})
    host = Text(analyzer='snowball', fields={'raw': Keyword()})
    threat_id = Text(analyzer='snowball')
    threat_name = Text(analyzer='snowball')
    tag_name = Text(fields={'raw': Keyword()})
    tag_class = Text(fields={'raw': Keyword()})
    tag_group = Text(fields={'raw': Keyword()})
    tag_description = Text(analyzer='snowball')
    public_tag_name = Text(analyzer='snowball')
    confidence_level = Integer()
    sample_date = Date()
    file_type = Text(fields={'raw': Keyword()})
    updated_at = Date()
    processed = Integer()
    src_ip = Ip()
    dst_ip = Ip()


class IoTEventDoc(DocType):
    '''
    Each event is it's own entity in the DB. This is the structure of that entitiy
    '''
    IoT = Object(SFNIOT)
    
    class Index:
         name = 'iot-*'

    @classmethod
    def get_indexable(cls):
        return cls.get_model().get_objects()

    @classmethod
    def from_obj(cls, obj):
        return cls(
            id=obj.id,
            domain_name=obj.domain_name,
            device_name=obj.device_name,
            host=obj.host,
            threat_id=obj.threat_id,
            event_tag=obj.event_tag,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            processed=obj.processed,
            src_ip=obj.src_ip,
            dst_ip=obj.dst_ip
        )

    def save(self, **kwargs):
        return super(IoTEventDoc, self).save(**kwargs)


class TagDetailsDoc(DocType):
    '''
    Stores/caches information about each tag in the DB
    '''
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    tag = Keyword()
    tag_groups = Keyword()
    doc_created = Date()
    doc_updated = Date()
    processed = Integer()

    class Index:
        name = 'sfn-tag-details'

    @classmethod
    def get_indexable(cls):
        return cls.get_model().get_objects()

    @classmethod
    def from_obj(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            tag=obj.tag,
            tag_groups=obj.tag_groups,
            doc_created=obj.doc_created,
            doc_updated=obj.doc_updated,
            processed=obj.processed,
        )

    def save(self, **kwargs):
        return super(TagDetailsDoc, self).save(**kwargs)
