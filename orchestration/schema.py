from ariadne import gql, QueryType, make_executable_schema

type_defs = gql("""
    type Query {
        hello: String!
    }
""")

def resolve_hello(*_):
    return "Hello!"

query = QueryType()
query.set_field("hello", resolve_hello)
schema = make_executable_schema(type_defs, query)