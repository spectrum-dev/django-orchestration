from ariadne import QueryType, make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers, MutationType

import strategy.resolvers

type_defs = [
    load_schema_from_path("orchestration/schema.graphql"),
    load_schema_from_path("strategy/schema.graphql")
]

# Query Implementations
query = QueryType()
query.set_field("userStrategies", strategy.resolvers.list_user_strategies)

# Mutation Implementations
mutation = MutationType()

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)