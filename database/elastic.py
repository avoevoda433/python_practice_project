from elasticsearch import Elasticsearch


class Elastic:

    def __init__(self, host: str, index: str):
        self.host = host
        self.index = index

    def __connection(self):
        return Elasticsearch(self.host)

    def add_index(self, id_ind: str, data: dict):
        self.__connection().index(index=self.index, id=id_ind, document=data)

    def find_document(self, response: str):
        return self.__connection().search(index=self.index, query={'match': {'text': response}})
