from pymongo import MongoClient

from fdcmp.settings import env


class MCPMongoService:
    def __init__(self) -> None:
        super().__init__()
        self.dbName = env("MCP_DB_NAME")
        self.client = MongoClient(host=env('MCP_DB_HOST'),
                    port=int(env("MCP_DB_PORT")),
                    username=env("MCP_DB_USER_NAME"),
                    password=env("MCP_DB_PASS"),
                    authSource=env('MCP_DB_AUTH_SOURCE'),
                    authMechanism=env('MCP_DB_AUTH_MECHANISM'))

    def insert(self, collect, query):
        return self.client[self.dbName][collect].insert(query)

    def find_one(self,collect, filter):
        return self.client[self.dbName][collect].find_one(filter)

    def update_one(self,collect, filter, updateQuery):
        return self.client[self.dbName][collect].update_one(filter,{"$set": updateQuery})

    def list_indexes(self, collection):
        return self.client[self.dbName][collection].list_indexes()

    def create_index(self, collection, index_name, index, expireAfterSeconds=None):
        if expireAfterSeconds is not None:
            return self.client[self.dbName][collection].create_index(index, name=index_name, expireAfterSeconds=expireAfterSeconds)
        return self.client[self.dbName][collection].create_index(index, name=index_name)

    def close(self):
        self.client.close()
